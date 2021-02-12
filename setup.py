#!/usr/bin/env python3

"""Setup for python module."""

import os
import sys
from setuptools import setup
from pathlib import Path
from setuptools.command.test import test as test_command


def get_requirements():
    """Get requirements."""
    with open("requirements.txt") as fd:
        return fd.read().splitlines()


def get_version():
    """Get version."""
    with open(os.path.join("thoth", "python", "__init__.py")) as f:
        content = f.readlines()

    for line in content:
        if line.startswith("__version__ ="):
            # dirty, remove trailing and leading chars
            return line.split(" = ")[1][1:-2]

    raise ValueError("No package version found")


class Test(test_command):
    """Introduce test command to run testsuite using pytest."""

    _IMPLICIT_PYTEST_ARGS = [
        "tests/",
        "--timeout=600",
        "--cov=./thoth",
        "--mypy",
        "--capture=no",
        "--verbose",
        "-l",
        "-s",
        "-vv",
    ]

    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        """Initialize options."""
        super().initialize_options()
        self.pytest_args = None

    def finalize_options(self):
        """Finalize options."""
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run tests."""
        import pytest

        passed_args = list(self._IMPLICIT_PYTEST_ARGS)

        if self.pytest_args:
            self.pytest_args = [arg for arg in self.pytest_args.split() if arg]
            passed_args.extend(self.pytest_args)

        sys.exit(pytest.main(passed_args))


VERSION = get_version()

setup(
    name="thoth-python",
    version=VERSION,
    packages=["thoth.python"],
    package_data={"thoth.python": ["py.typed"]},
    install_requires=get_requirements(),
    author="Fridolin Pokorny",
    author_email="fridolin@redhat.com",
    maintainer="Fridolin Pokorny",
    maintainer_email="fridolin@redhat.com",
    description="A Python ecosystem specific library",
    long_description=Path("README.rst").read_text(),
    url="https://github.com/thoth-station/python",
    license="GPLv3+",
    keywords="python dependency pypi dependencies tool library thoth",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    cmdclass={"test": Test},
    command_options={
        "build_sphinx": {
            "version": ("setup.py", VERSION),
            "release": ("setup.py", VERSION),
        }
    },
)
