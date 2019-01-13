"""
Usage:
    3_topic_modeling <num_topics>
"""


import docopt
import gensim
from gensim.corpora.dictionary import Dictionary
import nltk

from lib.elastic import og_reader


def extract_text(lemmatizer, tweet):
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

    tokenized = nltk.word_tokenize(text.lower())
    tagged = nltk.pos_tag(tokenized)
    lemmatized = []
    for word, tag in tagged:
        try:
            lemma = lemmatizer.lemmatize(word, pos=tag[0].lower())
        except:
            lemma = lemmatizer.lemmatize(word)
        lemmatized.append(lemma)
    return list(filter(lambda x: not x.startswith('//t.co/'), lemmatized))


def main(num_topics):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    with og_reader.get_reader() as r:
        tweets = [extract_text(lemmatizer, tweet) for tweet in r]
    dictionary = Dictionary(tweets)

    with og_reader.get_reader() as r:
        model = gensim.models.LdaMulticore((dictionary.doc2bow(tweet) for tweet in tweets), num_topics=num_topics)
    return dictionary, model


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    num_topics = int(args['<num_topics>'])
    dictionary, model = main(num_topics)
