"""
Usage:
    2_classifier dt <corpus_path>
    2_classifier nb <corpus_path>

Options:
    -d <int>  max depth
"""


import docopt
import elasticsearch
import nltk
from sklearn.model_selection import cross_validate

from lib.classifiers import decision_tree
from lib.classifiers import naive_bayes


def read_corpus(lemmatizer, path):
    """Returns the tokenized corpus is a list and a numerical mapping
    for every word in the corpus.
    """
    corpus = []
    dictionary = {}
    with open(path) as handle:
        for line in handle:
            label, tweet = line.strip().split('\t')
            index, id, text = eval(tweet)

            tokenized = nltk.word_tokenize(text.lower())
            tagged = nltk.pos_tag(tokenized)
            lemmatized = []
            for word, tag in tagged:
                try:
                    lemma = lemmatizer.lemmatize(word, pos=tag[0].lower())
                except:
                    lemma = lemmatizer.lemmatize(word)
                lemmatized.append(lemma)

            lemmatized += get_bigrams(lemmatized)

            for word in lemmatized:
                if word not in dictionary:
                    dictionary[word] = len(dictionary)
            corpus.append((index, id, lemmatized, label))
    return corpus, dictionary


def get_bigrams(seq):
    return [tuple(seq[i:i+2]) for i in range(len(seq)-1)]


def get_features(tweet, dictionary):
    """Creates numerical features from the words of the tweet"""
    features = {i: 0 for i in range(len(dictionary))}
    for word in tweet:
        features[dictionary[word]] += 1
    return [v for k, v in sorted(features.items())]


def get_username(el, index, id):
    x = el.get(index, '_all', id)
    x = x['_source']['user']
    if isinstance(x, str):
        return x
    else:
        x['screen_name']


def main(args):
    el = elasticsearch.Elasticsearch()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    raw_corpus, dictionary = read_corpus(lemmatizer, args['<corpus_path>'])
    corpus = []
    for tweet in raw_corpus:
        index, id, words, label = tweet
        username = get_username(el, index, id)
        corpus.append((index, id, username, words, label))
        if username not in dictionary:
            dictionary[username] = len(dictionary)
        
    features, labels = zip(*[(get_features(tweet, dictionary), label) for index, id, username, tweet, label in corpus])
    if args['dt']:
        model = decision_tree.train(features, labels)
    elif args['nb']:
        model = naive_bayes.train(features, labels)

    scores = cross_validate(model, features, labels, cv=10, return_train_score=True)
    print(f"train_scores: {scores['train_score']}")
    print(f"test_scores:  {scores['test_score']}")

    # print(decision_tree.get_visualization(model))


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    model = main(args)
