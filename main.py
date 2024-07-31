import os
import sys
import argparse

from pypi_odoo_addon.addon import PyPIOdooAddon


OUTPUT_DIR = "data"


def update_requirements_file(path, odoo_version, verbose=False):
    """
    Read the requirements file and generate new requirements content
    with the target addon name and version.
    """
    with open(path, "r") as file:
        addons, others, missing = [], [], []
        for line in file.readlines():
            if verbose:
                print("-" * 80)
                print(f"Processing line: {line}")

            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if not line.startswith("odoo"):
                others.append(line)
                continue

            addon = PyPIOdooAddon(line, odoo_version)
            if addon.target_addon_version and addon.target_name:
                if verbose:
                    print("Found addon for target version: ")
                    print(f"Addon: {addon.target_name}=={addon.target_addon_version}")
                addons.append(addon.target_name + "==" + addon.target_addon_version)
            else:
                missing.append(line)

    return addons, others, missing


def write_requirements_file(dir, odoo_version, addons, others):
    """
    Write the new requirements content to the requirements file.
    """
    path = os.path.join(dir, f"requirements-{odoo_version}.txt")
    requirements = others + addons
    with open(path, "w") as file:
        for requirement in requirements:
            file.write(requirement + "\n")


def write_missing_file(dir, odoo_version, missing):
    """
    Write the missing addons to a file.
    """
    path = os.path.join(dir, f"missing-requirements-{odoo_version}.txt")
    with open(path + "_missing.txt" , "w") as file:
        for miss in missing:
            file.write(miss + "\n")

def write_output(dir, odoo_version, addons, others, missing):
    """
    Write the new requirements content to the requirements file.
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

    write_requirements_file(dir, odoo_version, addons, others)
    write_missing_file(dir, odoo_version, missing)

def main():
    parser = argparse.ArgumentParser(
        description="Update the requirements for the target Odoo version."
    )
    parser.add_argument(
        "--file-path",
        "-f",
        type=str,
        required=True,
        help="The path to the requirements file.",
    )
    parser.add_argument(
        "--odoo-version", "-v", type=str, required=True, help="The target Odoo version."
    )
    parser.add_argument("--verbose", "-V", action="store_true", help="Log progress.")
    args = parser.parse_args()

    file_path = args.file_path.strip()
    odoo_version = args.odoo_version.strip()
    try:
        odoo_version = int(odoo_version.split(".")[0])
    except ValueError:
        raise ValueError("Odoo version must be major. E.g. 14.0 or 14")

    if args.verbose:
        print(f"Updating requirements file: {file_path}")
        print(f"Target Odoo version: {odoo_version}")

    addons, others, missing = update_requirements_file(
        file_path, odoo_version, args.verbose
    )
    
    if args.verbose:
        print("Writing new requirements file...")
    write_output(OUTPUT_DIR, odoo_version, addons, others, missing)
    
    if args.verbose:
        print("Done!")

if __name__ == "__main__":
    main()
