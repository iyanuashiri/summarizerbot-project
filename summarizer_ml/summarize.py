from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import json

import nltk
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"

nltk.download('punkt')


def summarize_article(urls):
    url = urls[0]['url']
    title = urls[0]['title']

    sentence_count = 5
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = []

    for sentence in summarizer(parser.document, sentence_count):
        sentences.append(str(sentence))

    summary = " ".join(sentences)

    return {'summary': summary, 'url': url, 'title': title}


def lambda_handler(event, context):
    details = json.loads(event)

    summaries = []

    for detail in details:
        summary = summarize_article(urls=detail['urls'])
        summaries.append(summary)

    detail_json = {
        "detail": {
            'detail': summaries
        },
        "detail-type": "Summary Notification",
        "source": "summary.notification"
    }

    return json.dumps(detail_json, default=str)
