from __future__ import print_function
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM

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


max_features = 20000
maxlen = 12000
batch_size = 64
print('Loading data...')
(x_train, y_train), (x_test, y_test) = import_data()

#x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
#x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
#print('x_train shape:', x_train.shape)
#print('x_test shape:', x_test.shape)

print('Building model')
model = Sequential()
model.add(Embedding(max_features, 256))
model.add(LSTM(256, dropout=0.1, recurrent_dropout=0.1))
model.add(Dense(1, activation='sigmoid'))

#binary classification, adam optimizer worked the best
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Training model')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=5,
          validation_data=(x_test, y_test))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
