
## Release 0.17.0 (2023-01-13T20:17:43)
* f656e65 Iterate over each artifacts instead of capturing in a list (#486)
* 1c03db4 Remove pipfile-requirements from thoth.yaml and updated OWNERS (#493)
* 4a55e80 Limit packaging to <22 (#489)
* 145f030 Convert to full pyproject.toml + Pipfile and get rid of requirements.txt (#491)
* 10fd504 git ls-files -z -- .pre-commit-config.yaml | xargs -0 sed -i 's#https://gitlab.com/PyCQA/flake8#https://github.com/PyCQA/flake8#' (#485)
* 3ed4736 :recycle: HouseKeeping: Updated pre-commit and OWNERS

## Release 0.16.11 (2022-10-20T06:35:02)
* 4d2790a Catch the 403 from the index which are forbidden
* 00b5794 Remove GitHub issue templates
* fb5704f Remove CODEOWNERS
* 9fca997 Enable TLS for Thoth

## Release 0.16.10 (2022-04-06T08:43:35)
* 242cf8a Overwrite supplied hash only if no hash was provided
* 4a263b9 Add myself as an approver and remove .thoth.yaml maintainers
* ac6463b Update pre-commit configuration
* 56ff988 use thoth-advise manager instead of update manager
* 557cc45 Remove redeliver container image template
* a4d24f1 Add template for delivering missing module
* 2c18f48 Release of version 0.16.9
* 570c5ca Fix constructing artifact url
* a158360 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 8fce5f4 Add parentheses
* 1e2a28a Fix typo in error message
* f008b0e Release of version 0.16.8
* ca3b50e Fix artifact obtaining on the Pulp instance
* a56e5b9 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* b0ccaeb Release of version 0.16.7
* 6479ee3 Add myself to maintainers
* 1439fd4 Add myself to approvers
* de92504 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 1378992 Strip any terminating slashes from index URL
* d900370 Check lockfile hash on provenance checks
* 1491401 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 54da255 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 2451b88 Update pyproject.toml to use Python 3.8
* 23be37c :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 5809a20 add kebechet to crossroads in docs
* ce63c47 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 72c35fb Release of version 0.16.6
* 0fe5765 Perform shallow copy when parsing Pipfile package entry
* 154eb03 :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 5984da9 Release of version 0.16.5
* 20d7425 Add tests for decoded artifact for package versions
* ad3d0cf :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* 1ff7b68 Add unquote to aiosource also
* 7213ce1 Release of version 0.16.4
* 37c3736 replace string with correct symbol
* cf5a1fa :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* ba33f9c Release of version 0.16.3
* a00dfda change sleep to 0 because it still gives up core
* 0caaf39 Properly handle not found exception on async source requests
* 0843213 Describe where files are looked up on an error
* 229ed07 :arrow_up: Automatic update of dependencies by Kebechet
* 858558f Fix typo
* 8663845 :arrow_up: Automatic update of dependencies by Kebechet (#404)
* d2efe79 Release of version 0.16.2
* 01ec7a7 make pre-commit happy
* e516381 Make optional parameters optional
* b6f6cdf :arrow_up: Automatic update of dependencies by Kebechet
* ca0b8fe :arrow_up: Automatic update of dependencies by Kebechet (#398)
* 1e982d3 :hatched_chick: update the prow resource limits (#397)
* 230b3bc Add note about constraints.txt to the README file (#396)
* 562ba37 Release of version 0.16.1 (#395)
* 1f214b1 Instantiate Pipfile instance just once (#393)
* 02010d1 Release of version 0.16.0 (#392)
* a90d7fa :arrow_up: Automatic update of dependencies by Kebechet (#390)
* df348d3 Add support for constraints (#389)
* af638bd Release of version 0.15.6 (#388)
* 46b55c5 Fix serialization of packages without version specifier (#386)
* 0f844ee :arrow_up: Automatic update of dependencies by Kebechet (#385)
* a0490f0 :arrow_up: Automatic update of dependencies by Kebechet (#383)
* c2d5fbd :arrow_up: Automatic update of dependencies by Kebechet (#380)
* cb64586 add prow check with specific args (#378)
* c39dbca Release of version 0.15.5
* 0b8401b Make pre-commit happy
* c184047 Optionally keep Thoth section when generating project
* 1fc65f9 Update OWNERS
* 03dcb3e :sparkles: let's run pre-commit
* 163d403 Add missing Kebechet templates
* 581a4e8 Release of version 0.15.4
* 86d327d Fix loading Pipfile files when requirements are used
* d7a6863 Revert "Fix serialization and loading of requirements files"
* c19edae :arrow_up: Automatic update of dependencies by Kebechet (#365)
* 8f12322 Adjust test checking for any version
* 7c93a7c Version identifier should be always non-None value
* 1512b78 Release of version 0.15.3
* 4ad7d76 Copy dict before performing pop
* f38a266 Release of version 0.15.2
* 6a30a43 :arrow_up: Automatic update of dependencies by Kebechet
* 2cb7db7 pre-releases do not need to be always stated in Pipfile
* cc68694 Release of version 0.15.1
* 4436661 Do not serialize allow_prereleases if not configured so
* f1c7196 Override entries in Thoth section if they do not meet type expected
* e59f303 Do not serialize empty dict in TOML in Pipfile
* 6db7bc5 Fix serialization and loading of requirements files
* c59c922 Release of version 0.15.0
* 3fd0672 Optionally keep thoth specific configuration in Pipfile
* f7dc066 Add routines to support adding packages to Pipfile
* 71e32f0 Release of version 0.14.0 (#352)
* af64372 Introduce disable index adjustment in Thoth's section in Pipfile (#349)
* 26a7fce Release of version 0.13.0 (#348)
* db708ae Fix signature and make sure factory for default is called (#346)
* ed57557 Fix signature to correctly describe return type (#345)
* a2c4f64 Introduce supported version properties (#343)
* e8dc8a4 Register pytest markers
* 9192908 pep561 for type checking (#333)
* 2efdb19 Raise an error if editable installs are used (#341)
* c4d4af4 Release of version 0.12.0 (#340)
* cb8c9c8 :arrow_up: Automatic update of dependencies by Kebechet (#339)
* 9772324 :arrow_up: Automatic update of dependencies by Kebechet
* 587c9ea Fix typing
* 6f9d220 Add tests related to Thoth section of Pipfile
* 3d19473 Introduce Thoth section in Pipfile
* 4e7f406 Reformat setup.py to fix pre-commit complains
* 396dacc removed bissenbay, thanks for your contributions!
* 158e212 Release of version 0.11.0 (#331)
* ee0e7ab Fix testsuite for Python 3.8 (#328)
* 3547efb Adjust how source name is derived (#325)
* 6cabdf8 :arrow_up: Automatic update of dependencies by kebechet. (#324)
* f30ee2a Add missing GitHub templates
* 7262bdb Relock to fix typing extension marker issue
* aa0606d bump python version (#322)
* 275c669 :pushpin: Automatic update of dependency aiohttp from 3.6.2 to 3.7.2 (#321)
* 9f3ca59 :pushpin: Automatic update of dependency aiohttp from 3.6.2 to 3.7.2 (#318)
* 47e610e :pushpin: Automatic update of dependency pyelftools from 0.26 to 0.27 (#317)
* 1202658 :pushpin: Automatic update of dependency lxml from 4.5.2 to 4.6.1 (#316)
* 67b8d96 :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.2 (#315)
* ce5e0da :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.2 (#319)
* 953a965 make pre-commit happy (#314)
* 0de4a1c Release of version 0.10.2 (#313)
* da33ebf :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#311)
* 1309c60 :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#310)
* 021af13 :pushpin: Automatic update of dependency attrs from 19.3.0 to 20.2.0 (#309)
* 118a920 :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.20.0 (#308)
* 9c4bdd1 :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#306)
* 460f296 fix package-version equality (#305)
* 3d8b209 Add maintainers (#304)
* 965bb8e Release of version 0.10.1 (#303)
* bcf0153 Adjust docstring (#299)
* 0e7fd99 :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.1 (#298)
* 18d65e4 Feature/ordered versions (#293)
* 6eca3e6 :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#295)
* 79c8e52 :arrow_down: removed the files as they are no longer required
* fc98d12 Replace legacy urls (#286)
* 35cb416 :pushpin: Automatic update of dependency lxml from 4.5.1 to 4.5.2 (#289)
* da14b8e :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#290)
* f979892 :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.2 (#288)
* 33bc1b5 add more functions to aiosource (#287)
* 8e5effa Add .thoth_last_analysis_id to .gitignore (#282)
* 80ba8fa :pushpin: Automatic update of dependency pytest-asyncio from 0.12.0 to 0.14.0 (#285)
* 681ea30 :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.13 (#284)
* 311ecf6 :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0 (#283)
* 637d998 Increase pytest timeout
* c084d3c Update OWNERS
* 57b83ed :pushpin: Automatic update of dependency pytest-timeout from 1.3.4 to 1.4.1
* a44eed6 Release of version 0.10.0
* e4f2b61 :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* 3a9ca03 strip trailing z
* 8e006c4 Use thoth-python errors
* 9192873 use existing warehouse function
* 0b76664 add doc string to release date
* da3c3fa get time of release
* 539c7a0 get time from warehouse
* 3d4c6ed Update stack to fix CI failure
* fb52eed Cache properties of PackageVersion
* 1da5ebe added a 'tekton trigger tag_release pipeline issue'
* 54c8205 :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* e2a2eba :pushpin: Automatic update of dependency click from 7.1.1 to 7.1.2
* 4efc8a9 :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* 5db9757 :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* 252d542 :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* 0469f3a :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* 2cba5c7 :pushpin: Automatic update of dependency pytest-asyncio from 0.10.0 to 0.11.0
* acc76b1 Be explicit about errors
* ddd8ddf Release of version 0.9.2
* 65a12de Change exception expected in the tests
* ca4ef34 Raise on failed requirements.{txt,in} load
* 5266d3d Raise an exception if a file failed to load
* 0ce317a :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* 2cbd335 :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* 81492b6 :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* bc8e705 :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* 0999ebc Use RHEL 8
* 4c40802 Remove typeshed from requirements
* ceadcec :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* 553ab46 :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* 328360f :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* ceecc39 :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* dcbd4b4 When checking if version exists when querying the DB the same package often shows up consecutively
* 0a3215d :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* 544a422 :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* 6cd7e7d Add templates for releases
* 96a9479 Update .thoth.yaml
* b4b9f63 :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* 54ca4d1 :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* 14b0b85 :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* a731027 :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* 46bb18a :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* 65fcc05 :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* 1f8c638 Add change to the other TODO
* 7701c75 Update test to omit pre-releases
* ecc02a6 :pushpin: Automatic update of dependency lxml from 4.4.3 to 4.5.0
* f079323 :pushpin: Automatic update of dependency lxml from 4.4.2 to 4.4.3
* daaef49 :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* fe4594e for-break-else loop
* aed7372 break if ending is found
* 38656da Fix if version is prefix to another version
* 0592f4a :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* 7c52d1b :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* 7833d6a :pushpin: Automatic update of dependency packaging from 20.0 to 20.1
* 74843ad :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* 9fc47c5 :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* 20033e8 :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* 5ba0cf7 :pushpin: Automatic update of dependency thoth-common from 0.9.27 to 0.9.28
* 4c95bea :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.27
* d759851 :pushpin: Automatic update of dependency thoth-analyzer from 0.1.7 to 0.1.8
* a5282ce :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* 2cd80f9 :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* 3be0bba :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24
* 6211dd7 Release of version 0.9.1
* 40d496d Fix sources dict handling
* a7f1e6e Release of version 0.9.0
* 68e11ec Move package parsing logic from thoth-solver
* b5e6bd1 :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* 7050771 Pass pip allows one --index-url per run
* 1782c40 Release of version 0.8.0
* 0273af6 Add pip/pip-tools support
* 422e3a0 Run the testsuite
* d0251d4 :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* ede452c :pushpin: Automatic update of dependency packaging from 19.2 to 20.0
* 69f1490 Happy new year!
* a39da77 :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* e53ef0b :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* 974974a :pushpin: Automatic update of dependency thoth-analyzer from 0.1.6 to 0.1.7
* 652fa72 Add Thamos documentation
* 5fc064a Point documentation to other libraries
* 207a302 Add Google Analytics
* d93f7b9 :pushpin: Automatic update of dependency pyelftools from 0.25 to 0.26
* 85fd4fb :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.21
* 4610f8e :pushpin: Automatic update of dependency thoth-analyzer from 0.1.5 to 0.1.6
* f0bbad0 Ignore Sphinx documentation configuration in Coala
* 63a0b1a Change Sphinx theme
* 69ade86 :pushpin: Automatic update of dependency thoth-common from 0.9.18 to 0.9.19
* 281972f :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.18
* 2747dc7 :pushpin: Automatic update of dependency thoth-analyzer from 0.1.4 to 0.1.5
* 965c1bb :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* 9f3ad03 :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* 7d0a3a6 :pushpin: Automatic update of dependency lxml from 4.4.1 to 4.4.2
* ea39b25 :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* 2acddd9 :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* b896eb0 :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* e305aaa :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* 9ccb1ab :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* 1ea42e1 Remove setuptools from Pipenv
* fc088de Release of version 0.7.1
* 5d2b52b Relock with new dependencies
* 4c1709b Remove last bits relying on semantic-version library
* 1d136fa Reflect code review comments
* 8a79a31 Fix testsuite respecting new implementation
* ee061db Use packaging module to be fully compliant with Python ecosystem
* e868fe9 Fix metadata propagation when instantiating PipfileLock
* 4ca6561 Add missing aiohttp dependency
* 62459b2 Normalize package name before checking its availability
* e8cba81 Introduce a method for checking if the given package is provided by index
* 664ab3c always use normalized package names
* 08f7fe2 re frido's comments on https://github.com/thoth-station/python/pull/160
* 813218b Normalized link text for comparison to package name
* 4d17416 bounced version
* e7f4a3f :sparkles: implemented a set of async methods
* ed2705c relocked
* 0899bb9 :sparkles: updated to our latest standards
* 8fdaeb6 Propagate metadata from constructed metadata in Pipfile
* 4596d39 Provide a way to define runtime environment when instantiating from package versions
* e1af864 Start using mypy for type checking
* 05d792e Drop version specification
* bc894ad Release of version 0.6.5
* 00692c6 Fix handling of user arguments when running pytest from setup.py
* 387f3af Add support for parsing extras from Pipfile and Pipfile.lock
* 888e322 Release of version 0.6.4
* 6d3e2e0 Adjust testsuite to use toml instead of contoml
* 2413dae Substitute contoml with toml
* 1c149ea Do not rely on pkg_resources, use packaging for version parsing
* 626148b Use packaging for package name normalization
* 37a54c7 Release of version 0.6.3
* 755965b Normalize Python package versions according to PEP-440
* e6f6bb6 :pushpin: Automatic update of dependency packaging from 19.1 to 19.2
* 064fe5a :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* 1c3520a :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* 0232b8e Release of version 0.6.2
* 8648824 Move testcase to its proper location
* 9a2fad6 Fix incosistent runtime environment attribute instantiation
* 1a04c30 fix symbols
* 09e5fa8 Fix Attribute Error
* 84c57f1 :pushpin: Automatic update of dependency semantic-version from 2.8.1 to 2.8.2
* fca4ddf :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* 0bcad44 :pushpin: Automatic update of dependency semantic-version from 2.8.0 to 2.8.1
* 5e6e158 :pushpin: Automatic update of dependency semantic-version from 2.7.1 to 2.8.0
* 585d574 :pushpin: Automatic update of dependency semantic-version from 2.7.0 to 2.7.1
* cc6d5c1 :pushpin: Automatic update of dependency semantic-version from 2.6.0 to 2.7.0
* ad43110 :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* 6bf9338 Fix temporary name assignment
* 788eb1e Add missing requirements
* c8c2204 :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* 3dfee17 Remove unused imports
* 6866404 :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* 0ec8b81 :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* 1b1a01d Release of version 0.6.1
* 356d7d6 Normalize Python package names according to PEP-0503
* bbc3f3f :pushpin: Automatic update of dependency lxml from 4.4.0 to 4.4.1
* 60907f9 Add missing runtime environment in dict reports of project
* f794c12 :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* b3174e3 Make results of tests agnostic to relative ordering
* f6faf7a Created function that returns list of artifacts
* 3e71064 Do not mock Artifact - test it instead
* 2ca2d6a Coala errors
* 5d663ba Addressed a few comments
* 8b5f6a0 Wheel symbols return now includes library
* e62ab05 changed testing whl&json files and some minor fixes
* 02cf6d7 Altered test and debugged
* 921c216 update
* f71999e Propogate verify_ssl
* 6405445 Fixed
* 5fd2f1a Fixed
* 547858b Variable name change and coala formatting
* 8cc7400 Added back get_hashes to pass test case
* ef4bae4 Created PythonArtifact class
* 294e9d5 Copy paste issue
* 617591d Install packaging
* 7649913 Changed based on review, refactored to only download once
* 9b64b1f :pushpin: Automatic update of dependency lxml from 4.3.5 to 4.4.0
* 9f540e5 :pushpin: Automatic update of dependency lxml from 4.3.4 to 4.3.5
* 238b79b Add typing
* 8d3e8bc Added pyelftools
* 4dca9d7 Added call in run func
* 339103a Download wheels
* b31ad51 Add code from my repo
* e99b2c4 Output filepath and sha256 for all files inside artifact
* 810f934 :pushpin: Automatic update of dependency thoth-common from 0.9.4 to 0.9.5
* 41325ca Release of version 0.6.0
* 87b8855 fix issue #20
* f8fc482 :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.4
* 2b7eb78 :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* ea29d83 :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* 1efc067 testing get_package_hashes() with_included_files
* 14d2775 :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* bb95390 :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* 58d53a5 :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* 66d3375 :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* 48bbdeb gathering hashes for .whl files
* 7fd1a36 :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* 55c4e4d :pushpin: Automatic update of dependency lxml from 4.3.3 to 4.3.4
* caaaa4a :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* bf91ea7 :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* 344bde6 :pushpin: Automatic update of dependency requests from 2.21.0 to 2.22.0
* 6138993 :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* 5e52c4f :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* de19972 :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* 0372117 Minor fix to display correct release in title of docs html
* ad6e94e :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* 25e8dff Add tests for parsing semver
* b2e550e A simple workaround to parse semver with leading zeros
* 1a9e9f3 :pushpin: Automatic update of dependency pytest from 4.4.0 to 4.4.1
* 6903e9a :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* e62c314 Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* 1a2d314 Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* b8cc336 Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* 6dc8e9d Automatic update of dependency pytest from 4.3.1 to 4.4.0
* 27f6365 Automatic update of dependency flexmock from 0.10.3 to 0.10.4
* 30cf33c Automatic update of dependency lxml from 4.3.2 to 4.3.3
* 994ae47 Propagate package name to debug message
* 5bf22e3 Release of version 0.5.0
* 8058d00 Rename dependency version to conform python package naming schema
* e08f15b Update dependencies
* 85bffce Add Thoth's configuration file
* e8f2e68 Use Sphinx for documentation
* 69dfb7e Ignore tests in coala
* 0f3abcd Make Coala happy
* 94ca95d Format with black
* b672b15 Provide runtime environment parameter
* 523f2de Minor fixes in implementation
* 737610d Use black for formating
* 9946fdf std coala config
* 6b367f7 added pytest jobs to all the pipes
* 11a1643 Requires are optional field in Pipfile
* 3161d7b Introduce configuration check method
* b6f69d3 Use black for formatting
* 9361d7c Minor fixes in implementation
* deaa37d It's already 2019
* a1c5e0b Remove unused imports
* 981697f Update .gitignore
* 915e42d Fix typo
* a47808e Improve packages gathering from indexes
* fde58b8 Version 0.4.6
* cf128e6 Avoid issues with bs4 when parsing simple API package listing
* a042d10 Release of version 0.4.5
* cf5d6b8 Make sure we use warehouse API only if it is available
* e8b5488 Version 0.4.4
* 057f33e Manipulate with core settings of a project
* 6602736 Create static method for semver parsing
* 2ee933b Add testsuite for provenance checks
* 5452693 Test creation of project from package versions
* b9c98c2 Release of version 0.4.3
* 0e68116 Introduce to_tuple_locked for locked packages
* 47f2f01 Release of version 0.4.2
* 8e8321d Make linter happy again
* df70c7b Automatic update of dependency pytest from 4.0.1 to 4.0.2
* e72db95 Introduce to_tuple method
* f9851e8 Version 0.4.1
* ae2d6f1 Minor fix for pipfile generation
* 1ac13eb Release of version 0.4.0
* 8b0bb77 Adjust report messages so that they are more generic
* faaf862 Use index url in reports rather than index name
* e20c8aa Be transparent about Pipfile's serialization type (JSON or TOML)
* eb38f55 Sanitize package source indexes before instantiation
* 7ee4b65 Sanitize package source indexes when deserializing
* 49a2956 Make default source name more differentiable
* 6eb009b Introduce digests fetcher abstraction for fetching package digests
* 9964fd8 Version 0.3.1
* 7fac418 Adjust README file
* 988856d Add testsuite to test thoth-python
* 946de3a Expose also PipfileMeta class
* f2a246b also managing releases to pypi now
* 54e278a adding standard thoth project configs
* 15abd65 Instantiate Project from strings
* 0fab6c0 Version 0.3.0
* ab97f43 Do not restrict click version
* 9a39bfb Version 0.2.0
* 4135a51 Do not forget requirements.txt
* 8ce290f Version 0.1.0
* 6b5fb63 Fix wrong imports
* eda4af0 Source code import
* c57ea01 Add long description for PyPI
* 3005ab0 Initial project import

## Release 0.16.9 (2022-02-24T17:10:01)
* Fix constructing artifact url
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* Add parentheses
* Fix typo in error message

## Release 0.16.8 (2022-02-14T14:42:58)
* Fix artifact obtaining on the Pulp instance
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.16.7 (2022-02-09T20:11:20)
* Add myself to maintainers
* Add myself to approvers
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* Strip any terminating slashes from index URL
* Check lockfile hash on provenance checks
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* Update pyproject.toml to use Python 3.8
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* add kebechet to crossroads in docs
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* Add tests for decoded artifact for package versions

## Release 0.16.6 (2021-11-09T10:01:56)
* Perform shallow copy when parsing Pipfile package entry
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.16.5 (2021-10-04T11:29:28)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment
* Add unquote to aiosource also

## Release 0.16.4 (2021-09-30T08:10:53)
### Features
* replace string with correct symbol
* :arrow_up: Automatic update of dependencies by Kebechet for the ubi8 environment

## Release 0.16.3 (2021-08-24T13:10:44)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet (#404)
### Bug Fixes
* Properly handle not found exception on async source requests
* Describe where files are looked up on an error
### Improvements
* change sleep to 0 because it still gives up core
* Fix typo

## Release 0.4.0 (2018-12-11T19:14:21)
* Adjust report messages so that they are more generic
* Use index url in reports rather than index name
* Be transparent about Pipfile's serialization type (JSON or TOML)
* Sanitize package source indexes before instantiation
* Sanitize package source indexes when deserializing
* Make default source name more differentiable
* Introduce digests fetcher abstraction for fetching package digests
* Version 0.3.1
* Adjust README file
* Add testsuite to test thoth-python
* Expose also PipfileMeta class
* also managing releases to pypi now
* adding standard thoth project configs
* Instantiate Project from strings
* Version 0.3.0
* Do not restrict click version
* Version 0.2.0
* Do not forget requirements.txt
* Version 0.1.0
* Fix wrong imports
* Source code import
* Add long description for PyPI
* Initial project import

## Release 0.4.2 (2018-12-17T14:16:16)
* Make linter happy again
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Introduce to_tuple method

## Release 0.4.3 (2018-12-17T16:03:54)
* Introduce to_tuple_locked for locked packages

## Release 0.4.5 (2019-01-02T12:35:14)
* Make sure we use warehouse API only if it is available
* Version 0.4.4
* Manipulate with core settings of a project
* Create static method for semver parsing
* Add testsuite for provenance checks
* Test creation of project from package versions
* Release of version 0.4.3
* Introduce to_tuple_locked for locked packages
* Release of version 0.4.2
* Make linter happy again
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Introduce to_tuple method
* Version 0.4.1
* Minor fix for pipfile generation
* Release of version 0.4.0
* Adjust report messages so that they are more generic
* Use index url in reports rather than index name
* Be transparent about Pipfile's serialization type (JSON or TOML)
* Sanitize package source indexes before instantiation
* Sanitize package source indexes when deserializing
* Make default source name more differentiable
* Introduce digests fetcher abstraction for fetching package digests
* Version 0.3.1
* Adjust README file
* Add testsuite to test thoth-python
* Expose also PipfileMeta class
* also managing releases to pypi now
* adding standard thoth project configs
* Instantiate Project from strings
* Version 0.3.0
* Do not restrict click version
* Version 0.2.0
* Do not forget requirements.txt
* Version 0.1.0
* Fix wrong imports
* Source code import
* Add long description for PyPI
* Initial project import

## Release 0.5.0 (2019-03-19T10:18:11)
* Rename dependency version to conform python package naming schema
* Update dependencies
* Add Thoth's configuration file
* Use Sphinx for documentation
* Ignore tests in coala
* Make Coala happy
* Format with black
* Provide runtime environment parameter
* Minor fixes in implementation
* Use black for formating
* std coala config
* added pytest jobs to all the pipes
* Requires are optional field in Pipfile
* Introduce configuration check method
* Use black for formatting
* Minor fixes in implementation
* It's already 2019
* Remove unused imports
* Update .gitignore
* Fix typo
* Improve packages gathering from indexes
* Version 0.4.6
* Avoid issues with bs4 when parsing simple API package listing
* Release of version 0.4.5
* Make sure we use warehouse API only if it is available
* Version 0.4.4
* Manipulate with core settings of a project
* Create static method for semver parsing
* Add testsuite for provenance checks
* Test creation of project from package versions
* Release of version 0.4.3
* Introduce to_tuple_locked for locked packages
* Release of version 0.4.2
* Make linter happy again
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Introduce to_tuple method
* Version 0.4.1
* Minor fix for pipfile generation
* Release of version 0.4.0
* Adjust report messages so that they are more generic
* Use index url in reports rather than index name
* Be transparent about Pipfile's serialization type (JSON or TOML)
* Sanitize package source indexes before instantiation
* Sanitize package source indexes when deserializing
* Make default source name more differentiable
* Introduce digests fetcher abstraction for fetching package digests
* Version 0.3.1
* Adjust README file
* Add testsuite to test thoth-python
* Expose also PipfileMeta class
* also managing releases to pypi now
* adding standard thoth project configs
* Instantiate Project from strings
* Version 0.3.0
* Do not restrict click version
* Version 0.2.0
* Do not forget requirements.txt
* Version 0.1.0
* Fix wrong imports
* Source code import
* Add long description for PyPI
* Initial project import

## Release 0.6.0 (2019-07-22T20:56:03)
* fix issue #20
* :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* testing get_package_hashes() with_included_files
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* gathering hashes for .whl files
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency lxml from 4.3.3 to 4.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency requests from 2.21.0 to 2.22.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* Minor fix to display correct release in title of docs html
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* Add tests for parsing semver
* A simple workaround to parse semver with leading zeros
* :pushpin: Automatic update of dependency pytest from 4.4.0 to 4.4.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* Automatic update of dependency pytest from 4.3.1 to 4.4.0
* Automatic update of dependency flexmock from 0.10.3 to 0.10.4
* Automatic update of dependency lxml from 4.3.2 to 4.3.3
* Propagate package name to debug message

## Release 0.6.1 (2019-08-12T14:54:10)
* Normalize Python package names according to PEP-0503
* :pushpin: Automatic update of dependency lxml from 4.4.0 to 4.4.1
* Add missing runtime environment in dict reports of project
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* :pushpin: Automatic update of dependency lxml from 4.3.5 to 4.4.0
* :pushpin: Automatic update of dependency lxml from 4.3.4 to 4.3.5
* Output filepath and sha256 for all files inside artifact
* :pushpin: Automatic update of dependency thoth-common from 0.9.4 to 0.9.5

## Release 0.6.2 (2019-09-17T09:48:53)
* Move testcase to its proper location
* Fix incosistent runtime environment attribute instantiation
* fix symbols
* Fix Attribute Error
* :pushpin: Automatic update of dependency semantic-version from 2.8.1 to 2.8.2
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency semantic-version from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency semantic-version from 2.7.1 to 2.8.0
* :pushpin: Automatic update of dependency semantic-version from 2.7.0 to 2.7.1
* :pushpin: Automatic update of dependency semantic-version from 2.6.0 to 2.7.0
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* Fix temporary name assignment
* Add missing requirements
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* Remove unused imports
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* Make results of tests agnostic to relative ordering
* Created function that returns list of artifacts
* Do not mock Artifact - test it instead
* Coala errors
* Addressed a few comments
* Wheel symbols return now includes library
* changed testing whl&json files and some minor fixes
* Altered test and debugged
* update
* Propogate verify_ssl
* Fixed
* Fixed
* Variable name change and coala formatting
* Added back get_hashes to pass test case
* Created PythonArtifact class
* Copy paste issue
* Install packaging
* Changed based on review, refactored to only download once
* Add typing
* Added pyelftools
* Added call in run func
* Download wheels
* Add code from my repo

## Release 0.6.3 (2019-09-23T09:17:38)
* Normalize Python package versions according to PEP-440
* :pushpin: Automatic update of dependency packaging from 19.1 to 19.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9

## Release 0.6.4 (2019-10-07T12:18:06)
* Adjust testsuite to use toml instead of contoml
* Substitute contoml with toml
* Do not rely on pkg_resources, use packaging for version parsing
* Use packaging for package name normalization

## Release 0.6.5 (2019-10-21T10:22:14)
* Fix handling of user arguments when running pytest from setup.py
* Add support for parsing extras from Pipfile and Pipfile.lock

## Release 0.7.1 (2019-11-08T10:09:30)
* Relock with new dependencies
* Remove last bits relying on semantic-version library
* Reflect code review comments
* Fix testsuite respecting new implementation
* Use packaging module to be fully compliant with Python ecosystem
* Fix metadata propagation when instantiating PipfileLock
* Add missing aiohttp dependency
* Normalize package name before checking its availability
* Introduce a method for checking if the given package is provided by index
* always use normalized package names
* re frido's comments on https://github.com/thoth-station/python/pull/160
* Normalized link text for comparison to package name
* bounced version
* :sparkles: implemented a set of async methods
* relocked
* :sparkles: updated to our latest standards
* Propagate metadata from constructed metadata in Pipfile
* Provide a way to define runtime environment when instantiating from package versions
* Start using mypy for type checking
* Drop version specification

## Release 0.8.0 (2020-01-07T13:20:08)
* Add pip/pip-tools support
* Run the testsuite
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.3 to 1.3.4
* :pushpin: Automatic update of dependency packaging from 19.2 to 20.0
* :pushpin: Automatic update of dependency pytest from 5.3.1 to 5.3.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.21 to 0.9.22
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.6 to 0.1.7
* Add Thamos documentation
* Point documentation to other libraries
* Add Google Analytics
* :pushpin: Automatic update of dependency pyelftools from 0.25 to 0.26
* :pushpin: Automatic update of dependency thoth-common from 0.9.19 to 0.9.21
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.5 to 0.1.6
* Ignore Sphinx documentation configuration in Coala
* Change Sphinx theme
* :pushpin: Automatic update of dependency thoth-common from 0.9.18 to 0.9.19
* :pushpin: Automatic update of dependency thoth-common from 0.9.17 to 0.9.18
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.4 to 0.1.5
* :pushpin: Automatic update of dependency thoth-common from 0.9.16 to 0.9.17
* :pushpin: Automatic update of dependency pytest from 5.3.0 to 5.3.1
* :pushpin: Automatic update of dependency lxml from 4.4.1 to 4.4.2
* :pushpin: Automatic update of dependency pytest from 5.2.4 to 5.3.0
* :pushpin: Automatic update of dependency pytest from 5.2.3 to 5.2.4
* :pushpin: Automatic update of dependency pytest from 5.2.2 to 5.2.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.15 to 0.9.16
* :pushpin: Automatic update of dependency thoth-common from 0.9.14 to 0.9.15
* Remove setuptools from Pipenv
* Release of version 0.7.1
* Relock with new dependencies
* Remove last bits relying on semantic-version library
* Reflect code review comments
* Fix testsuite respecting new implementation
* Use packaging module to be fully compliant with Python ecosystem
* Fix metadata propagation when instantiating PipfileLock
* Add missing aiohttp dependency
* Normalize package name before checking its availability
* Introduce a method for checking if the given package is provided by index
* always use normalized package names
* re frido's comments on https://github.com/thoth-station/python/pull/160
* Normalized link text for comparison to package name
* bounced version
* :sparkles: implemented a set of async methods
* relocked
* :sparkles: updated to our latest standards
* Propagate metadata from constructed metadata in Pipfile
* Provide a way to define runtime environment when instantiating from package versions
* Start using mypy for type checking
* Drop version specification
* Release of version 0.6.5
* Fix handling of user arguments when running pytest from setup.py
* Add support for parsing extras from Pipfile and Pipfile.lock
* Release of version 0.6.4
* Adjust testsuite to use toml instead of contoml
* Substitute contoml with toml
* Do not rely on pkg_resources, use packaging for version parsing
* Use packaging for package name normalization
* Release of version 0.6.3
* Normalize Python package versions according to PEP-440
* :pushpin: Automatic update of dependency packaging from 19.1 to 19.2
* :pushpin: Automatic update of dependency thoth-common from 0.9.9 to 0.9.10
* :pushpin: Automatic update of dependency thoth-common from 0.9.8 to 0.9.9
* Release of version 0.6.2
* Move testcase to its proper location
* Fix incosistent runtime environment attribute instantiation
* fix symbols
* Fix Attribute Error
* :pushpin: Automatic update of dependency semantic-version from 2.8.1 to 2.8.2
* :pushpin: Automatic update of dependency pytest from 5.1.1 to 5.1.2
* :pushpin: Automatic update of dependency semantic-version from 2.8.0 to 2.8.1
* :pushpin: Automatic update of dependency semantic-version from 2.7.1 to 2.8.0
* :pushpin: Automatic update of dependency semantic-version from 2.7.0 to 2.7.1
* :pushpin: Automatic update of dependency semantic-version from 2.6.0 to 2.7.0
* :pushpin: Automatic update of dependency pytest from 5.1.0 to 5.1.1
* Fix temporary name assignment
* Add missing requirements
* :pushpin: Automatic update of dependency pytest from 5.0.1 to 5.1.0
* Remove unused imports
* :pushpin: Automatic update of dependency thoth-common from 0.9.7 to 0.9.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.6 to 0.9.7
* Release of version 0.6.1
* Normalize Python package names according to PEP-0503
* :pushpin: Automatic update of dependency lxml from 4.4.0 to 4.4.1
* Add missing runtime environment in dict reports of project
* :pushpin: Automatic update of dependency thoth-common from 0.9.5 to 0.9.6
* Make results of tests agnostic to relative ordering
* Created function that returns list of artifacts
* Do not mock Artifact - test it instead
* Coala errors
* Addressed a few comments
* Wheel symbols return now includes library
* changed testing whl&json files and some minor fixes
* Altered test and debugged
* update
* Propogate verify_ssl
* Fixed
* Fixed
* Variable name change and coala formatting
* Added back get_hashes to pass test case
* Created PythonArtifact class
* Copy paste issue
* Install packaging
* Changed based on review, refactored to only download once
* :pushpin: Automatic update of dependency lxml from 4.3.5 to 4.4.0
* :pushpin: Automatic update of dependency lxml from 4.3.4 to 4.3.5
* Add typing
* Added pyelftools
* Added call in run func
* Download wheels
* Add code from my repo
* Output filepath and sha256 for all files inside artifact
* :pushpin: Automatic update of dependency thoth-common from 0.9.4 to 0.9.5
* Release of version 0.6.0
* fix issue #20
* :pushpin: Automatic update of dependency thoth-common from 0.9.3 to 0.9.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.2 to 0.9.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.1 to 0.9.2
* testing get_package_hashes() with_included_files
* :pushpin: Automatic update of dependency pytest from 5.0.0 to 5.0.1
* :pushpin: Automatic update of dependency pytest from 4.6.3 to 5.0.0
* :pushpin: Automatic update of dependency thoth-common from 0.9.0 to 0.9.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.11 to 0.9.0
* gathering hashes for .whl files
* :pushpin: Automatic update of dependency pytest from 4.6.2 to 4.6.3
* :pushpin: Automatic update of dependency lxml from 4.3.3 to 4.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.8.7 to 0.8.11
* :pushpin: Automatic update of dependency pytest from 4.5.0 to 4.6.2
* :pushpin: Automatic update of dependency requests from 2.21.0 to 2.22.0
* :pushpin: Automatic update of dependency thoth-common from 0.8.5 to 0.8.7
* :pushpin: Automatic update of dependency pytest from 4.4.2 to 4.5.0
* :pushpin: Automatic update of dependency pytest from 4.4.1 to 4.4.2
* Minor fix to display correct release in title of docs html
* :pushpin: Automatic update of dependency pytest-cov from 2.6.1 to 2.7.1
* Add tests for parsing semver
* A simple workaround to parse semver with leading zeros
* :pushpin: Automatic update of dependency pytest from 4.4.0 to 4.4.1
* :pushpin: Automatic update of dependency thoth-common from 0.8.4 to 0.8.5
* Automatic update of dependency thoth-common from 0.8.3 to 0.8.4
* Automatic update of dependency thoth-common from 0.8.2 to 0.8.3
* Automatic update of dependency thoth-common from 0.8.1 to 0.8.2
* Automatic update of dependency pytest from 4.3.1 to 4.4.0
* Automatic update of dependency flexmock from 0.10.3 to 0.10.4
* Automatic update of dependency lxml from 4.3.2 to 4.3.3
* Propagate package name to debug message
* Release of version 0.5.0
* Rename dependency version to conform python package naming schema
* Update dependencies
* Add Thoth's configuration file
* Use Sphinx for documentation
* Ignore tests in coala
* Make Coala happy
* Format with black
* Provide runtime environment parameter
* Minor fixes in implementation
* Use black for formating
* std coala config
* added pytest jobs to all the pipes
* Requires are optional field in Pipfile
* Introduce configuration check method
* Use black for formatting
* Minor fixes in implementation
* It's already 2019
* Remove unused imports
* Update .gitignore
* Fix typo
* Improve packages gathering from indexes
* Version 0.4.6
* Avoid issues with bs4 when parsing simple API package listing
* Release of version 0.4.5
* Make sure we use warehouse API only if it is available
* Version 0.4.4
* Manipulate with core settings of a project
* Create static method for semver parsing
* Add testsuite for provenance checks
* Test creation of project from package versions
* Release of version 0.4.3
* Introduce to_tuple_locked for locked packages
* Release of version 0.4.2
* Make linter happy again
* Automatic update of dependency pytest from 4.0.1 to 4.0.2
* Introduce to_tuple method
* Version 0.4.1
* Minor fix for pipfile generation
* Release of version 0.4.0
* Adjust report messages so that they are more generic
* Use index url in reports rather than index name
* Be transparent about Pipfile's serialization type (JSON or TOML)
* Sanitize package source indexes before instantiation
* Sanitize package source indexes when deserializing
* Make default source name more differentiable
* Introduce digests fetcher abstraction for fetching package digests
* Version 0.3.1
* Adjust README file
* Add testsuite to test thoth-python
* Expose also PipfileMeta class
* also managing releases to pypi now
* adding standard thoth project configs
* Instantiate Project from strings
* Version 0.3.0
* Do not restrict click version
* Version 0.2.0
* Do not forget requirements.txt
* Version 0.1.0
* Fix wrong imports
* Source code import
* Add long description for PyPI
* Initial project import

## Release 0.9.0 (2020-01-08T12:48:55)
* Move package parsing logic from thoth-solver
* :pushpin: Automatic update of dependency thoth-common from 0.9.22 to 0.9.23
* Pass pip allows one --index-url per run
* Happy new year!

## Release 0.9.1 (2020-01-09T08:38:14)
* Fix sources dict handling

## Release 0.9.2 (2020-04-20T13:04:30)
* Change exception expected in the tests
* Raise on failed requirements.{txt,in} load
* Raise an exception if a file failed to load
* :pushpin: Automatic update of dependency thoth-common from 0.12.8 to 0.12.9
* :pushpin: Automatic update of dependency thoth-common from 0.12.7 to 0.12.8
* :pushpin: Automatic update of dependency thoth-common from 0.12.6 to 0.12.7
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.0 to 0.6.1
* Use RHEL 8
* Remove typeshed from requirements
* :pushpin: Automatic update of dependency thoth-common from 0.10.8 to 0.10.9
* :pushpin: Automatic update of dependency thoth-common from 0.10.7 to 0.10.8
* :pushpin: Automatic update of dependency pytest-mypy from 0.4.2 to 0.5.0
* :pushpin: Automatic update of dependency requests from 2.22.0 to 2.23.0
* When checking if version exists when querying the DB the same package often shows up consecutively
* :pushpin: Automatic update of dependency thoth-common from 0.10.6 to 0.10.7
* :pushpin: Automatic update of dependency thoth-common from 0.10.5 to 0.10.6
* Add templates for releases
* Update .thoth.yaml
* :pushpin: Automatic update of dependency thoth-common from 0.10.4 to 0.10.5
* :pushpin: Automatic update of dependency thoth-common from 0.10.3 to 0.10.4
* :pushpin: Automatic update of dependency thoth-common from 0.10.2 to 0.10.3
* :pushpin: Automatic update of dependency thoth-common from 0.10.1 to 0.10.2
* :pushpin: Automatic update of dependency thoth-common from 0.10.0 to 0.10.1
* :pushpin: Automatic update of dependency pytest from 5.3.4 to 5.3.5
* Add change to the other TODO
* Update test to omit pre-releases
* :pushpin: Automatic update of dependency lxml from 4.4.3 to 4.5.0
* :pushpin: Automatic update of dependency lxml from 4.4.2 to 4.4.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.31 to 0.10.0
* for-break-else loop
* break if ending is found
* Fix if version is prefix to another version
* :pushpin: Automatic update of dependency thoth-common from 0.9.30 to 0.9.31
* :pushpin: Automatic update of dependency thoth-common from 0.9.29 to 0.9.30
* :pushpin: Automatic update of dependency packaging from 20.0 to 20.1
* :pushpin: Automatic update of dependency pytest from 5.3.3 to 5.3.4
* :pushpin: Automatic update of dependency thoth-common from 0.9.28 to 0.9.29
* :pushpin: Automatic update of dependency pytest from 5.3.2 to 5.3.3
* :pushpin: Automatic update of dependency thoth-common from 0.9.27 to 0.9.28
* :pushpin: Automatic update of dependency thoth-common from 0.9.26 to 0.9.27
* :pushpin: Automatic update of dependency thoth-analyzer from 0.1.7 to 0.1.8
* :pushpin: Automatic update of dependency thoth-common from 0.9.25 to 0.9.26
* :pushpin: Automatic update of dependency thoth-common from 0.9.24 to 0.9.25
* :pushpin: Automatic update of dependency thoth-common from 0.9.23 to 0.9.24

## Release 0.10.0 (2020-06-17T08:42:56)
* :pushpin: Automatic update of dependency pytest-cov from 2.9.0 to 2.10.0
* strip trailing z
* Use thoth-python errors
* use existing warehouse function
* add doc string to release date
* get time of release
* get time from warehouse
* Update stack to fix CI failure
* Cache properties of PackageVersion
* added a 'tekton trigger tag_release pipeline issue'
* :pushpin: Automatic update of dependency thoth-common from 0.13.1 to 0.13.2
* :pushpin: Automatic update of dependency click from 7.1.1 to 7.1.2
* :pushpin: Automatic update of dependency thoth-common from 0.13.0 to 0.13.1
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.1 to 0.6.2
* :pushpin: Automatic update of dependency thoth-common from 0.12.10 to 0.13.0
* :pushpin: Automatic update of dependency thoth-common from 0.12.9 to 0.12.10
* :pushpin: Automatic update of dependency pytest-asyncio from 0.10.0 to 0.11.0
* Be explicit about errors

## Release 0.10.1 (2020-08-11T11:55:43)
* Adjust docstring (#299)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.1 (#298)
* Feature/ordered versions (#293)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#295)
* :arrow_down: removed the files as they are no longer required
* Replace legacy urls (#286)
* :pushpin: Automatic update of dependency lxml from 4.5.1 to 4.5.2 (#289)
* :pushpin: Automatic update of dependency pytest-timeout from 1.4.1 to 1.4.2 (#290)
* :pushpin: Automatic update of dependency thoth-common from 0.13.13 to 0.14.2 (#288)
* add more functions to aiosource (#287)
* Add .thoth_last_analysis_id to .gitignore (#282)
* :pushpin: Automatic update of dependency pytest-asyncio from 0.12.0 to 0.14.0 (#285)
* :pushpin: Automatic update of dependency thoth-common from 0.13.8 to 0.13.13 (#284)
* :pushpin: Automatic update of dependency requests from 2.23.0 to 2.24.0 (#283)
* Increase pytest timeout
* Update OWNERS
* :pushpin: Automatic update of dependency pytest-timeout from 1.3.4 to 1.4.1

## Release 0.10.2 (2020-09-24T07:05:23)
### Features
* Add maintainers (#304)
### Bug Fixes
* fix package-version equality (#305)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest-mypy from 0.6.2 to 0.7.0 (#311)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#310)
* :pushpin: Automatic update of dependency attrs from 19.3.0 to 20.2.0 (#309)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.20.0 (#308)
* :pushpin: Automatic update of dependency pytest-cov from 2.10.0 to 2.10.1 (#306)

## Release 0.11.0 (2020-12-04T21:42:28)
### Features
* Fix testsuite for Python 3.8 (#328)
* Adjust how source name is derived (#325)
* :arrow_up: Automatic update of dependencies by kebechet. (#324)
* Add missing GitHub templates
* bump python version (#322)
### Bug Fixes
* Relock to fix typing extension marker issue
### Improvements
* make pre-commit happy (#314)
### Automatic Updates
* :pushpin: Automatic update of dependency aiohttp from 3.6.2 to 3.7.2 (#321)
* :pushpin: Automatic update of dependency aiohttp from 3.6.2 to 3.7.2 (#318)
* :pushpin: Automatic update of dependency pyelftools from 0.26 to 0.27 (#317)
* :pushpin: Automatic update of dependency lxml from 4.5.2 to 4.6.1 (#316)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.2 (#315)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.2 (#319)

## Release 0.12.0 (2021-02-08T13:32:28)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* Fix typing
* Introduce Thoth section in Pipfile
### Bug Fixes
* Reformat setup.py to fix pre-commit complains
### Improvements
* Add tests related to Thoth section of Pipfile
* removed bissenbay, thanks for your contributions!

## Release 0.13.0 (2021-02-15T12:42:31)
### Features
* Fix signature and make sure factory for default is called (#346)
* Fix signature to correctly describe return type (#345)
* Introduce supported version properties (#343)
* Register pytest markers
### Bug Fixes
* Raise an error if editable installs are used (#341)
### Improvements
* pep561 for type checking (#333)

## Release 0.14.0 (2021-02-16T14:23:54)
### Features
* Introduce disable index adjustment in Thoth's section in Pipfile (#349)

## Release 0.15.0 (2021-02-22T13:35:51)
### Features
* Optionally keep thoth specific configuration in Pipfile
* Add routines to support adding packages to Pipfile

## Release 0.15.1 (2021-02-23T08:21:20)
### Features
* Do not serialize empty dict in TOML in Pipfile
### Bug Fixes
* Do not serialize allow_prereleases if not configured so
### Improvements
* Fix serialization and loading of requirements files
### Other
* Override entries in Thoth section if they do not meet type expected

## Release 0.15.2 (2021-02-24T13:02:32)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet
* pre-releases do not need to be always stated in Pipfile

## Release 0.15.3 (2021-02-25T13:12:54)
### Features
* Copy dict before performing pop

## Release 0.15.4 (2021-03-01T21:23:12)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#365)
* Version identifier should be always non-None value
### Bug Fixes
* Fix loading Pipfile files when requirements are used
### Improvements
* Revert "Fix serialization and loading of requirements files"
* Adjust test checking for any version

## Release 0.15.5 (2021-03-05T12:36:36)
### Features
* Make pre-commit happy
* Optionally keep Thoth section when generating project
* Update OWNERS
* :sparkles: let's run pre-commit
* Add missing Kebechet templates

## Release 0.15.6 (2021-03-24T09:29:14)
### Features
* Fix serialization of packages without version specifier (#386)
* :arrow_up: Automatic update of dependencies by Kebechet (#385)
* :arrow_up: Automatic update of dependencies by Kebechet (#383)
* :arrow_up: Automatic update of dependencies by Kebechet (#380)
* add prow check with specific args (#378)

## Release 0.16.0 (2021-04-26T20:05:49)
### Features
* :arrow_up: Automatic update of dependencies by Kebechet (#390)
* Add support for constraints (#389)

## Release 0.16.1 (2021-04-27T10:16:07)
### Features
* Instantiate Pipfile instance just once (#393)

## Release 0.16.2 (2021-07-19T04:52:31)
### Features
* Make optional parameters optional
* :arrow_up: Automatic update of dependencies by Kebechet
* :arrow_up: Automatic update of dependencies by Kebechet (#398)
* :hatched_chick: update the prow resource limits (#397)
* Add note about constraints.txt to the README file (#396)
### Improvements
* make pre-commit happy
