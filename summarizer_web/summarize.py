from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import nltk
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"

nltk.download('punkt')


def summarize_article(url, sentence_count):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = []

    for sentence in summarizer(parser.document, sentence_count):
        sentences.append(str(sentence))

    return " ".join(sentences)


# def context(url, sentence_count, algorithm_type=1):
#     if algorithm_type == Algorithm.NLTK.value:
#         return summarize_by_nltk(url=url, sentence_count=sentence_count)
#     raise NotImplementedError(f'Algorithm {algorithm_type} does not exist')


def summarize_thread(thread, sentence_count):
    parser = PlaintextParser.from_string(thread, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    
    sentences = []

    for sentence in summarizer(parser.document, sentence_count):
        sentences.append(str(sentence))
    
    return " ".join(sentences)
