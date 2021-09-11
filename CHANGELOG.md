# Release Notes

This project uses [semantic versioning][semver].

**Table of contents:**

- [0.x](#0x)
  - [0.0.x](#00x)
    - [Version 0.0.0](#version-000)

<!--

## Unreleased

- The terms analyzer now converts all terms to lower case prior to analysis.

- The terms analyzer now ignores common English [stop words][stop words].

- The token analyzer (CLI and library) can now read configuration files named
  `.dgloss.conf` (which are automatically found when scanning the target
  directory).

- Added the `--config-dir` option, which allows you to specify a separate
  directory to scan for config files (so that you're not forced to add the
  config files to the target directory).

- Configuration files now give you the option to:

  - Specify which reference corpus you want to use for comparison

  - Switch case-sensitivity on and off

  - Switch the use of common English stop words filtering on and off

  - Specify term literals to ignore

  - Specify term regexes to ignore

  Combined, these features improve the utility of the term analysis by allowing
  you to filter out terms that are of no interest. This allows for an iterative
  approach to improving the relevancy of the output.

-->

## 0.x

### 0.0.x

#### Version 0.0.0

*Released on 2021-09-10*

- Added release notes (`CHANGELOG.md`)

- Added `dgloss` Python library

- Added `dgloss.analyzers.terms` module that can scan a directory of text files
  for the most uncommon terms

- Added `dgloss-analyze-terms` CLI tool to wrap the `dgloss.analyzers.terms`
  module

<!-- Link references go below this line, sorted ascending --->

[semver]: https://semver.org/
[stop words]: https://en.wikipedia.org/wiki/Stop_word
