# DeepLearning でタイムを予想する
import numpy as np
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras

EPOCHS = 100
graph = tf.get_default_graph()
VERSION = 1

# 引数 dataframe
def predict(x):
    graph = tf.get_default_graph()
    with graph.as_default():
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            model = load_model()
            return model.predict(x)

def load_model():
    return keras.models.load_model('machinelearning/ml_racer_pred_dl.pickle')

def fit(X, y):
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    model = build_model(X)
    graph = tf.get_default_graph()
    with graph.as_default():
        with tf.Session():
            history = model.fit(X, y, epochs=EPOCHS,
                            validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])
            model.save('machinelearning/ml_racer_pred_dl.pickle')

def build_model(_X):
    model = keras.Sequential([
        keras.layers.Dense(10, activation='elu', input_shape=[len(_X.keys())]),
        keras.layers.Dense(10, activation='elu'),
        keras.layers.Dense(10, activation='elu'),
        keras.layers.Dense(10, activation='elu'),
        keras.layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
    return model

class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0: print('')
        print('.', end='')
