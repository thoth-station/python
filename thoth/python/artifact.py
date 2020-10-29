#!/usr/bin/env python3
# thoth-python
# Copyright(C) 2019, 2020 Kevin Postlthwait
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

"""Representation a python module and all the files within."""

import shutil
import logging
import requests
import tempfile
import zipfile
import tarfile
import hashlib
import os
from elftools.elf.elffile import ELFFile
from typing import Iterator, Tuple, Any
import attr

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Artifact:
    """Python artifacts are compressed modules."""

    artifact_name = attr.ib(type=str)
    artifact_url = attr.ib(type=str)
    compressed_file = attr.ib(type=str, default=None)
    dir_name = attr.ib(type=str, default=None)
    verify_ssl = attr.ib(type=bool, default=False)
    sha = attr.ib(type=str, default=None)

    def __attrs_post_init__(self):
        """Initialize sha after init."""
        self.sha = self._calculate_sha()

    def _download_if_necessary(self):
        if self.compressed_file is None:
            self._download_artifact()

    def _extract_if_necessary(self):
        self._download_if_necessary()
        if self.dir_name is None:
            self._extract_py_module()

    def _download_artifact(self) -> None:
        _LOGGER.debug("Downloading artifact from url %r", self.artifact_url)
        response = requests.get(self.artifact_url, verify=self.verify_ssl, stream=True)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as f:
            self.compressed_file = f.name
            f.write(response.content)

    def _extract_py_module(self) -> None:

        self._download_if_necessary()

        try:
            self.dir_name = tempfile.mkdtemp()
            try:
                if self.compressed_file.endswith(".tar.gz"):
                    tf = tarfile.open(self.compressed_file)
                    tf.extractall(self.dir_name)
                    _LOGGER.debug("Artifact is .tar.gz file")
                else:
                    ext = self.compressed_file.split(".")[-1]
                    with zipfile.ZipFile(self.compressed_file) as zip_ref:
                        zip_ref.extractall(self.dir_name)
                        _LOGGER.debug("Artifact is .%r file", ext)
            except Exception as e:
                _LOGGER.exception(f"Could not extract {self.compressed_file}: {str(e)}")
        except Exception as exc:
            _LOGGER.exception(f"Could not create temp dir: {str(exc)}")

    def _calculate_sha(self) -> str:
        """Calculate SHA256 of compressed file if not present in url."""
        url_parts = self.artifact_url.rsplit("#", maxsplit=1)
        if len(url_parts) == 2 and url_parts[1].startswith("sha256="):
            sha256 = url_parts[1][len("sha256=") :]
            _LOGGER.debug("Using SHA256 stated in URL: %r", url_parts[1])
            return sha256

        self._download_if_necessary()

        with open(self.compressed_file, "rb") as f:
            digest = hashlib.sha256()
            chunk = 1024
            while True:
                data = f.read(chunk)
                if data:
                    digest.update(data)
                else:
                    break

        hex_digest = digest.hexdigest()
        _LOGGER.debug("Computed artifact sha256 digest for %r: %s", self.artifact_url, digest)
        return hex_digest

    #                       VERSIONED SYMBOLS                                #
    def _elf_find_versioned_symbols(self, elf: ELFFile) -> Iterator[Tuple[str, str]]:
        """Take an ELFFile object and outputs the required dynamic symbols."""
        section = elf.get_section_by_name(".gnu.version_r")

        if section is not None:
            for verneed, verneed_iter in section.iter_versions():
                if verneed.name.startswith("ld-linux"):
                    continue
                for vernaux in verneed_iter:
                    yield verneed.name, vernaux.name

    def _is_elf(self, filename: str) -> bool:
        """Check if files magic numbers are <delete>ELF."""
        with open(filename, "rb") as f:
            return f.read(16).startswith(b"\x7f\x45\x4c\x46")

    def _get_versioned_symbols_from_file(self, result, filename: str):
        """Given a file get all required dynamic symbols if it's an executable."""
        with open(filename, "rb") as f:
            if not self._is_elf(filename):
                return
            elf = ELFFile(f)
            for lib, sym in self._elf_find_versioned_symbols(elf):
                if result.get(lib) is None:
                    result[lib] = set()
                result[lib].add(sym)

    def get_versioned_symbols(self) -> dict:
        """Walk dir and get all dynamic symbols required from all files."""
        self._extract_if_necessary()
        result = dict()  # type: Any
        for dir_name, _, file_list in os.walk(self.dir_name):
            for fname in file_list:
                self._get_versioned_symbols_from_file(result, os.path.join(dir_name, fname))

        for symbol in result:
            result[symbol] = list(result[symbol])

        return result

    #                          Package Digests                                          #
    def gather_hashes(self) -> list:
        """Calculate checksums and gather hashes of all file in the given artifact."""
        self._extract_if_necessary()

        digests = []
        for root, _, files in os.walk(self.dir_name):
            for file_ in files:
                filepath = os.path.join(root, file_)
                if os.path.isfile(filepath):
                    with open(filepath, "rb") as my_file:
                        digests.append(
                            {
                                "filepath": filepath[len(self.dir_name) + 1 :],
                                "sha256": hashlib.sha256(my_file.read()).hexdigest(),
                            }
                        )
        return digests

    def __del__(self):
        """Remove temporary file created by class."""
        try:
            if self.compressed_file.startswith("/tmp"):
                os.remove(self.compressed_file)
            shutil.rmtree(self.dir_name)
        except Exception:
            pass
