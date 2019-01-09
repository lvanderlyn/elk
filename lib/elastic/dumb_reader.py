from contextlib import contextmanager

import elasticsearch
from elasticsearch import helpers


@contextmanager
def get_reader():
    """This generates a dumb reader which iterates over all the logstash indices
    (one per date) and retrieves all tweets.
    """

    def _reader(es, indices):
        for i in indices:
            yield from helpers.scan(es, index=i)

    # Assume elastic runs on localhost on the default port
    es = elasticsearch.Elasticsearch()
    # logstash indices start with "logstash-" by default
    indices = [x for x in es.indices.get_mapping().keys() if x.startswith('logstash')]
    # this can be used to gauge progress
    total_num_tweets = sum(es.search(i)['hits']['total'] for i in indices)

    yield _reader(es, indices)


if __name__ == '__main__':
    with get_reader() as r:
        for tweet in r:
            print(tweet)
