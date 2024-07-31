# odoo-addon-pypi-scraper
Simple tool to find Odoo addons in PyPI by name and Odoo version and update
Odoo requirements file.

## Motivation
When migrating Odoo databases, you might need to track odoo modules packages accross
versions and even though this script will skip everything but odoo addons and some
odoo addons might not exist in your target Odoo version, it might save some time. 

## Usage
To use the script, you need to provide the following required arguments:

1. `--file-path`: The path to your Odoo requirements.txt file.
2. `--odoo-version`: The version of Odoo you want the addons to be compatible with.

Here's an example of how to run the script with the required arguments:

```bash
python main.py --file-path /your_path/requirements.txt --odoo-version 14.0
```

Optionally, you could pass --verbose (-V) to print progress in the terminal.
