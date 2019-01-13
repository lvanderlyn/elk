"""
Usage:
    2_classifier dt <corpus_path>
    2_classifier nb <corpus_path>

Options:
    -d <int>  max depth
"""


import docopt
import nltk
from sklearn.model_selection import cross_validate

from lib.classifiers import decision_tree
from lib.classifiers import naive_bayes


def read_corpus(path):
    """Returns the tokenized corpus is a list and a numerical mapping
    for every word in the corpus.
    """
    corpus = []
    dictionary = {}
    with open(path) as handle:
        for line in handle:
            label, tweet = line.strip().split('\t')
            tweet = eval(tweet)[2]
            words = nltk.word_tokenize(tweet)
            for word in words:
                if word not in dictionary:
                    dictionary[word] = len(dictionary)
            corpus.append((words, label))
    return corpus, dictionary


def get_features(tweet, dictionary):
    """Creates numerical features from the words of the tweet"""
    features = {i: 0 for i in range(len(dictionary))}
    for word in tweet:
        features[dictionary[word]] += 1
    return [v for k, v in sorted(features.items())]


def main(args):
    corpus, dictionary = read_corpus(args['<corpus_path>'])
    features, labels = zip(*[(get_features(tweet, dictionary), label) for tweet, label in corpus])
    if args['dt']:
        model = decision_tree.train(features, labels)
    elif args['nb']:
        model = naive_bayes.train(features, labels)

    print(decision_tree.get_visualization(model))


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    model = main(args)
