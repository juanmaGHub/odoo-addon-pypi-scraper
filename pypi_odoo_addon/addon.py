import re

from .scraper import PyPIScraper


PREFIX_CHANGES_AT_VERSION = 14

PYPI_ODOO_ADDON_VERSION_PREFIX = r"^odoo\d{2}-addon-"
PYPI_ODOO_ADDON_NO_VERSION_PREFIX = r"^odoo-addon-"


class PyPIOdooAddon:
    def __init__(self, name, odoo_version):
        self.name = name
        self.odoo_version = odoo_version
        self.target_name = self._get_odoo_addon_target_name(name)
        self.pypi_scraper = PyPIScraper(odoo_version)
        self.target_project_path = self._get_odoo_addon_target_project()
        self.target_addon_version = self._get_odoo_addon_target_version()

    def _get_odoo_addon_target_name(self, name):
        """
        Compute the addon name with the version context as setuptools requires
        for a specific version of Odoo.
        """
        name = name.strip().lower().split("==")[0]
        name = re.sub(PYPI_ODOO_ADDON_VERSION_PREFIX, "", name)
        name = re.sub(PYPI_ODOO_ADDON_NO_VERSION_PREFIX, "", name)

        if self.odoo_version <= PREFIX_CHANGES_AT_VERSION:
            return f"odoo{self.odoo_version}-addon-{name}"

        return f"odoo-addon-{name}"

    def _get_odoo_addon_target_project(self):
        if not self.target_name:
            return None

        project_path = self.pypi_scraper.pypi_request("search", value=self.target_name)
        return project_path.strip("/") if project_path else None

    def _get_odoo_addon_target_version(self):
        if not self.target_project_path:
            return None
        fragment = ""
        if self.odoo_version > PREFIX_CHANGES_AT_VERSION:
            fragment = "history"

        target_version = self.pypi_scraper.pypi_request(
            self.target_project_path, fragment=fragment
        )
        return target_version
