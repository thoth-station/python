#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# type: ignore

"""Tests for Pipfile and Pipfile.lock handling."""

import os

import pytest
import toml

from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.python import PackageVersion
from thoth.python import Source

from .base import PythonTestCase


class TestPipfile(PythonTestCase):

    @pytest.mark.parametrize("pipfile", [
        'Pipfile_test1',
    ])
    def test_from_string(self, pipfile: str):
        with open(os.path.join(self.data_dir, 'pipfiles', pipfile), 'r') as pipfile_file:
            content = pipfile_file.read()

        instance = Pipfile.from_string(content)
        # Sometimes toml does not preserve inline tables causing to_string() fail. However, we produce valid toml.
        assert instance.to_dict() == toml.loads(content)

    def test_pipfile_extras_parsing(self):
        instance = Pipfile.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_extras"))
        assert instance is not None
        assert len(instance.packages.packages) == 1
        assert "selinon" in instance.packages.packages
        package_version = instance.packages.packages["selinon"]
        assert set(package_version.to_dict().pop("extras")) == {
            "celery",
            "mongodb",
            "postgresql",
            "redis",
            "s3",
            "sentry",
        }
        assert set(package_version.extras) == {"celery", "mongodb", "postgresql", "redis", "s3", "sentry"}


class TestPipfileLock(PythonTestCase):

    @pytest.mark.parametrize("pipfile_lock", [
        'Pipfile_test1.lock',
    ])
    def test_from_string(self, pipfile_lock: str):
        with open(os.path.join(self.data_dir, 'pipfiles', pipfile_lock), 'r') as pipfile_lock_file:
            content = pipfile_lock_file.read()

        with open(os.path.join(self.data_dir, 'pipfiles', pipfile_lock[:-len('.lock')]), 'r') as pipfile_file:
            pipfile_content = pipfile_file.read()

        pipfile_instance = Pipfile.from_string(pipfile_content)
        instance = PipfileLock.from_string(content, pipfile=pipfile_instance)
        assert instance.to_string() == content

    def test_extras_parsing(self):
        pipfile_instance = Pipfile.from_file(os.path.join(self.data_dir, "pipfiles", "Pipfile_extras"))
        instance = PipfileLock.from_file(
            os.path.join(self.data_dir, "pipfiles", "Pipfile_extras.lock"),
            pipfile=pipfile_instance
        )

        assert instance is not None
        assert len(instance.packages.packages) == 34
        assert "selinon" in instance.packages.packages
        package_version = instance.packages.packages["selinon"]
        assert set(package_version.to_dict().pop("extras")) == {
            "celery",
            "mongodb",
            "postgresql",
            "redis",
            "s3",
            "sentry",
        }
        assert set(package_version.extras) == {"celery", "mongodb", "postgresql", "redis", "s3", "sentry"}
