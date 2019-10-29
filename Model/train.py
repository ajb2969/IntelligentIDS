from __future__ import print_function
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GaussianDropout, Activation, MaxPool2D

x_train_file = "../Data/x_train.csv"
x_test_file = "../Data/x_test.csv"
y_train_file = "../Data/y_train.csv"
y_test_file = "../Data/y_test.csv"


def import_data():
    x_train = np.genfromtxt(x_train_file, delimiter=',')
    x_test = np.genfromtxt(x_test_file, delimiter=',')
    y_train = np.genfromtxt(y_train_file, delimiter=',')
    y_test = np.genfromtxt(y_test_file, delimiter=',')
    return (x_train, y_train), (x_test, y_test)


maxlen = 30000
batch_size = 32
print('Loading data...')
(x_train, y_train), (x_test, y_test) = import_data()

# x_train = sequence.pad_sequences(x_train)
# x_test = sequence.pad_sequences(x_test)

print('Building model')
model = Sequential()
model.add(GaussianDropout(.2))
model.add(Activation("softmax"))
model.add(Embedding(8, 128, embeddings_initializer='uniform'))
model.add(LSTM(128, dropout=0.1, recurrent_dropout=0.1))
model.add(Dense(1, activation='sigmoid'))

# binary classification, adam optimizer worked the best
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Training model')
model.fit(x_train, y_train, batch_size=batch_size, epochs=5, validation_data=(x_test, y_test), workers=12, use_multiprocessing=True)
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)

print(model.summary())
print('Test score:', score)
print('Test accuracy:', acc)
