import requests


PYPI_URL = "https://pypi.org/pypi"
PYPI_JSON_PATH = "json"


class PyPIJSON:
    @staticmethod    
    def get_package_data(package_name):
        """
        Get the data of a package from PyPI
        :param package_name: The name of the package
        :return: The data of the package
        """
        url = f"{PYPI_URL}/{package_name}/{PYPI_JSON_PATH}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": f"HTTP error occurred: {err}"}
        except requests.exceptions.RequestException as err:
            return {"error": f"Request error occurred: {err}"}

    @staticmethod
    def parse_package_data(data):
        """
        Parse the data of an Odoo addon from PyPI
        :param data: The data of the package
        :return: The parsed data
        """
        if "info" not in data:
            return {"error": "No package info found"}
        info = data["info"]

        if "releases" not in data:
            return {"error": "No package releases found"}

        releases = list(data["releases"].keys())
        releases.sort()

        return {
            "name": info["name"],
            "version": info["version"],
            "summary": info["summary"],
            "description": "See https://pypi.org/project/" + info["name"],
            "license": info["license"],
            "author": info["author"],
            "author_email": info["author_email"],
            "home_page": info["home_page"],
            "keywords": info["keywords"],
            "classifiers": info["classifiers"],
            "releases": releases,
            "latest_version": releases[-1] if releases else None,
        }