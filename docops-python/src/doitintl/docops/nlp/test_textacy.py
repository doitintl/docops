from textacy import preprocessing
from textacy import extract
from icecream import ic

import textacy


def compile(input_filename, output_filename):

    text = open(input_filename).read()

    text = preprocessing.remove.html_tags(text)
    text = preprocessing.remove.brackets(text)
    text = preprocessing.remove.punctuation(text)
    text = preprocessing.remove.accents(text)

    text = preprocessing.replace.currency_symbols(text, " ")
    text = preprocessing.replace.emails(text, " ")
    text = preprocessing.replace.emojis(text, " ")
    text = preprocessing.replace.hashtags(text, " ")
    text = preprocessing.replace.numbers(text, " ")
    text = preprocessing.replace.phone_numbers(text, " ")
    text = preprocessing.replace.urls(text, " ")

    text = preprocessing.normalize.bullet_points(text)
    text = preprocessing.normalize.hyphenated_words(text)
    text = preprocessing.normalize.quotation_marks(text)
    text = preprocessing.normalize.unicode(text, form="NFC")
    text = preprocessing.normalize.whitespace(text)

    output_file = open(output_filename, "w")
    output_file.write(text)
    output_file.close()

    return text


def make_doc(text):
    doc = textacy.make_spacy_doc(text, "en_core_web_sm")


def test_ngrams(doc):
    ngrams = extract.ngrams(
        doc,
        (2, 3, 4, 5),
        filter_stops=True,
        filter_punct=True,
        filter_nums=True,
    )

    ic(ngrams)


# ic(list(textacy.extract.ngrams(doc, 3, filter_stops=True,
#    filter_punct=True, filter_nums=False)))

# ic(kt.textrank(doc, normalize="lemma", topn=10))

# ic(kt.sgrank(doc, ngrams=(1, 2, 3, 4), normalize="lower", topn=0.1))


def run():
    text = compile("docs.html", "docs.txt")
    doc = make_doc(text)
    test_ngrams(doc)
