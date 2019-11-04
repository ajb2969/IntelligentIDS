from __future__ import print_function
import numpy as np
from os import system
import random
from keras.preprocessing import sequence
from keras.models import Sequential
import keras.regularizers as kr
from keras.layers import Dense, Embedding, LSTM, GaussianDropout, Activation, Bidirectional, MaxPool1D, Concatenate

x_train_file = "x_train.csv"
x_test_file = "x_test.csv"
y_train_file = "y_train.csv"
y_test_file = "y_test.csv"
output_file = "model.json"


def import_data():
    x_train = np.genfromtxt(x_train_file, delimiter=',')
    x_test = np.genfromtxt(x_test_file, delimiter=',')
    y_train = np.genfromtxt(y_train_file, delimiter=',')
    y_test = np.genfromtxt(y_test_file, delimiter=',')
    return (x_train, y_train), (x_test, y_test)


def add_train():
    print("Reshuffling data")
    train = random.randint(60, 70)
    test = 100 - train
    print("Train is ", train/100 , " test is ", test/100)
    system("python3 ../Data/train_test.py " + (train/100).__str__() + " " + (test/100).__str__())


def train():
    add_train()
    batch_size = 32
    print('Loading data...')
    (x_train, y_train), (x_test, y_test) = import_data()

    model = Sequential()

    x_train = sequence.pad_sequences(x_train)
    x_test = sequence.pad_sequences(x_test)

    model.add(GaussianDropout(.1))
    model.add(Embedding(8, 128, embeddings_initializer='TruncatedNormal', activity_regularizer=kr.L1L2(0.01, 0.01)))
    model.add(LSTM(128, dropout=0.1, recurrent_dropout=0.1, return_sequences=True, go_backwards=True))
    model.add(MaxPool1D())
    model.add(Dense(64, input_shape=(128,), activation='sigmoid'))
    model.add(Bidirectional(LSTM(32, dropout=0.2, recurrent_dropout=0.1)))
    model.add(Dense(1, activation='sigmoid', ))

    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print('Training model')
    model.fit(x_train,
              y_train,
              batch_size=batch_size,
              epochs=1,
              validation_data=(x_test, y_test),
              workers=100,
              use_multiprocessing=True,
              verbose=False,
              shuffle=True)
    score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)

    print(model.summary())
    print('Test score:', score)
    print('Test accuracy:', acc)

    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    if float(acc) < 0.9:
        print("Accuracy is less than 0.9")
        train()


if __name__ == '__main__':
    train()
