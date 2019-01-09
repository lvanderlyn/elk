from contextlib import contextmanager

import elasticsearch
from elasticsearch import helpers


@contextmanager
def get_reader():
    """This returns a reader which iterates over all the logstash indices
    (one per date) and retrieves all tweets that are not retweets.
    """

    def _reader(es, indices):
        for i in indices:
            # One could probably write an elastic query to eliminate retweets
            for tweet in helpers.scan(es, index=i):
                retweeted = tweet['_source'].get('retweeted_status', False)
                if not retweeted:
                    try:
                        retweeted = tweet['_source']['message'].startswith('RT ')
                    except KeyError:
                        pass
                if not retweeted:
                    yield tweet

    # Assume elastic runs on localhost on the default port
    es = elasticsearch.Elasticsearch()
    # logstash indices start with "logstash-" by default
    indices = [x for x in es.indices.get_mapping().keys() if x.startswith('logstash')]
    indices.sort()
    # this can be used to gauge progress
    total_num_tweets = sum(es.search(i)['hits']['total'] for i in indices)

    yield _reader(es, indices)


if __name__ == '__main__':
    with get_reader() as r:
        for tweet in r:
            print(tweet)
