import gzip
import math
import os
import pathlib
import re
import sqlite3

import charset_normalizer

import nltk
from nltk import downloader
from nltk import stem

from tabulate import tabulate

import dgloss
from dgloss.config import Configuration
from dgloss.color import Formatter


class TermAnalyzer:

    # TODO: Add more corpora to test with
    # TODO: Allow users to select which corpora to use
    # TODO: Document this in the CLI script
    PKG_CORPORA = {
        "leeds": {
            "filename": "data/corpora/leeds.txt.gz",
            "re": r"(?P<rank>\d+) +(?P<ipm>\d+(\.?\d+)) +(?P<lemma>\\w+)",
        }
    }

    # https://www.nltk.org/nltk_data/
    NLTK_CORPORA = ["punkt", "wordnet"]

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
            local.lemma AS lemma,
            IIF(ref.ipm IS NOT NULL, local.ipm - ref.ipm, local.ipm) AS delta
        FROM
            lemmas AS local
        LEFT JOIN
            lemmas AS ref
        ON
            ref.source = 'reference' AND ref.lemma = local.lemma
        WHERE
            local.source = 'local' AND delta > 0
        ORDER BY
            delta DESC
        LIMIT ?;
    """

    _formatter = None
    _config = None
    _cache_path = None
    _db_path = None
    _lemmatizer = None

    def __init__(self):
        self._formatter = Formatter()
        self._config = Configuration()
        self._cache_path = self._config.make_cache()
        filename_path = pathlib.Path(f"{__name__}.db")
        self.db_path = self._cache_path.joinpath(filename_path)
        self._create_schema()

    def _print(self, msg, stdout=True):
        self._formatter.print(msg, stdout)

    def _create_schema(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(self._DROP_TABLE_QUERY)
        cur.execute(self._CREATE_TABLE_QUERY)
        con.commit()
        con.close()

    def use_pkg_corpus(self, corpus_name):
        module_path = pathlib.Path(f"{__file__}")
        # TODO: Raise custom exception if dict key not found
        corpus = self.PKG_CORPORA[corpus_name]
        data_path = module_path.parent.parent.joinpath(corpus["filename"])
        if not dgloss.quiet:
            self._print(f"<fg=blue>Loading corpus</>: {corpus_name}")
        with gzip.open(data_path, "rb") as f:
            data_bytes = f.read()
        data = str(charset_normalizer.from_bytes(data_bytes).best())
        line_re = re.compile(corpus["re"])
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        source = "reference"
        for line in data.splitlines():
            matches = line_re.match(line.strip())
            if not matches:
                continue
            ipm = float(matches.group("ipm"))
            lemma = matches.group("lemma")
            cur.execute(self._INSERT_LEMMA_QUERY, [source, lemma, ipm])
            # TODO convert to canonical lemma using nltk before importing
            if dgloss.verbose:
                self._print(f"<fg=green>Inserted</>: {source}, {lemma}, {ipm}")
        con.commit()
        con.close()

    def init_nltk(self):
        nltk_dir = self._cache_path.joinpath("nltk")
        nltk_dir.mkdir(parents=True, exist_ok=True)
        nltk.data.path.insert(0, nltk_dir)
        dl = downloader.Downloader()
        for name in self.NLTK_CORPORA:
            if not dl.is_installed(name):
                self._print(f"<fg=blue>Installing corpus</>: {name}")
                dl.download(name, quiet=True)
            else:
                if dl.is_stale(name):
                    self._print(f"<fg=blue>Updating corpus</>: {name}")
                    dl.update(name, quiet=True)
        self._lemmatizer = stem.WordNetLemmatizer()

    def scan_dir(self, dirname):
        if not dgloss.quiet:
            self._print(f"<fg=blue>Scanning directory</>: {dirname}")
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
                lemma_count = self.scan_file(filename, lemmas_counts)
                total_lemma_count += lemma_count
        self.process_lemmas(lemmas_counts, total_lemma_count)

    def scan_file(self, filename, lemmas_counts):
        charset = charset_normalizer.from_path(filename).best()
        if not charset:
            # We were unable to decode this as a text file
            if dgloss.verbose:
                self._print(f"<fg=yellow>Skipping</>: {filename}")
            # Return a count of zero lemmas
            return 0
        if not dgloss.quiet:
            self._print(f"<fg=blue>Scanning</>: {filename}")
        text = str(charset)
        tokens = nltk.word_tokenize(text)
        word_re = re.compile(r"\w")
        total_lemma_count = 0
        for token in tokens:
            if not word_re.search(token):
                continue
            lemma = self._lemmatizer.lemmatize(token)
            count = lemmas_counts.get(lemma, 0)
            lemmas_counts[lemma] = count + 1
            total_lemma_count += 1
        return total_lemma_count

    def process_lemmas(self, lemmas_counts, total_lemma_count):
        source = "local"
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        for lemma, count in lemmas_counts.items():
            percent = count / total_lemma_count
            ipm = round(percent * 1000000, 2)
            cur.execute(self._INSERT_LEMMA_QUERY, [source, lemma, ipm])
            if dgloss.verbose:
                if len(lemma) > 40:
                    lemma = lemma[:40] + "[...]"
                self._print(f"<fg=green>Inserted</>: {source}, {lemma}, {ipm}")
        con.commit()
        con.close()

    def print_ranks(self, limit=100, format="github"):
        headers = ["Rank", "Base term"]
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        table_rows = []
        for row in cur.execute(self._SELECT_DELTAS_QUERY, [limit]):
            lemma, delta = row
            rank = round(math.log(delta))
            table_rows.append([rank, lemma])
        con.close()
        table = tabulate(table_rows, headers=headers, tablefmt=format)
        self._print(table)
