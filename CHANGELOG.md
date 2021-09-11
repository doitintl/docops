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
