# DoiT Glossary Utilities

*A collection of utilities for the creation and maintenance of technical
glossaries*

> 📝 &nbsp;&nbsp;**Note**
>
> This project does not currently have any documentation besides the sparse
> information in this README. We will add more detailed documentation at a
> later date.

**Table of contents:**

- [Install](#install)
- [Use](#use)
  - [CLI tool](#cli-tool)
    - [Example uses](#example-uses)
- [Configuration files](#configuration-files)
  - [Syntax](#syntax)
  - [Notes](#notes)

## Install

You can install the [doit-gloss-utils][pypi-project] Python package using
[Pip][pip]:

```console
$ pip install doit-gloss-utils
Collecting doit-gloss-utils
  Downloading doit_gloss_utils-0.0.0-py3-none-any.whl (175 kB)
[...]
Successfully installed doit-gloss-utils-0.0.0
```

The [project releases][releases] page has a complete list of all releases and
the corresponding release notes and release assets.

## Use

### CLI tool

This project provides the following command-line tool:

```console
$ dgloss-analyze-terms --help
Find terms that may be candidates for inclusion in a glossary

Usage:

  dgloss-analyze-terms [options] <DIR>
  dgloss-analyze-terms [options] (-h | --help)
  dgloss-analyze-terms [options] (--version)
  dgloss-analyze-terms [options] (--show-formats)
  dgloss-analyze-terms [options] (--print-cache)
  dgloss-analyze-terms [options] (--delete-cache)

This program will:

  - Scan the target directory (`<DIR>`) for configuration files named
    `.dgloss.conf` and process them prior to analysis.

    You can use the `--config-dir` option to specify an alternative directory
    to scan for configuration files.

  - Scan the target directory (`<DIR>`) for files (ignoring any directory or
    filename that begins with the `.` character).

  - Tokenize all files (that can be decoded as character data) into a list of
    unique terms, regardless of file format.

  - Attempt to group terms using lemmatization (i.e., convert inflected words
    to their standard to dictionary form).

  - Count how often every term is used and compare this with word frequency
    data from a standard (i.e., non-technical) English-language corpus.

  - Print a list of terms that appear more often than expected, ranked on a
    logarithmic scale, and sorted from the highest to the lowest frequency.

Basic options:

  -h, --help               Print this help message and exit

  --version                Print the software version number and exit

  -v, --verbose            Display verbose output messages

  -q, --quiet              Silence most output messages

  --disable-ansi           Disable ANSI escape code formatting

  -c --config-dir=DIR      Search `DIR` for `.dgloss.conf` files instead of the
                           target directory

  -l, --row-limit=NUM      Limit results to `NUM` rows [default: 100]

  -r, --table-format=TYPE  Use table format `TYPE` [default: simple]

  --show-formats           Print a list of supported table formats and exit

  --print-cache            Print the location of the cache directory and exit

  --delete-cache           Delete the cache directory and exit

  --show-warnings          Show Python warnings
```

#### Example uses

As an example, you can run the term analyzer on all text files within the
[examples directory][examples_dir] and print the top 10 candidate terms, like
this:

```console
$ dgloss-analyze-terms --row-limit=10 examples/
Scanning configuration directory: examples
Loading word frequency corpus: leeds
Scanning target directory: examples
  Rank  Base term
------  -----------
    11  *
    11  .
    10  ,
    10  #
    10  %
    10  ''
    10  )
    10  (
    10  :
    10  ]
```

The [examples directory][examples_dir] has no configuration file (i.e., only
the [default values](#syntax) are set). This example demonstrates how noisy the
output can be without configuring the analyzer.

You can re-analyze the [examples directory][examples_dir] using the [test
configuration directory][test_dir] to see how a relatively simple
[configuration file][config file] can improve the results:

```console
$ dgloss-analyze-terms --config-dir=data/configs/test/ --row-limit=10 examples/
Scanning configuration directory: data/configs/test
Loading word frequency corpus: leeds
Scanning target directory: examples
  Rank  Base term
------  -----------
    10  cloud
    10  account
    10  aws
     9  billing
     9  google
     9  access
     9  report
     9  spot
     9  instance
     9  service
```

## Configuration files

The term analyzer will scan the target directory (or the configuration
directory instead, if specified) top-down for any file named `.dgloss.conf`.

The `.dgloss.conf` files can list any number of configuration instructions. The
instructions are processed in the order they are read (file-by-file).

### Syntax

Each `.dgloss.conf` instruction takes the form of a line using the following
syntax:

```
COMMAND OPTION ARGUMENT
```

All three components of the instruction are required.

Lines beginning with `#` are treated as comments and will be ignored. Empty
lines will also be ignored.

The current list of valid instructions are:

<table>
  <tr>
    <th>Command</th>
    <th width="20%">Argument</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>Use&nbsp;corpus&nbsp;&lt;ARGUMENT&gt;</code></td>
    <td>Any supported corpora name</td>
    <td><code>leeds</code></td>
    <td>Use the specified corpus as a word frequency reference</td>
  </tr>
  <tr>
    <td><code>ignore&nbsp;case&nbsp;&lt;ARGUMENT&gt;</code></td>
    <td><code>true</code> or <code>false</code></td>
    <td><code>true</code></td>
    <td>Whether or not to ignore word case</td>
  </tr>
  <tr>
    <td><code>ignore&nbsp;stopwords&nbsp;&lt;ARGUMENT&gt;</td>
    <td>Any supported language name</td>
    <td>None</td>
    <td>Ignore common stop words for the specified language</td>
  </tr>
  <tr>
    <td><code>ignore&nbsp;literal&nbsp;&lt;ARGUMENT&gt;</td>
    <td>Any string</td>
    <td>None</td>
    <td>Ignore any terms that exactly match the specified string</td>
  </tr>
  <tr>
    <td><code>ignore&nbsp;regex&nbsp;&lt;ARGUMENT&gt;</td>
    <td>Any regular expression</td>
    <td>None</td>
    <td>Ignore any terms that match the specified regular expression</td>
  </tr>
</table>

### Notes

- For the time being, the only supported word frequency reference corpus is
  `leeds`.

  The `leeds` corpus is an English language word frequency corpus taken from
  the _University of Leeds Centre for Translation Studies_
  [corpora][leeds_corpora].

  In the future, this package may provide alternative word frequency corpora.

- Any languages in the [Natural Language Toolkit][nltk] (NLTK) `stopwords`
  corpus are supported. See the [NLTK Corpora][nltk_corpora] page for more
  information.

  This software was written to process English text, so you probably want to
  specify `english` if you wish to ignore stop words.

- Regular expressions are parsed by the Python [re][re_module] module.

<!-- Link references go below this line, sorted ascending --->

[config file]: blob/main/data/configs/test/.dgloss.conf
[examples_dir]: tree/main/examples
[leeds_corpora]: http://corpus.leeds.ac.uk/list.html
[nltk_corpora]: http://www.nltk.org/nltk_data/
[nltk]: https://www.nltk.org/
[pip]: https://pip.pypa.io/en/stable/
[pypi-project]: https://pypi.org/project/doit-gloss-utils
[re_module]: https://docs.python.org/3/library/re.html
[releases]: https://github.com/doitintl/docops-gloss-utils/releases
[test_dir]: tree/main/data/configs/test
