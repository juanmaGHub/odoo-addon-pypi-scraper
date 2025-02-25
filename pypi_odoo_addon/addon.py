import re

from .pypi_api_json import PyPIJSON


PREFIX_CHANGES_AT_VERSION = 14

PYPI_ODOO_ADDON_VERSION_PREFIX = r"^odoo\d{2}-addon-"
PYPI_ODOO_ADDON_NO_VERSION_PREFIX = r"^odoo-addon-"


class PyPIOdooAddon:
    def __init__(self, name, odoo_version):
        self.name = name
        self.odoo_version = odoo_version
        self.target_name = self._get_odoo_addon_target_name(name)
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

    def _get_odoo_addon_target_version(self):
        """
        Get the latest version of the target Odoo addon
        """
        data = PyPIJSON.get_package_data(self.target_name)
        data = PyPIJSON.parse_package_data(data)
        str_odoo_version = str(self.odoo_version) + ".0"
        if str_odoo_version in data.get("latest_version", ""):
            return data.get("latest_version", None)
        for release in data.get("releases", []):
            if str_odoo_version in release:
                return release
        return None
