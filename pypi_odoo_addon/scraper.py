import requests
from bs4 import BeautifulSoup


PREFIX_CHANGES_AT_VERSION = 14

PYPI_ODOO_ADDON_VERSION_PREFIX = r"^odoo\d{2}-addon-"
PYPI_ODOO_ADDON_NO_VERSION_PREFIX = r"^odoo-addon-"

PYPI_URL = "https://pypi.org"
PYPI_SEARCH = "/search/?q="
PAYPI_ODOO_SEARCH_CONTEXT = "&o=&c=Framework+%3A%3A+Odoo"

MAX_PAGE = 5


class PyPIScraper:
    """
    A scraper to get the project URL or the project version from PyPI.
    """
    def __init__(self, base_url=None, odoo_context=None) -> None:
        self.base_url = base_url or PYPI_URL
        self.search_option = PYPI_SEARCH
        self.odoo_context = odoo_context or PAYPI_ODOO_SEARCH_CONTEXT
        self.addons = []

    def _make_request(self, is_search, value, page=1):
        """
        Make a request to PyPI.
        is_search: bool
            If True, the request is a search request.
        value: str
            The value to search or the project name.
        page: int
            The page number to search for the package in case of a search request.
        """
        search_context, option = "", ""
        if is_search:
            search_context = self.odoo_context
            option = self.search_option

        url = self.base_url + option + value + search_context
        if page > 1:
            url += f"&page={page}"

        url = self.base_url + option + value + search_context
        if page > 1:
            url += f"&page={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # return already parsed content
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
            if value in match:
                return match
        return None

    def _get_project_version(self, soup, value):
        project_header = soup.find("h1", {"class": "package-header__name"})
        if project_header:
            name_and_version = project_header.text.strip().split(" ")
            if len(name_and_version) > 1:
                return name_and_version[-1]

        return None

    def pypi_request(self, is_search, value):
        """
        Wrapper to make a request to PyPI from an external class.
        is_search: bool
            If True, the request is a search request.
        value: str
            The value to search or the project name.
        """
        if is_search:
            for page in range(1, MAX_PAGE + 1):
                parsed_response = self._make_request(is_search, value, page)
                package = self._search_package(parsed_response, value)
                if package:
                    return package
            return None

        parsed_response = self._make_request(is_search, value)
        return self._get_project_version(parsed_response, value)
