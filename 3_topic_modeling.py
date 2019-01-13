"""
Usage:
    3_topic_modeling <num_topics>
"""


import docopt
import gensim
from gensim.corpora.dictionary import Dictionary
import nltk

from lib.elastic import og_reader


def extract_text(tweet):
    try:
        text = tweet['_source']['extended_tweet']['full_text']
    except KeyError:
        try:
            text = tweet['_source']['extended_tweet']['text']
        except KeyError:
            try:
                text = tweet['_source']['message']
            except KeyError:
                try:
                    text = tweet['_source']['text']
                except KeyError:
                    text = None
    tokens = nltk.word_tokenize(text)
    return dictionary.doc2bow(tokens)


def main(num_topics):
    with og_reader.get_reader() as r:
        tweets = [extract_text(tweet) for tweet in r]
    dictionary = Dictionary(tweets)

    with og_reader.get_reader() as r:
        model = gensim.models.LdaMulticore((dictionary.doc2bow(tweet) for tweet in tweets), num_topics=num_topics)
    return model


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    num_topics = int(args['<num_topics>'])
    model = main(num_topics)
