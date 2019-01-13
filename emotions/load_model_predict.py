from elasticsearch import Elasticsearch, helpers
import json

from keras.preprocessing import text as txt, sequence
from keras.models import model_from_json
import numpy as np

with open('dictionary.json', 'r') as dictionary_file:
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


# load saved model
with open('model.json', 'r') as f:
    loaded_model_json = f.read()

model = model_from_json(loaded_model_json)
model.load_weights('model.h5')

es = Elasticsearch()
indices = [x for x in es.indices.get_mapping().keys() if x.startswith('logstash')]
labels = ['negative', 'positive']
for i in indices:
    print('index: ' + i)
    for tweet in helpers.scan(es, index=i):
        if 'message' in tweet['_source']:
            tweet_text = tweet['_source']['message']
        else:
            tweet_text = tweet['_source']['text']

        words = convert_text_to_index_array(tweet_text)
        words_pad = sequence.pad_sequences([words], maxlen=70)

        if len(words) > 0:
            pred = model.predict(words_pad)

            # predicted value - index of the max value
            tonality = np.argmax(pred).item()

            try:
                res = es.update(index=i, doc_type="doc", id=tweet['_id'], body={'doc': {'tonality': labels[tonality]}})

                print('message: ' + tweet_text + ', tonality: ' + labels[tonality])
            except Exception as e:
                print(e)
