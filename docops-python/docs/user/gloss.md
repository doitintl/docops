# Glossary Utilities

_A collection of utilities for the creation and maintenance of technical glossaries_

> 📝&nbsp;&nbsp;**Note**
>
> The glossary utilities do not currently have any documentation besides the sparse information on this page. We will add more detailed documentation at a later date.

**Table of contents:**

- [Usage](#usage)
  - [CLI program](#cli-program)
    - [Example uses](#example-uses)
- [Configuration files](#configuration-files)
- [Configuration options](#configuration-options)
  - [Use](#use)
    - [Corpus](#corpus)
  - [Ignore](#ignore)
    - [Case](#case)
    - [Stowords](#stowords)
    - [Term literals](#term-literals)
    - [Term regexes](#term-regexes)
- [Example configuration file](#example-configuration-file)

## Usage

### CLI program

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

As an example, you can run the term analyzer on all text files within a repository and print the top 10 candidate terms, like this:

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

However, this example was run with no configuration file and demonstrates how noisy the output can be without configuring the analyzer.

You can re-analyze the [examples directory][examples_dir] using the [test configuration directory][test_dir] to see how a relatively simple [configuration file][config_file] can improve the results:

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

[config_file]: ../../tests/config/.dgloss.conf
[examples_dir]: ../../tests/examples
[test_dir]: ../../tests/config

## Configuration files

The term analyzer will scan the target directory (or the configuration directory instead, if specified) top-down for any file named one of the following:

- `.dgloss.yaml`
- `.dgloss.yml`
- `dgloss.yaml`
- `dgloss.yml`

The configuration files can list any number of configuration instructions. The instructions are processed in the order they are read (file-by-file).

## Configuration options

Each configuration file must be valid [YAML][yaml].

Unknown YAML keys are silently ignored.

Additionally, as is standard with YAML, empty lines and lines beginning with `#` are also ignored.

[yaml]: [https://en.wikipedia.org/wiki/YAML]

### Use

The top level `use` key can take one child key.

#### Corpus

The `corpus` key can take the value of any supported word frequency reference
corpus name.

Example configuration:

```yaml
use:
  corpus: leeds
```

For the time being, the only supported corpus is `leeds`, which is an English
language word frequency corpus taken from the _University of Leeds_ [Centre for
Translation Studies corpora][leeds_corpora]. In the future, this package may
provide additional word frequency corpora.

[leeds_corpora]: http://corpus.leeds.ac.uk/list.html

### Ignore

The top level `ignore` key can take several child keys.

#### Case

The `case` key can be set to `true` or `false` and indicates whether or not to
ignore word case during analysis.

Example configuration:

```yaml
ignore:
  case: true
```

The default value is `true`.

#### Stowords

The `stopwords` key can be any supported language name.

Any languages in the [Natural Language Toolkit][nltk] (NLTK) stopwords corpus
are supported. See the [NLTK Corpora][nltk_corpora] page for more information.

This software was written to process English text, so you probably want to
specify `english` if you wish to ignore stop words.

Example configuration:

```yaml
ignore:
  stopwords: 'english'
```

The default value is `english`.

[nltk_corpora]: http://www.nltk.org/nltk_data/
[nltk]: https://www.nltk.org/

#### Term literals

The `term-literals` key takes a list of literal strings. The analyzer will ignore
any terms that exactly match the specified string.

Example configuration:

```yaml
ignore:
  term-literals:
      - foo
      - bar
      - baz
```

#### Term regexes

The `regexes` key takes a list of [regular expressions][regexes]. The analyzer
will ignore any terms that match the specified regular expression.

Example configuration:

```yaml
ignore:
  term-regexes:
    # Ignore terms without any letters
    - '^[^a-zA-Z]+$'
    # Ignore terms that are a single letter
    - '^[a-zA-Z]$'
```

Regular expressions are parsed by the Python [re][re_module] module.

[regexes]: https://en.wikipedia.org/wiki/Regular_expression
[re_module]: https://docs.python.org/3/library/re.html

## Example configuration file

If you combined all of the [configuration option]((#configuration-options))
examples above, the full configuration file would look like this:

```yaml
use:
  corpus: leeds

ignore:
  case: true
  stopwords: 'english'
  term-literals:
    - foo
    - bar
    - baz
  term-regexes:
    # Ignore terms without any letters
    - '^[^a-zA-Z]+$'
    # Ignore terms that are a single letter
    - '^[a-zA-Z]$'
```

---

🏠 [Home][home]

[home]: https://github.com/doitintl/docops-python
