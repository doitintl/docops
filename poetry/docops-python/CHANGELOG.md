# Changelog

This project uses [semantic versioning][semver].

**Table of contents:**

- [2.x](#2x)
  - [2.1.0](#210)
  - [2.0.1](#201)
  - [2.0.0](#200)
- [1.x](#1x)
  - [1.0.0](#100)
- [0.x](#0x)
  - [0.1.0](#010)
  - [0.0.0](#000)

[semver]: https://semver.org/

<!--

## Unreleased

ADD UNRELEASED CHANGES HERE UNTIL THE NEXT RELEASE IS MADE

-->

## 2.x

### 2.1.0

_Released on 2021-01-03 ([view source and package files][2.1.0])_

**Enhancements:**

- Added new `docops-screenshots` program, which can frame screenshots with a drop shadow.

**Fixes:**

- The newer version of NLTK now downloads the required `omw-1.4` dataset.

[2.1.0]: https://github.com/doitintl/docops-utils/releases/tag/2.1.0

### 2.0.1

_Released on 2021-09-23 ([view source and package files][2.0.1])_

**Fixes:**

- Fixed "Created cache" message which was still printed even when the `--quiet` option was used.

- Fixed repository URL in package metadata.

[2.0.1]: https://github.com/doitintl/docops-utils/releases/tag/2.0.1

### 2.0.0

_Released on 2021-09-23 ([view source and package files][2.0.0])_

**Breaking changes:**

- The `--row-limit` option has been renamed `--term-limit` (to be agnostic to output type).

- The `--show-formats` option has been renamed to `--show-table-formats`, in keeping with the new `--show-output-types` option (see below).

**Enhancements:**

- Added the `--output-type` and `--show-output-types` options. At the moment, the only additional option this gives you is to turn off table output.

**Fixes**:

- The `data` directory is now shipped alongside the Python modules, which is now available locally when installing the package.

[2.0.0]: https://github.com/doitintl/docops-utils/releases/tag/2.0.0

## 1.x

### 1.0.0

_Released on 2021-09-19 ([view source and package files][1.0.0])_

**Breaking changes:**

- This project has been renamed from `doit-gloss-utils` to `doitintl-docops`, and a previously unreleased `doit-gitbook-client` package has been merged into the project.

  The top-level Python [namespace package][pep-420] name is now called `doitintl`. The previously named `gloss` module is now `doitintl.docops.gloss` and the previously named `dgbc` module is now `doitintl.docops.gitbook`.

  The previously named `dgloss-analyze-terms` CLI tool is now `docops-gloss-terms`, and the previously named `dgbc` tool is now `docops-gitbook`.

**Enhancements:**

- Added `--whoami` functionality to the `docops-gitbook` CLI tool (i.e., to demonstrate that authentication worked by showing you your own user details)

- Lowered required Python version to 3.8.

**Fixes:**

- Fixed bug with `--print-cache` not working unless you first run the analyzer.

- Fixed emoji rendering bug on PyPI by using the emoji character directly instead of GitHub emoji syntax.

[pep-420]: https://www.python.org/dev/peps/pep-0420/
[1.0.0]: https://github.com/doitintl/docops-utils/releases/tag/1.0.0

## 0.x

### 0.1.0

_Released on 2021-09-15 (tag no longer available)_

**Enhancements:**

- The terms analyzer can now ignore word case during analysis.

  This feature is configurable (see below).

- The terms analyzer can now ignore [stop words][stop words] in one of 23 different languages.

  This feature is configurable (see below).

- You can now configure the token analyzer (CLI and library) with multiple `.dgloss.conf` configuration files.

  By default, the token analyzer will scan the target directory (top-down) for configuration files. The `.dgloss.conf` files can list any number of configuration instructions. The instructions are processed in the order they are read (file-by-file).

  Configuration instructions improve the utility of term analysis by allowing you to filter out terms that are of no interest.

  The [README][readme] has some basic examples as well as basic syntax documentation for writing configuration files.

- Added the `--config-dir` option, which allows you to specify a separate directory to scan top-down for config files. This option means that:

  - You do not have to modify the target directory in any way by adding configuration files.

  - You can maintain a separate directory of shared configuration files for use with multiple projects.

- Configuration files give you the option to:

  - Specify which word frequency reference corpus you want to use for comparison.

    Defaults to `leeds`.

    The `leeds` corpus is provided by this package and is the only available word frequency corpus for the time being.

  - Configure case-insensitivity with `true` or `false`.

    Defaults to `true` (i.e., will ignore case).

  - Enable stop words filtering by specifying a language.

    Defaults to `english`.

  - Specify an arbitrary number of string literals to ignore. If a term exactly matches the string literal, it will be ignored.

  - Specify an arbitrary number of regexes to ignore. If a regex matches a term, the term will be ignored.

  See the [README][readme] for more details.

**Fixes:**

- Fixed a few minor bugs.

- Fixed the `dgloss-analyze-terms --help` output.

[readme]: https://github.com/doitintl/docops-utils/
[stop words]: https://en.wikipedia.org/wiki/Stop_word

### 0.0.0

_Released on 2021-09-10 (tag no longer available)_

- Added release notes (`CHANGELOG.md`).

- Added `dgloss` Python library.

- Added `dgloss.analyzers.terms` module that can scan a directory of text files for the most uncommon terms.

- Added `dgloss-analyze-terms` CLI tool to wrap the `dgloss.analyzers.terms` module.
