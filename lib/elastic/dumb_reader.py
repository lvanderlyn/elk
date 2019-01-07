from contextlib import contextmanager

import elasticsearch
from elasticsearch import helpers


@contextmanager
def reader():
    """This dumb reader iterates over all the logstash indices (one per date)
    and retrieves all tweets.
    """

    def _reader(es):
        for i in indices:
            yield from helpers.scan(es, index=i)

    # Assume elastic runs on localhost on the default port
    es = elasticsearch.Elasticsearch()
    # select all indices that start with "logstash"
    indices = [x for x in es.indices.get_mapping().keys() if x.startswith('logstash')]

    yield _reader(es)


if __name__ == '__main__':
    with reader() as r:
        for line in r:
            print(line)
