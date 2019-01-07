"""
Usage: generate_annotation_samples -n STR -k INT

Options:
    -n STR  annotator ID (use 1,2,3,... or names or whatever)
    -k INT  number of samples

The annotator ID is used as a seed for random to produce reproducible samples.
This does not guarantee non-overlapping samples when used three times with
individual annotator IDs. If you want to ensure that, use a single annotator
ID and set -k to "number of samples" * "annotators".
"""

import random

import docopt

from lib.elastic import dumb_reader


random.seed(42)


def get_sample(n, k):
    random.seed(n)

    with dumb_reader.reader() as r:
        tweets = list(r)
    
    sample = random.sample(tweets, k)

    return [(x['_id'], x['_source'].get('message')) for x in sample]


if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    annotator_id = args['-n']
    number_of_samples = int(args['-k'])

    for x in get_sample(annotator_id, number_of_samples):
        print(x)
