from setuptools import setup

import os
import sys
import json

sys.path.append("radio_sim")


def package_files(package_dir, subdirectory):
    # walk the input package_dir/subdirectory
    # return a package_data list
    paths = []
    directory = os.path.join(package_dir, subdirectory)
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            path = path.replace(package_dir + "/", "")
            paths.append(os.path.join(path, filename))
    return paths


data_files = package_files("hera_cal", "data") + package_files(
    "hera_cal", "calibrations"
)

setup_args = {
    "name": "radio_sim",
    "author": "Tyler Cox",
    "url": "https://github.com/tyler-a-cox/radio_sim",
    "license": "BSD",
    "description": "collection of calibration routines to run on the HERA instrument.",
    "package_dir": {"radio_sim": "radio_sim"},
    "packages": ["radio_sim"],
    "include_package_data": True,
    "scripts": [],
    "package_data": {"radio_sim": data_files},
    "install_requires": [
        "numpy>=1.10",
        "scipy",
        "astropy",
        "pyuvdata",
    ],
    "extras_require": {
        "all": [
            "aipy>=3.0",
        ]
    },
    "zip_safe": False,
}


if __name__ == "__main__":
    setup(*(), **setup_args)
