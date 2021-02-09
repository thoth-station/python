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

"""Tests for module provenance."""

import os
from .base import PythonTestCase

import pytest

from thoth.python import Project


class TestProvenanceCheck(PythonTestCase):
    """Test ProvenanceCheck module."""

    def load_test_project(self, pinned_index: bool = False) -> Project:
        """Instantiate testing project from prepared testing Pipfile and Pipfile.lock files.

        @param pinned_index: true for retrieving Pipfile with pinned index
        """
        pipfile_path = os.path.join(
            self.data_dir,
            "pipfiles",
            "Pipfile_provenance1" if not pinned_index else "Pipfile_provenance2",
        )
        pipfile_lock_path = os.path.join(
            self.data_dir,
            "pipfiles",
            "Pipfile_provenance1.lock" if not pinned_index else "Pipfile_provenance2.lock",
        )
        return Project.from_files(pipfile_path, pipfile_lock_path)

    @pytest.mark.parametrize(
        "index_report",
        [
            {
                "https://index-aicoe.a3c1.starter-us-west-1.openshiftapps.com": [
                    {
                        "sha256": "5f6cf0a8ddf7eb8aea6f4c514427633698a684423673da8f44f6f0f303cce4a9",
                    },
                    {
                        "sha256": "74b72dd2a127da25b08dcbfabf6e495065c2a2309e415d0feac5d0e0d60fcb3e",
                    },
                ],
                "https://pypi.org/simple": [
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    },
                    {
                        "sha256": "8e52bf8079a48e2a53f3dfeec9e04addb900c101d1591c85df69cf677d3237e7",
                    },
                ],
            }
        ],
    )
    def test_different_artifacts_on_sources(self, index_report):
        """Test different artifacts on sources."""
        # Suggest to explicitly specify package source.
        project = self.load_test_project()
        package_version = project.pipfile_lock.packages.get("yaspin")
        report = project._check_scan(package_version, index_report=index_report)

        assert isinstance(report, list)
        assert len(report) == 1

        report = report[0]

        assert "type" in report
        assert "WARNING" == report["type"]

        assert "id" in report
        assert report["id"] == "DIFFERENT-ARTIFACTS-ON-SOURCES"

        assert "indexes" in report
        assert set(report["indexes"]) == {
            "https://index-aicoe.a3c1.starter-us-west-1.openshiftapps.com",
            "https://pypi.org/simple",
        }

    @pytest.mark.parametrize(
        "index_report",
        [
            {
                "foo": [
                    {
                        "sha256": "2222222222222222222222222222222222222222222222222222222222222222",
                    },
                    {
                        "sha256": "1111111111111111111111111111111111111111111111111111111111111111",
                    },
                ],
                "https://pypi.org/simple": [
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    },
                    {
                        "sha256": "8e52bf8079a48e2a53f3dfeec9e04addb900c101d1591c85df69cf677d3237e7",
                    },
                ],
                "https://index-aicoe.a3c1.starter-us-west-1.openshiftapps.com": [
                    {
                        "sha256": "5f6cf0a8ddf7eb8aea6f4c514427633698a684423673da8f44f6f0f303cce4a9",
                    },
                    {
                        "sha256": "74b72dd2a127da25b08dcbfabf6e495065c2a2309e415d0feac5d0e0d60fcb3e",
                    },
                ],
            }
        ],
    )
    def test_different_source_error(self, index_report):
        """Test different source error."""
        # Error that the given artifact is installed from different source.
        project = self.load_test_project(pinned_index=True)
        package_version = project.pipfile_lock.packages.get("yaspin")
        report = project._check_scan(package_version, index_report=index_report)

        assert isinstance(report, list)
        assert len(report) == 1

        report = report[0]

        assert "type" in report
        assert "ERROR" in report["type"]

        assert "id" in report
        assert "ARTIFACT-DIFFERENT-SOURCE" == report["id"]

        assert "indexes" in report
        assert ["https://pypi.org/simple"] == report["indexes"]

        assert "sources" in report
        assert list(report["sources"].keys()) == ["https://pypi.org/simple"]

    @pytest.mark.parametrize(
        "index_report",
        [
            {
                "https://index-aicoe.a3c1.starter-us-west-1.openshiftapps.com": [
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    },
                    {
                        "sha256": "8e52bf8079a48e2a53f3dfeec9e04addb900c101d1591c85df69cf677d3237e7",
                    },
                ],
                "https://pypi.org/simple": [
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    }
                ],
            }
        ],
    )
    def test_possible_different_source_info(self, index_report):
        """Test possible different source info."""
        # Warning that the given artifact can installed from different source.
        project = self.load_test_project(pinned_index=True)
        package_version = project.pipfile_lock.packages.get("yaspin")
        report = project._check_scan(package_version, index_report=index_report)

        assert isinstance(report, list)
        assert len(report) == 1

        report = report[0]

        assert "type" in report
        assert "INFO" == report["type"]

        assert "id" in report
        assert "ARTIFACT-POSSIBLE-DIFFERENT-SOURCE" == report["id"]

        assert "indexes" in report
        assert ["https://pypi.org/simple"] == report["indexes"]

        assert "sources" in report
        assert list(report["sources"].keys()) == ["https://pypi.org/simple"]

    @pytest.mark.parametrize(
        "index_report",
        [
            {
                "https://pypi.org/simple": [
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    },
                    {
                        "sha256": "8e52bf8079a48e2a53f3dfeec9e04addb900c101d1591c85df69cf677d3237e7",
                    },
                ]
            }
        ],
    )
    def test_missing_package_error(self, index_report):
        """Test missing package error."""
        # Error missing package on index.
        project = self.load_test_project(pinned_index=True)
        package_version = project.pipfile_lock.packages.get("yaspin")
        report = project._check_scan(package_version, index_report=index_report)

        assert isinstance(report, list)
        assert len(report) == 1

        report = report[0]

        assert "type" in report
        assert "ERROR" == report["type"]

        assert "id" in report
        assert "MISSING-PACKAGE" == report["id"]

    @pytest.mark.parametrize(
        "index_report",
        [
            {
                "https://pypi.org/simple": [
                    {
                        "sha256": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    },
                    {
                        "sha256": "36fdccc5e0637b5baa8892fe2c3d927782df7d504e9020f40eb2c1502518aa5a",
                    },
                ]
            }
        ],
    )
    def test_invalid_artifact_hash_error(self, index_report):
        """Test invalid artifact hash error."""
        # Error that the given hash was not found on index.
        project = self.load_test_project()
        package_version = project.pipfile_lock.packages.get("yaspin")
        report = project._check_scan(package_version, index_report=index_report)

        assert isinstance(report, list)
        assert len(report) == 1

        report = report[0]

        assert "type" in report
        assert "ERROR" == report["type"]

        assert "id" in report
        assert "INVALID-ARTIFACT-HASH" == report["id"]

        assert report["digest"] == "8e52bf8079a48e2a53f3dfeec9e04addb900c101d1591c85df69cf677d3237e7"
