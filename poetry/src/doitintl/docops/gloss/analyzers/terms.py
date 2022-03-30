# MIT License

# Copyright 2021, DoiT International

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import gzip
import math
import os
import re
import sqlite3

from tabulate import tabulate

import nltk

from doitintl import docops
from doitintl.docops.gloss import charset


class TermAnalyzer:

    _DROP_TABLE_QUERY = """
        DROP TABLE IF EXISTS lemmas;
    """

    _CREATE_TABLE_QUERY = """
        CREATE TABLE lemmas (
            source TEXT NOT NULL,
            lemma TEXT NOT NULL,
            ipm REAL NOT NULL,
            PRIMARY KEY (source, lemma)
        ) WITHOUT ROWID;
    """

    _INSERT_LEMMA_QUERY = """
        INSERT OR REPLACE INTO lemmas (
            source, lemma, ipm
        ) VALUES (
            ?, ?, ?
        );
    """

    _SELECT_DELTAS_QUERY = """
        SELECT
            target.lemma AS lemma,
            IIF(ref.ipm IS NOT NULL, target.ipm - ref.ipm, target.ipm) AS delta
        FROM
            lemmas AS target
        LEFT JOIN
            lemmas AS ref
        ON
            ref.source = 'reference' AND ref.lemma = target.lemma
        WHERE
            target.source = 'target' AND delta > 0
        ORDER BY
            delta DESC
        LIMIT ?;
    """

    _config = None

    def __init__(self, config):
        # Load configuration before continuing
        self._config = config

    def _print(self, *args):
        self._config.printer.print(*args)

    def _create_schema(self):
        con = sqlite3.connect(self._config.cache.get_db_path())
        cur = con.cursor()
        cur.execute(self._DROP_TABLE_QUERY)
        cur.execute(self._CREATE_TABLE_QUERY)
        con.commit()
        con.close()

    def ignore_case(self):
        self._ignore_case = True

    def ignore_stop_words(self):
        self._ignore_stop_words = True

    def _load_pkg_corpus(self):
        # TODO: Raise custom exception if dict key not found
        corpus_def = self._config.word_freq_corpus
        if not corpus_def:
            raise docops.ConfigurationError(
                "No word frequency corpus specified"
            )
        corpus_name = corpus_def["name"]
        if not docops.quiet:
            self._print(
                f"<fg=blue>Loading word frequency corpus</>: {corpus_name}"
            )
        with gzip.open(corpus_def["abs_filename"], "rb") as f:
            bytes = f.read()
        text = charset.decode_bytes(
            bytes, filename=corpus_def["data_filename"]
        )
        line_re = re.compile(corpus_def["re"])
        con = sqlite3.connect(self._config.cache.get_db_path())
        cur = con.cursor()
        source = "reference"
        for line in text.splitlines():
            matches = line_re.match(line.strip())
            if not matches:
                continue
            ipm = float(matches.group("ipm"))
            lemma = matches.group("lemma")
            lemma = self._config.lemmatizer.lemmatize(lemma)
            lemma = self._filter_lemma(lemma)
            if not lemma:
                continue
            cur.execute(self._INSERT_LEMMA_QUERY, [source, lemma, ipm])
            if docops.verbose:
                self._print(f"<fg=green>Added</>: {source}, {lemma}, {ipm}")
        con.commit()
        con.close()

    def _scan_dir(self):
        dirname = self._config.target_dirname
        if not docops.quiet:
            self._print(f"<fg=blue>Scanning target directory</>: {dirname}")
        lemmas_counts = {}
        total_lemma_count = 0
        for root, dirs, files in os.walk(dirname):
            # Skip directories starting with `.`
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in files:
                # Skip files starting with `.`
                if filename.startswith("."):
                    continue
                filename = os.path.join(root, filename)
                lemma_count = self._scan_file(filename, lemmas_counts)
                total_lemma_count += lemma_count
        self._process_lemmas(lemmas_counts, total_lemma_count)

    def _scan_file(self, filename, lemmas_counts):
        if docops.verbose:
            self._print(f"<fg=blue>Scanning</>: {filename}")
        try:
            text = charset.decode_file(filename)
        except docops.EncodingError:
            if docops.verbose:
                self._print(f"<fg=yellow>Skipped</>: {filename}")
            # Return a count of zero lemmas
            return 0
        tokens = nltk.word_tokenize(text)
        total_lemma_count = 0
        for token in tokens:
            lemma = self._config.lemmatizer.lemmatize(token)
            lemma = self._filter_lemma(lemma)
            if not lemma:
                continue
            count = lemmas_counts.get(lemma, 0)
            lemmas_counts[lemma] = count + 1
            total_lemma_count += 1
        return total_lemma_count

    def _filter_lemma(self, lemma):
        config = self._config
        if config.ignore_case:
            lemma = lemma.lower()
        if lemma in config.ignore_literals:
            if docops.verbose:
                self._print(f"<fg=yellow>Ignoring literal</>: {lemma}")
            return
        if any(regex.search(lemma) for regex in config.ignore_regexes):
            if docops.verbose:
                self._print(f"<fg=yellow>Ignoring regex</>: {lemma}")
            return
        return lemma

    def _process_lemmas(self, lemmas_counts, total_lemma_count):
        source = "target"
        con = sqlite3.connect(self._config.cache.get_db_path())
        cur = con.cursor()
        for lemma, count in lemmas_counts.items():
            percent = count / total_lemma_count
            ipm = round(percent * 1000000, 2)
            cur.execute(self._INSERT_LEMMA_QUERY, [source, lemma, ipm])
            if docops.verbose:
                if len(lemma) > 40:
                    lemma = lemma[:40] + "[...]"
                self._print(f"<fg=green>Added</>: {source}, {lemma}, {ipm}")
        con.commit()
        con.close()

    def run(self):
        self._create_schema()
        self._load_pkg_corpus()
        self._scan_dir()

    def print_table(self):
        if docops.verbose:
            print("Table format: {self.docops.table_format}")
        headers = ["Rank", "Base term"]
        con = sqlite3.connect(self._config.cache.get_db_path())
        cur = con.cursor()
        table_rows = []
        for row in cur.execute(self._SELECT_DELTAS_QUERY, [docops.term_limit]):
            lemma, delta = row
            rank = round(math.log(delta))
            table_rows.append([rank, lemma])
        con.close()
        table = tabulate(
            table_rows, headers=headers, tablefmt=docops.table_format
        )
        self._print(table)
