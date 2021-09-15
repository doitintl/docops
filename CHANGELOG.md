# Release Notes

This project uses [semantic versioning][semver].

**Table of contents:**

- [0.x](#0x)
  - [0.0.1](#001)
    - [Enhancements](#enhancements)
    - [Fixes](#fixes)
  - [0.0.0](#000)

<!--

## Unreleased

- ADD UNRELEASED CHANGES HERE UNTIL THE NEXT RELEASE IS MADE

#### Enhancements

#### Fixes

- Fixed emoji rendering bug on PyPI by using the emoji character directly
  instead of GitHub emoji syntax.

-->

## 0.x

### 0.0.1

_Released on 2021-09-15_ ([view source and package files][0.0.1])

#### Enhancements

- The terms analyzer can now ignore word case during analysis.

  This feature is configurable (see below).

- The terms analyzer can now ignore [stop words][stop words] in one of 23
  different languages.

  This feature is configurable (see below).

- You can now configure the token analyzer (CLI and library) with multiple
  `.dgloss.conf` configuration files.

  By default, the token analyzer will scan the target directory (top-down) for
  configuration files. The `.dgloss.conf` files can list any number of
  configuration instructions. The instructions are processed in the order they
  are read (file-by-file).

  Configuration instructions improve the utility of term analysis by allowing
  you to filter out terms that are of no interest.

  The [README][README] has some basic examples as well as basic syntax
  documentation for writing configuration files.

- Added the `--config-dir` option, which allows you to specify a separate
  directory to scan top-down for config files. This option means that:

  - You do not have to modify the target directory in any way by adding
    configuration files.

  - You can maintain a separate directory of shared configuration files for use
    with multiple projects.

- Configuration files give you the option to:

  - Specify which word frequency reference corpus you want to use for
    comparison.

    Defaults to `leeds`.

    The `leeds` corpus is provided by this package and is the only available
    word frequency corpus for the time being.

  - Configure case-insensitivity with `true` or `false`.

    Defaults to `true` (i.e., will ignore case).

  - Enable stop words filtering by specifying a language.

    Defaults to `english`.

  - Specify an arbitrary number of string literals to ignore. If a term exactly
    matches the string literal, it will be ignored.

  - Specify an arbitrary number of regexes to ignore. If a regex matches a
    term, the term will be ignored.

  See the [README][README] for more details.

#### Fixes

- Fixed a few minor bugs.

- Fixed the `dgloss-analyze-terms --help` output.

### 0.0.0

_Released on 2021-09-10_ ([view source and package files][0.0.1])

- Added release notes (`CHANGELOG.md`).

- Added `dgloss` Python library.

- Added `dgloss.analyzers.terms` module that can scan a directory of text files
  for the most uncommon terms.

- Added `dgloss-analyze-terms` CLI tool to wrap the `dgloss.analyzers.terms`
  module.

<!-- Link references go below this line, sorted ascending --->

[semver]: https://semver.org/
[stop words]: https://en.wikipedia.org/wiki/Stop_word
[README]: https://github.com/doitintl/docops-gloss-utils
[0.0.0]: https://github.com/doitintl/docops-gloss-utils/releases/tag/0.0.0
[0.0.1]: https://github.com/doitintl/docops-gloss-utils/releases/tag/0.0.1
