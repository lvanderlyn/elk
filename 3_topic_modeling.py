"""
Usage:
    3_topic_modeling <num_topics>
"""


import docopt
import gensim
import nltk

from lib.elastic import og_reader


def main(num_topics):
    with og_reader.get_reader() as r:
        model = gensim.models.LdaMulticore(r, num_topics=num_topics)
    return model


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    num_topics = int(args['<num_topics>'])
    model = main(num_topics)
