import os
import numpy as np
from nltk.corpus import stopwords

stop_words = stopwords.words('english')


def load_embeddings():
    # load pre-trained word embeddings (GloVe, twitter)
    embeddings_index = {}
    for fn in os.listdir('glove.twitter.27B'):
        with open('glove.twitter.27B/' + fn) as f:
            for line in f:
                values = line.split()
                word = values[0]

                try:
                    coefs = np.asarray(values[1:], dtype='float32')
                except:
                    pass

                embeddings_index[word] = coefs

    return embeddings_index
