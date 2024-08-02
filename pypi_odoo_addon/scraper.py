from urllib.parse import urlparse, urlunparse, urlencode

import requests
from bs4 import BeautifulSoup


PYPI_URL = "https://pypi.org"
PYPI_SEARCH_PATH = "search"
PYPI_ODOO_FRAMWORK = "Framework :: Odoo"

MAX_PAGE = 5


class PyPIScraper:
    """
    A scraper to get the project URL or the project version from PyPI.
    """

    def __init__(self, odoo_version, base_url=None) -> None:
        self.base_url = base_url or PYPI_URL
        self.odoo_version = odoo_version

    def _url_builder(self, path, query={}, fragment=""):
        """
        Build new URL based on the base URL.
        path: str
            The path to add to the base URL (e.g. /search, /project/addon_name).
        query: dict
            The query parameters to add to the URL.
            (e.g. {"q": "addon_name", "c": "Framework :: Odoo"}).
        """
        if query:
            query = urlencode(query)

        # parse the base URL (https://pypi.org)
        base_url = urlparse(self.base_url)

        return urlunparse((base_url.scheme, base_url.netloc, path, "", query, fragment))

    def _make_request(self, path, query={}, fragment=""):
        """
        Make a request to PyPI.
        path: str
            The path to add to the base URL (e.g. /search, /project/addon_name).
        query: dict
            The query parameters to add to the URL.
            (e.g. {"q": "addon_name", "c": "Framework :: Odoo"}).
        fragment: str
            The fragment to add to the URL. (e.g. #history).
        """
        url = self._url_builder(path, query, fragment)
        try:
            response = requests.get(url)
            response.raise_for_status()

            return BeautifulSoup(response.content, "html.parser")

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Invalid response from PyPI: {e}")

        except Exception as e:
            raise ValueError(f"Error while parsing the response: {e}")

    def _search_package(self, soup, value):
        """
        Search for the package (value) in content search results.
        soup: BeautifulSoup object
            The parsed content from the request.
        value: str
            The package (value) to search.
        """
        search_results = soup.find(
            "ul", {"class": "unstyled", "aria-label": "Search results"}
        )
        if not search_results:
            return None

        for li in search_results.find_all("li"):
            match = li.find("a", {"class": "package-snippet"})["href"]
            if value == match.strip("/").split("/")[-1]:
                return match
        return None

    def _search_release_timeline(self, soup):
        """
        Search for the release timeline in the project page.
        soup: BeautifulSoup object
            The parsed content from the request.
        """
        timeline = soup.find("div", {"class": "release-timeline"})
        if not timeline:
            return None
        for a in timeline.find_all("a", {"class": "card release__card"}):
            p_version = a.find("p", {"class": "release__version"})
            if p_version and p_version.text.strip().startswith(
                str(self.odoo_version)
            ):
                return p_version.text.strip()
        return None

    def _get_project_version(self, soup, fragment):
        if not fragment:
            project_header = soup.find("h1", {"class": "package-header__name"})
            if project_header:
                name_and_version = project_header.text.strip().split(" ")
                if len(name_and_version) > 1:
                    return name_and_version[-1]

            return None
        return self._search_release_timeline(soup)

    def pypi_request(self, path, fragment="", value=None):
        """
        Wrapper to make a request to PyPI from an external class.
        is_search: bool
            If True, the request is a search request.
        value: str
            The value to search or the project name.
        """
        if path == PYPI_SEARCH_PATH:
            if not value:
                raise ValueError("The value to search is required.")

            query = {"q": value, "o": "", "c": PYPI_ODOO_FRAMWORK}
            for page in range(1, MAX_PAGE + 1):
                if page > 1:
                    query["page"] = page

                parsed_response = self._make_request(path, query, fragment)
                package = self._search_package(parsed_response, value)
                if package:
                    return package
            return None

        parsed_response = self._make_request(path, fragment=fragment)
        return self._get_project_version(parsed_response, fragment)
