from tensorflow.keras import Sequential
from tensorflow.keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.python.util import deprecation
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import numpy as np
import pickle
import warnings
deprecation._PRINT_DEPRECATION_WARNINGS = False
warnings.filterwarnings("ignore")


def create_dataset(data_input, data_output, size):
    dataset_input = data_input.loc[:, ["GG Compr Press",
                                       "GG Speed Actual",
                                       "GG Inlet Vibr",
                                       "GG Center Vib",
                                       "T1 Avg",
                                       "T2 Avg",
                                       "T3 Avg",
                                       "T4 Avg",
                                       "T5 Avg",
                                       "T6 Avg",
                                       "T7 Avg",
                                       "T8 Avg"]]

    dataset_output = data_output

    scaler = MinMaxScaler(feature_range=(0, 1))

    dataset_input = scaler.fit_transform(dataset_input)
    dataset_output = scaler.fit_transform(dataset_output.reshape(-1, 1))

    train_size = int(len(dataset_input) * size)

    X_train = dataset_input[0:train_size]
    X_test = dataset_input[train_size:len(dataset_input)]
    Y_train = dataset_output[0:train_size]
    Y_test = dataset_output[train_size:len(dataset_input)]

    return X_train, X_test, Y_train, Y_test


def model_lstm(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

    model = Sequential()
    model.add(LSTM(32, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(16, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(8))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    history = model.fit(X_train,
                        Y_train,
                        validation_data=(X_test, Y_test),
                        epochs=10,
                        batch_size=10,
                        verbose=1,
                        shuffle=False,
                        callbacks=[EarlyStopping(monitor='val_loss', patience=10)])

    model.save('data/model_lstm.h5')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(history.history['accuracy'], label='Train Accuracy')
    ax.plot(history.history['val_accuracy'], label='Test Accuracy')
    ax.set_ylim(0, 1)
    ax.set_title('Model Accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epochs')
    ax.legend(loc='upper right')

    return model, fig


def model_cnn(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    history = model.fit(X_train,
                        Y_train,
                        validation_data=(X_test, Y_test),
                        epochs=10,
                        batch_size=10,
                        verbose=1,
                        shuffle=False,
                        callbacks=[EarlyStopping(monitor='val_loss', patience=10)])

    model.save('data/model_cnn.h5')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(history.history['accuracy'], label='Train Accuracy')
    ax.plot(history.history['val_accuracy'], label='Test Accuracy')
    ax.set_ylim(0, 1)
    ax.set_title('Model Accuracy')
    ax.set_ylabel('Accuracy')
    ax.set_xlabel('Epochs')
    ax.legend(loc='upper right')

    return model, fig


def model_logistic(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                               intercept_scaling=1, l1_ratio=None, max_iter=100,
                               multi_class='multinomial', n_jobs=None, penalty='l2',
                               random_state=41, tol=0.0001, verbose=0,
                               warm_start=False)

    model.fit(X_train, Y_train)

    cm = confusion_matrix(Y_test, model.predict(X_test))

    filename_model = "data/model_logistic.sav"
    pickle.dump(model, open(filename_model, 'wb'))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm, cmap='viridis')
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, round(cm[i, j] / np.sum(cm), 2), ha='center', va='center', color='red', size='15')

    return model, fig


def model_random_forest(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    model = RandomForestClassifier()

    model.fit(X_train, Y_train)

    cm = confusion_matrix(Y_test, model.predict(X_test))

    filename_model = "data/model_random_forest.sav"
    pickle.dump(model, open(filename_model, 'wb'))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm, cmap='viridis')
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, round(cm[i, j] / np.sum(cm), 2), ha='center', va='center', color='red', size='15')

    return model, fig


def model_svm(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    model = SVC(C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False,
                tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=- 1, decision_function_shape='ovr'
                , break_ties=False, random_state=None)

    model.fit(X_train, Y_train)

    cm = confusion_matrix(Y_test, model.predict(X_test))

    filename_model = "data/model_svm.sav"
    pickle.dump(model, open(filename_model, 'wb'))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm, cmap='viridis')
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, round(cm[i, j] / np.sum(cm), 2), ha='center', va='center', color='red', size='15')

    return model, fig

