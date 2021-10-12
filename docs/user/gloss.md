# Glossary Utilities

_A collection of utilities for the creation and maintenance of technical
glossaries_

> 📝&nbsp;&nbsp;**Note**
>
> The glossary utilities do not currently have any documentation besides the
> sparse information on this page. We will add more detailed documentation at a
> later date.

**Table of contents:**

- [Use](#use)
  - [CLI tool](#cli-tool)
    - [Example uses](#example-uses)
- [Configuration files](#configuration-files)
  - [Syntax](#syntax)
  - [Notes](#notes)

## Use

### CLI tool

You can invoke the CLI program with this command:

```console
$ docops-gloss-terms
Usage:
  docops-gloss-terms [options] <DIR>
  docops-gloss-terms [options] (-h | --help)
  docops-gloss-terms [options] (--version)
  docops-gloss-terms [options] (--show-formats)
  docops-gloss-terms [options] (--print-cache)
  docops-gloss-terms [options] (--delete-cache)
```

#### Example uses

As an example, you can run the term analyzer on all text files within a
repository and print the top 10 candidate terms, like this:

```console
$ docops-gloss-terms --row-limit=10 examples/
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

However, this example was run with no configuration file and demonstrates how
noisy the output can be without configuring the analyzer.

If you reanalyze the same repository with configuration file, you can improve
the results with relatively little effort:

```console
$ docops-gloss-terms --config-dir=data/configs/test/ --row-limit=10 examples/
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

```text
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
  the _University of Leeds_ [Centre for Translation Studies
  corpora][leeds_corpora].

  In the future, this package may provide alternative word frequency corpora.

- Any languages in the [Natural Language Toolkit][nltk] (NLTK) `stopwords`
  corpus are supported. See the [NLTK Corpora][nltk_corpora] page for more
  information.

  This software was written to process English text, so you probably want to
  specify `english` if you wish to ignore stop words.

- Regular expressions are parsed by the Python [re][re_module] module.

[leeds_corpora]: http://corpus.leeds.ac.uk/list.html
[nltk]: https://www.nltk.org/
[nltk_corpora]: http://www.nltk.org/nltk_data/
[re_module]: https://docs.python.org/3/library/re.html

---

🏠 [Home][home]

[home]: https://github.com/doitintl/docops-python
