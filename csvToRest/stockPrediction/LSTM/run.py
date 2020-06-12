import os
import json
import time
import math
import matplotlib.pyplot as plt
from .core.data_processor import DataLoader
from .core.model import Model


def trend(stockdata):
    UpDown=[]
    for i in range(len(stockdata)-1):
        if stockdata[i] > stockdata[i+1]: UpDown.append('down')
        else: UpDown.append('Up')
    return UpDown


def prediction_errors(true_trend, predicted_trend):
    err = []
    right = 0
    wrong = 0
    for i in range(len(true_trend)):
        if true_trend[i] == predicted_trend[i]:
            err.append('true')
            right = right+1
        else:
            err.append('false')
            wrong = wrong + 1

    return right, wrong


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    true_trend = trend(true_data)
    predicted_trend = trend(predicted_data)
    print(prediction_errors(true_trend, predicted_trend))
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
	# Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        if data[0]>data[-1]: print('down')
        else: print('up')
        plt.legend()
    plt.show()


def main():
    configs = json.load(open('./stockPrediction/LSTM/config.json', 'r'))  #csvToRest\stockPrediction\LSTM\config.json
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])

    data = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns']
    )

    model = Model()
    model.build_model(configs)
    x, y = data.get_train_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    # out-of memory generative training
    steps_per_epoch = math.ceil((data.len_train - configs['data']['sequence_length']) / configs['training']['batch_size'])
    model.train_generator(
        data_gen=data.generate_train_batch(
            seq_len=configs['data']['sequence_length'],
            batch_size=configs['training']['batch_size'],
            normalise=configs['data']['normalise']
        ),
        epochs=configs['training']['epochs'],
        batch_size=configs['training']['batch_size'],
        steps_per_epoch=steps_per_epoch,
        save_dir=configs['model']['save_dir']
    )

    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    predictions = model.predict_sequences_multiple(x_test, configs['data']['sequence_length'], configs['data']['sequence_length'])
    #predictions = model.predict_sequence_full(x_test, configs['data']['sequence_length'])
    #predictions = model.predict_point_by_point(x_test)
    #print(predictions)
    plot_results_multiple(predictions, y_test, configs['data']['sequence_length'])
    #plot_results(predictions, y_test)


if __name__ == '__main__':
    main()