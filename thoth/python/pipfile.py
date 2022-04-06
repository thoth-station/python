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

"""Parse string representation of a Pipfile or Pipfile.lock and represent it in an object."""

import os
import json
import hashlib
import logging
from typing import Dict
from typing import Any
from typing import Optional
from typing import Iterable
from typing import List
from itertools import chain

import toml
import attr
from packaging.requirements import Requirement

from .exceptions import PipfileParseError
from .exceptions import InternalError
from .exceptions import SourceNotFoundError
from .packages import Packages
from .source import Source
from .package_version import PackageVersion


_LOGGER = logging.getLogger(__name__)

# The default Pipfile spec number (version) stated in the Pipfile.lock.
_DEFAULT_PIPFILE_SPEC = 6


@attr.s(slots=True)
class PipfileMeta:
    """Parse meta information stored in Pipfile or Pipfile.lock."""

    sources = attr.ib(type=Dict[str, Source])
    requires = attr.ib(type=Dict[str, Any], default=attr.Factory(dict))
    pipenv = attr.ib(type=Optional[Dict[str, Any]], default=None)
    hash = attr.ib(type=Optional[Dict[str, Any]], default=None)
    pipfile_spec = attr.ib(type=int, default=_DEFAULT_PIPFILE_SPEC)

    @classmethod
    def from_dict(cls, dict_: dict):
        """Parse sources from dict as stated in Pipfile/Pipfile.lock."""
        _LOGGER.debug("Parsing Pipfile/Pipfile.lock metadata section")
        dict_ = dict(dict_)

        if "sources" in dict_:
            # Naming is confusing here - Pipfile uses source, Pipfile.lock sources.
            dict_["source"] = dict_.pop("sources")

        if "source" not in dict_:
            dict_["source"] = []

        sources = {d["name"]: Source.from_dict(d) for d in dict_.pop("source")}
        requires = dict_.pop("requires", {})
        pipenv = dict_.pop("pipenv", None)
        pipfile_spec = dict_.pop("pipfile-spec", None)
        hash_ = dict_.pop("hash", None)

        if dict_:
            _LOGGER.warning("Metadata ignored in Pipfile or Pipfile.lock: %s", dict_)

        return cls(sources=sources, requires=requires, pipenv=pipenv, hash=hash_, pipfile_spec=pipfile_spec)

    def to_dict(self, is_lock: bool = False):
        """Produce sources as a dict representation as stated in Pipfile/Pipfile.lock."""
        _LOGGER.debug("Generating Pipfile%s metadata section", "" if not is_lock else ".lock")
        sources_dict = [source.to_dict() for source in self.sources.values()]

        result = {}  # type: Dict[str, Any]
        if is_lock:
            # Pipenv is omitted.
            result["sources"] = sources_dict
            result["requires"] = self.requires or {}
            result["hash"] = self.hash
            result["pipfile-spec"] = self.pipfile_spec or _DEFAULT_PIPFILE_SPEC
        else:
            result["source"] = sources_dict
            if self.pipenv:
                result["pipenv"] = self.pipenv

            if self.requires:
                result["requires"] = self.requires

        return result

    def set_hash(self, hash_: dict):
        """Set hash of Pipfile to make sure pipenv uses correct parts.."""
        self.hash = hash_

    def to_requirements_index_conf(self) -> str:
        """Add index configuration as would be stated in the requirements.txt file."""
        result = ""

        primary_index_added = False
        for source in self.sources.values():
            if not primary_index_added:
                result += f"-i {source.url}\n"
                primary_index_added = True
            else:
                result += f"--extra-index-url {source.url}\n"

        return result

    def get_sources_providing_package(self, package_name: str) -> list:
        """Get all source indexes providing the given package."""
        result = []
        for source in self.sources.values():
            if package_name in source.get_packages():
                result.append(source)

        return result

    def get_sources_providing_package_version(self, package_name: str, package_version: str) -> list:
        """Get all source indexes providing the given package in the specified value."""
        result = []
        for source in self.sources.values():
            if source.provides_package_version(package_name, package_version):
                result.append(source)

        return result

    def add_source(self, source: Source):
        """Add the given package source."""
        self.sources[source.name] = source

    def get_source_by_url(self, index_url) -> Source:
        """Get source registered by its index url."""
        for source in self.sources.values():
            if source.url == index_url:
                return source
        else:
            raise SourceNotFoundError(f"Package source with url {index_url} not found")


@attr.s(slots=True)
class _PipfileBase:
    """A base class encapsulating logic of Pipfile and Pipfile.lock."""

    packages = attr.ib(type=Packages)
    dev_packages = attr.ib(type=Packages)
    meta = attr.ib(type=PipfileMeta)

    # I wanted to reuse pipenv implementation, but the implementation is not that reusable. Also, we would like
    # to have support of different pipenv files so we will need to distinguish implementation details on our own.

    @classmethod
    def from_requirements(cls, requirements_content: str):
        raise NotImplementedError

    @classmethod
    def from_string(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def parse(cls, *args, **kwargs):
        """Try to parse provided Pipfile{,.lock} content.

        Try to determine whether Pipfile{,.lock} or raw requirements were used.
        """
        try:
            return cls.from_string(*args, **kwargs)
        except PipfileParseError:
            # Fallback to raw requirements parsing.
            return cls.from_requirements(*args, **kwargs)

    def to_requirements_file(self, develop: bool = False) -> str:
        """Convert the current requirement specification to a string that is in compliance with requirements.txt."""
        # First add index configuration.
        requirements_file = self.meta.to_requirements_index_conf()

        for package_version in self.packages.packages.values() if not develop else self.dev_packages.packages.values():
            if package_version.version and package_version.version != "*":
                requirements_file += f"{package_version.name}{package_version.version}\n"
            else:
                requirements_file += f"{package_version.name}\n"

        return requirements_file

    def add_package_version(self, package_version: PackageVersion):
        """Add the given package."""
        if package_version.develop:
            self.dev_packages.add_package_version(package_version)
        else:
            self.packages.add_package_version(package_version)

    def sanitize_source_indexes(self):
        """Make sure all indexes used by packages are registerd in meta."""
        _LOGGER.debug("Checking source indexes used")

        def _index_check(package_version: PackageVersion, source: Source):
            if source is package_version.index or package_version.index is None:
                return

            if source.name == package_version.index.name and source.url != package_version.index.url:
                raise InternalError(
                    f"Found package source index {source} with different name but same URL "
                    f"as for package {package_version.name} in "
                    f"version {package_version.version}: {package_version.index}"
                )
            elif source.name == package_version.index.name and source.verify_ssl != package_version.index.verify_ssl:
                raise InternalError(
                    f"Found package source index {source} with different SSL verification settings "
                    f"but same URL as for package {package_version.name} in "
                    f"version {package_version.version}: {package_version.index}"
                )

        for package_version in chain(self.packages.packages.values(), self.dev_packages.packages.values()):
            if not package_version.index:
                continue

            if package_version.index.name not in self.meta.sources:
                for source in self.meta.sources.values():
                    _index_check(package_version, source)
                self.meta.sources[package_version.index.name] = package_version.index
            else:
                _index_check(package_version, self.meta.sources[package_version.index.name])

    @staticmethod
    def _construct_requirements_packages(packages: Iterable[PackageVersion]) -> str:
        """Construct a requirements.txt/in string entry for each package."""
        result = ""

        for package in packages:
            result += package.name
            if package.extras:
                result += f"[{','.join(e for e in sorted(package.extras))}]"  # type: ignore
            if package.version and package.version != "*":
                result += package.version

            if package.markers:
                result += "; " + package.markers

            if package.hashes:
                result += " \\\n"
                for idx, digest in enumerate(package.hashes):
                    result += f"    --hash={digest}"
                    if idx != len(package.hashes) - 1:
                        result += " \\\n"
                    else:
                        result += "\n"
            else:
                result += "\n"

        return result

    @classmethod
    def _construct_requirements(
        cls,
        packages: Iterable[PackageVersion],
        dev_packages: Optional[Iterable[PackageVersion]],
        meta: PipfileMeta,
        with_header: bool = True,
    ) -> str:
        result = ""
        if with_header:
            result = """#
# This file is autogenerated by Thoth and is meant to be used with pip-compile
# as provided by pip-tools.
#
"""

        for idx, index in enumerate(meta.sources.values()):
            if idx == 0:
                result += f"--index-url {index.url}\n"
            else:
                result += f"--extra-index-url {index.url}\n"

        result += "\n"
        result += cls._construct_requirements_packages(packages)

        if dev_packages:
            result += "\n#\n# dev packages\n#\n"
            result += cls._construct_requirements_packages(dev_packages)

        return result

    def construct_requirements_txt(self) -> str:
        """Construct requirements.txt file."""
        return self._construct_requirements(
            self.packages.packages.values(),
            self.dev_packages.packages.values(),
            self.meta,
        )


@attr.s(slots=True)
class ThothPipfileSection:
    """Thoth specific section in Pipfile."""

    allow_prereleases = attr.ib(type=Dict[str, bool], default=attr.Factory(dict))
    disable_index_adjustment = attr.ib(type=bool, default=False)

    def to_dict(self, keep_defaults: bool = False) -> Dict[str, Any]:
        """Get a dict representation of Thoth specific section in Pipfile."""
        result = attr.asdict(self)

        # Keep the Thoth section minimal.
        if not keep_defaults and not result["allow_prereleases"]:
            result.pop("allow_prereleases")

        if not keep_defaults and not result["disable_index_adjustment"]:
            result.pop("disable_index_adjustment")

        return result

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "ThothPipfileSection":
        """Convert Thoth specific section in Pipfile to a dictionary representation."""
        dict_ = dict(dict_)
        allow_prereleases = dict_.pop("allow_prereleases", None) or {}
        disable_index_adjustment = dict_.pop("disable_index_adjustment", False)

        if dict_:
            _LOGGER.warning("Unknown entry in Thoth specific Pipfile section: %r", dict_)

        if not isinstance(allow_prereleases, dict):
            _LOGGER.warning(
                "allow_prereleases expected to be a dictionary, but got %r instead - ignoring", type(allow_prereleases)
            )
            allow_prereleases = {}
        if not isinstance(disable_index_adjustment, bool):
            _LOGGER.warning(
                "disable_index_adjustment expected to be a boolean, but got %r instead - ignoring",
                type(disable_index_adjustment),
            )
            disable_index_adjustment = False

        for k, v in list(allow_prereleases.items()):
            if not isinstance(k, str) or not k:
                _LOGGER.warning("allow_prereleases expects package names, but got %r - ignoring", k)
                allow_prereleases.pop(k)
                continue
            if not isinstance(v, bool):
                _LOGGER.warning("allow_prereleases expects a boolean flag for package %r but got %r - ignoring", k, v)
                allow_prereleases.pop(k)
                continue

        return cls(allow_prereleases=allow_prereleases, disable_index_adjustment=disable_index_adjustment)


@attr.s(slots=True)
class Pipfile(_PipfileBase):
    """A Pipfile representation - representation of direct dependencies of an application."""

    thoth = attr.ib(type=ThothPipfileSection, default=attr.Factory(ThothPipfileSection))

    @property
    def data(self):
        """Return data used to compute hash based on Pipfile stored in Pipfile.lock."""
        meta = self.meta.to_dict(is_lock=True)
        # Only these values are used to compute digest.
        meta = {"requires": meta["requires"], "sources": meta["sources"]}
        return {"default": self.packages.to_pipfile(), "develop": self.dev_packages.to_pipfile(), "_meta": meta}

    @classmethod
    def from_package_versions(cls, packages: List[PackageVersion], meta: PipfileMeta = None) -> "Pipfile":
        """Construct Pipfile from provided PackageVersion instances."""
        return cls(
            packages=Packages.from_package_versions([pv for pv in packages if not pv.develop], develop=False),
            dev_packages=Packages.from_package_versions([pv for pv in packages if pv.develop], develop=True),
            meta=meta or PipfileMeta.from_dict({}),
        )

    @classmethod
    def from_file(cls, file_path: Optional[str] = None) -> "Pipfile":
        """Parse Pipfile file and return its Pipfile representation."""
        if file_path and os.path.isdir(file_path):
            file_path = os.path.join(file_path, "Pipfile")

        file_path = file_path or "Pipfile"

        _LOGGER.debug("Loading Pipfile from %r", file_path)
        with open(file_path, "r") as pipfile_file:
            return cls.from_string(pipfile_file.read())

    @classmethod
    def from_string(cls, pipfile_content: str) -> "Pipfile":  # type: ignore
        """Parse Pipfile from its string representation."""
        _LOGGER.debug("Parsing Pipfile toml representation from string")
        try:
            parsed = toml.loads(pipfile_content)
        except Exception as exc:  # noqa: F841
            # We are transparent - Pipfile can be eigher TOML or JSON - try to parse any of these.
            try:
                parsed = json.loads(pipfile_content)
            except Exception as exc:
                raise PipfileParseError("Failed to parse provided Pipfile") from exc

        return cls.from_dict(parsed)

    @classmethod
    def from_dict(cls, dict_) -> "Pipfile":
        """Retrieve instance of Pipfile from its dictionary representation."""
        _LOGGER.debug("Parsing Pipfile")
        dict_ = dict(dict_)
        packages = dict_.pop("packages", {})
        dev_packages = dict_.pop("dev-packages", {})
        thoth_section = ThothPipfileSection.from_dict(dict_.pop("thoth", {}))

        # Use remaining parts - such as requires, pipenv configuration and other flags.
        meta = PipfileMeta.from_dict(dict_)
        return cls(
            packages=Packages.from_pipfile(packages, develop=False, meta=meta),
            dev_packages=Packages.from_pipfile(dev_packages, develop=True, meta=meta),
            meta=meta,
            thoth=thoth_section,
        )

    def to_dict(self, keep_thoth_section: bool = False) -> dict:
        """Return Pipfile representation as dict."""
        _LOGGER.debug("Generating Pipfile")
        result = {"packages": self.packages.to_pipfile(), "dev-packages": self.dev_packages.to_pipfile()}
        result.update(self.meta.to_dict())

        thoth_section = self.thoth.to_dict(keep_defaults=keep_thoth_section)
        if thoth_section:
            result["thoth"] = thoth_section

        return result

    def to_string(self, *, keep_thoth_section: bool = False) -> str:
        """Convert representation of Pipfile to actual Pipfile file content."""
        _LOGGER.debug("Converting Pipfile to toml")
        return toml.dumps(self.to_dict(keep_thoth_section=keep_thoth_section))

    def construct_requirements_in(self) -> str:
        """Construct requirements.in file for the current project."""
        return self._construct_requirements(
            self.packages.packages.values(),
            self.dev_packages.packages.values(),
            self.meta,
        )

    def to_file(self, *, path: str = "Pipfile", keep_thoth_section: bool = False) -> None:
        """Convert the current state of Pipfile to actual Pipfile file stored in CWD."""
        if os.path.isdir(path):
            path = os.path.join(path, "Pipfile")

        with open(path, "w") as pipfile:
            pipfile.write(self.to_string(keep_thoth_section=keep_thoth_section))

    def hash(self):
        """Compute hash of Pipfile."""
        # TODO: this can be implementation dependent on Pipfile version - we are simply reusing the current version.
        content = json.dumps(self.data, sort_keys=True, separators=(",", ":"))
        hexdigest = hashlib.sha256(content.encode("utf8")).hexdigest()
        _LOGGER.debug("Computed hash for %r: %r", content, hexdigest)
        return {"sha256": hexdigest}

    def add_requirement(
        self,
        requirement: str,
        *,
        is_dev: bool = False,
        index_url: Optional[str] = None,
        force: bool = False,
    ) -> None:
        """Parse and add a requirement to direct dependency listing."""
        parsed_requirement = Requirement(requirement)

        if parsed_requirement.url:
            raise NotImplementedError("Adding packages specified by URL or by using editables is not supported")

        source = None
        if index_url is not None:
            try:
                source = self.meta.get_source_by_url(index_url)
            except SourceNotFoundError:
                if not force:
                    raise

                source = Source(index_url)
                self.meta.add_source(source)

        if len(self.meta.sources) == 1:
            # Do not assign any source (even when provided explictly) if there is only one source to be
            # compatible with TOML output of Pipenv.
            source = None

        package_version = PackageVersion(
            name=parsed_requirement.name,
            version=str(parsed_requirement.specifier) or None,
            develop=is_dev,
            index=source,
            markers=str(parsed_requirement.marker) if parsed_requirement.marker else None,
            extras=list(parsed_requirement.extras),
        )
        packages = self.packages if not is_dev else self.dev_packages
        packages.add_package_version(package_version, force=force)


@attr.s(slots=True)
class PipfileLock(_PipfileBase):
    """A Pipfile.lock representation - representation of fully pinned down stack with info such as hashes."""

    pipfile = attr.ib(type=Optional[Pipfile])

    @classmethod
    def from_package_versions(
        cls, pipfile: Pipfile, packages: List[PackageVersion], meta: PipfileMeta = None
    ) -> "PipfileLock":
        """Construct Pipfile from provided PackageVersion instances."""
        return cls(
            pipfile=pipfile,
            packages=Packages.from_package_versions([pv for pv in packages if not pv.develop], develop=False),
            dev_packages=Packages.from_package_versions([pv for pv in packages if pv.develop], develop=True),
            meta=meta or PipfileMeta.from_dict({}),
        )

    @classmethod
    def from_file(cls, file_path: Optional[str] = None, pipfile: Optional[Pipfile] = None) -> "PipfileLock":
        """Parse Pipfile.lock file and return its PipfileLock representation."""
        if file_path and os.path.isdir(file_path):
            file_path = os.path.join(file_path, "Pipfile.lock")

        file_path = file_path or "Pipfile.lock"

        _LOGGER.debug("Loading Pipfile.lock from %r", file_path)
        with open(file_path, "r") as pipfile_file:
            return cls.from_string(pipfile_file.read(), pipfile)

    @classmethod
    def from_string(cls, pipfile_content: str, pipfile: Optional[Pipfile] = None) -> "PipfileLock":  # type: ignore
        """Parse Pipfile.lock from its string content."""
        _LOGGER.debug("Parsing Pipfile.lock JSON representation from string")
        try:
            parsed = json.loads(pipfile_content)
        except Exception as exc:
            raise PipfileParseError("Failed to parse provided Pipfile.lock") from exc

        return cls.from_dict(parsed, pipfile)

    @classmethod
    def from_dict(cls, dict_: dict, pipfile: Optional[Pipfile] = None) -> "PipfileLock":
        """Construct PipfileLock class from a parsed JSON representation as stated in actual Pipfile.lock."""
        _LOGGER.debug("Parsing Pipfile.lock")
        meta = PipfileMeta.from_dict(dict_["_meta"])
        return cls(
            meta=meta,
            packages=Packages.from_pipfile_lock(dict_["default"], develop=False, meta=meta),
            dev_packages=Packages.from_pipfile_lock(dict_["develop"], develop=True, meta=meta),
            pipfile=pipfile,
        )

    def to_string(self, pipfile: Optional[Pipfile] = None) -> str:
        """Convert the current state of PipfileLock to its Pipfile.lock file representation."""
        _LOGGER.debug("Converting Pipfile.lock to JSON")
        return json.dumps(self.to_dict(pipfile), sort_keys=True, indent=4) + "\n"

    def to_file(self, *, path: str = "Pipfile.lock", pipfile: Optional[Pipfile] = None) -> None:
        """Convert the current state of PipfileLock to actual Pipfile.lock file stored in CWD."""
        if os.path.isdir(path):
            path = os.path.join(path, "Pipfile.lock")

        with open(path, "w") as pipfile_lock:
            pipfile_lock.write(self.to_string(pipfile))

    def to_dict(self, pipfile: Pipfile = None) -> dict:
        """Create a dict representation of Pipfile.lock content."""
        _LOGGER.debug("Generating Pipfile.lock")
        pipfile = pipfile or self.pipfile

        if not pipfile:
            raise InternalError("Pipfile has to be provided when generating Pipfile.lock to compute SHA hashes")

        if self.meta.hash is None:
            self.meta.set_hash(pipfile.hash())

        self.sanitize_source_indexes()

        content = {
            "_meta": self.meta.to_dict(is_lock=True),
            "default": self.packages.to_pipfile_lock(),
            "develop": self.dev_packages.to_pipfile_lock(),
        }
        return content
