# to train the model training data and word embeddings are needed

import pandas as pd
import numpy as np
from tqdm import tqdm
import json

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

from keras.preprocessing import sequence, text
from keras.models import Sequential
from keras.layers import Bidirectional, SpatialDropout1D
from keras.layers.core import Dense, Activation, Dropout
from keras.callbacks import EarlyStopping
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding


def load_embeddings():
    # load pre-trained word embeddings (GloVe, twitter)
    embeddings_index = {}
    with open('glove.twitter.27B/glove.twitter.27B.25d.txt') as f:
        for line in f:
            values = line.split()
            word = values[0]

            try:
                coefs = np.asarray(values[1:], dtype='float32')
            except:
                pass

            embeddings_index[word] = coefs

    return embeddings_index


# load test and training data
train_data = pd.read_csv("text_emotion.csv", encoding='latin-1')

# split data and labels into training and validation sets
xtrain, xvalid, ytrain, yvalid = train_test_split(train_data.content.values, train_data.sentiment.values,
                                                  stratify=train_data.sentiment.values,
                                                  random_state=42, test_size=0.1, shuffle=True)

lb = LabelBinarizer()
lb.fit(ytrain)
train_Y_bi = lb.fit_transform(ytrain)
valid_Y_bi = lb.fit_transform(yvalid)

token = text.Tokenizer(num_words=None)
# build dictionary with indices based on texts
token.fit_on_texts(list(xtrain) + list(xvalid))
# represent texts as sequence of indices
xtrain_seq = token.texts_to_sequences(xtrain)
xvalid_seq = token.texts_to_sequences(xvalid)

# zero pad the sequences to make sure they are of the same length
max_len = 70
xtrain_pad = sequence.pad_sequences(xtrain_seq, maxlen=max_len)
xvalid_pad = sequence.pad_sequences(xvalid_seq, maxlen=max_len)

word_index = token.word_index
# save dictionary to use it for prediction
with open('dictionary.json', 'w') as dictionary_file:
    json.dump(word_index, dictionary_file)

# create an embedding matrix for the words we have in the dataset
embeddings_index = load_embeddings()  # load GloVe embeddings
embedding_matrix = np.zeros((len(word_index) + 1, 25))
for word, i in tqdm(word_index.items()):
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# a bidirectional LSTM with two dense layers
model = Sequential()
# turns indices into embedding vectors
model.add(Embedding(len(word_index) + 1, 25, weights=[embedding_matrix], input_length=max_len, trainable=False))
model.add(SpatialDropout1D(0.3))
model.add(Bidirectional(LSTM(300, dropout=0.3, recurrent_dropout=0.3)))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.8))

model.add(Dense(13))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model with early stopping callback
earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')

model.fit(xtrain_pad, y=train_Y_bi, batch_size=512, epochs=10,
          verbose=1, validation_data=(xvalid_pad, valid_Y_bi), callbacks=[earlystop])  # accuracy 0.7348 (stopped at epoch 19)

# save the model
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights('model.h5')
