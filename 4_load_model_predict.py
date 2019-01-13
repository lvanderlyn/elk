"""
    Goes through the tweets in Elasticsearch and predicts tonality using the trained model.
    Updates the tweets with the predicted value.
"""

from elasticsearch import Elasticsearch, helpers
import json

from keras.preprocessing import text as txt, sequence
from keras.models import model_from_json
import numpy as np

# load dictionary saved during training to use it for converting text to number vectors
with open('emotions_model/dictionary.json', 'r') as dictionary_file:
    dictionary = json.load(dictionary_file)


def convert_text_to_index_array(text):
    words = txt.text_to_word_sequence(text)
    word_indices = []
    for word in words:
        if word in dictionary:
            word_indices.append(dictionary[word])
        else:
            print("'%s' not in training corpus; ignoring." % word)
    return word_indices


# imitates keras tokenizer used during training
def normalize_text(text):
    text = text.lower()
    filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    split = " "
    for c in filters:
        text = text.replace(c, split)
    return text


# def gen_data(tweets, index):
#     for t in tweets:
#         yield {
#             '_index': index,
#             '_op_type': 'update',
#             '_type': 'doc',
#             '_id': t[0],
#             'doc': {'tonality': t[1]},
#         }


def main():
    # load saved model
    with open('emotions_model/model.json', 'r') as f:
        loaded_model_json = f.read()

    model = model_from_json(loaded_model_json)
    model.load_weights('emotions_model/model.h5')

    es = Elasticsearch()
    indices = [x for x in es.indices.get_mapping().keys() if x.startswith('logstash')]
    labels = ['negative', 'positive']
    # updated_data = []
    try:
        for i in indices:
            print('index: ' + i)
            for tweet in helpers.scan(es, index=i):
                try:
                    tweet_text = tweet['_source']['extended_tweet']['full_text']
                except KeyError:
                    try:
                        tweet_text = tweet['_source']['extended_tweet']['text']
                    except KeyError:
                        try:
                            tweet_text = tweet['_source']['message']
                        except KeyError:
                            try:
                                tweet_text = tweet['_source']['text']
                            except KeyError:
                                tweet_text = None

                tweet_text = normalize_text(tweet_text)
                words = convert_text_to_index_array(tweet_text)
                words_pad = sequence.pad_sequences([words], maxlen=70)

                if len(words) > 0:
                    pred = model.predict(words_pad)

                    # predicted value - index of the max value
                    tonality = np.argmax(pred).item()
                    # updated_data.append((tweet['_id'], labels[tonality]))

                    es.update(index=i, doc_type="doc", id=tweet['_id'], body={'doc': {'tonality': labels[tonality]}})

                    print('message: ' + tweet_text + ', tonality: ' + labels[tonality])

    except Exception as e:
        print(e)

        # helpers.bulk(es, gen_data(updated_data, i))


if __name__ == '__main__':
    main()
