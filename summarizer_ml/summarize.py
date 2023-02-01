from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import json

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCE_COUNT = 5


def summarize_article(urls):
    url = urls[0]['expanded_url']
    title = urls[0]['title']

    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = []

    for sentence in summarizer(parser.document, SENTENCE_COUNT):
        sentences.append(str(sentence))

    summary = " ".join(sentences)

    return {'summary': summary, 'url': url, 'title': title}


def lambda_handler(event, context):
    response_payload = event['detail']['responsePayload']
    details = json.loads(response_payload)
    summaries = []

    for detail in details:
        summary = summarize_article(urls=detail['urls'])
        summaries.append(summary)

    return json.dumps(summaries, default=str)
