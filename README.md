# odoo-addon-pypi-scraper
Simple tool to find Odoo addons in PyPI by name and Odoo version and update
Odoo requirements file.

## Motivation
When migrating Odoo databases, you might need to track odoo modules packages accross
versions and even though this script will skip everything but odoo addons and some
odoo addons might not exist in your target Odoo version, it might save some time.

## Scraper
In case of changes in PyPI web front changes. Below there are some code snippets with
the HTML elements and CSS classes the script relies on to get packages versions.

### Package Search
```code
search_results = soup.find(
    "ul", {"class": "unstyled", "aria-label": "Search results"}
)

...

for li in search_results.find_all("li"):
    match = li.find("a", {"class": "package-snippet"})["href"]
    if value in match:
        return match
```

### Project
```code
project_header = soup.find("h1", {"class": "package-header__name"})
```

### Project Release History Search
```code
timeline = soup.find("div", {"class": "release-timeline"})

...

for a in timeline.find_all("a", {"class": "card release__card"}):
    p_version = a.find("p", {"class": "release__version"})
...
```

## Usage
To use the script, you need to provide the following required arguments:

1. `--file-path`: The path to your Odoo requirements.txt file.
2. `--odoo-version`: The version of Odoo you want the addons to be compatible with.

Here's an example of how to run the script with the required arguments:

```bash
python main.py --file-path /your_path/requirements.txt --odoo-version 14.0
```

Optionally, you could pass --verbose (-V) to print progress in the terminal.
