__author__ = "Jakob Aungiers"
__copyright__ = "Jakob Aungiers 2018"
__version__ = "2.0.0"
__license__ = "MIT"

import os
import json
import time
import math
import matplotlib.pyplot as plt
from .core.data_processor import DataLoader
from .core.model import Model

class lstmModel():
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.configs = json.load(open('./stockPrediction/LSTM/config.json', 'r'))
        self.model = Model()


    def loadModel(self):
        self.model.load_model(filepath="./saved_models/"+self.name+".h5")
    

    def predict(self, model):
        self.predictions = model.predict_sequences_multiple(self.x_test, self.configs['data']['sequence_length'], self.configs['data']['sequence_length'])
        # predictions = model.predict_sequence_full(x_test, configs['data']['sequence_length'])
        # predictions = model.predict_point_by_point(x_test)

        #self.plot_results_multiple(self.predictions, self.y_test, self.configs['data']['sequence_length'])
        # plot_results(predictions, y_test)
        flat_list=[]
        for sublist in self.predictions:
            for item in sublist:
                flat_list.append(item)
        print(flat_list)
        jsonPrediction=[]
        i=0
        for date in self.x_test.tolist():
            try:
                jsonPrediction.append({"%s" %date :flat_list[i]})
                i=i+1
            except:
                pass
            
        return flat_list




    def generateData(self):
        print(os.path.join(os.getcwd(), 'data', self.name, self.name+'.csv')) 
        self.data = DataLoader(
            os.path.join(os.getcwd(), 'data', self.name, self.name + '.csv'),
            self.configs['data']['train_test_split'],
            self.configs['data']['columns']
        )

        self.generatedData=self.data.generate_train_batch(
                seq_len=self.configs['data']['sequence_length'],
                batch_size=self.configs['training']['batch_size'],
                normalise=self.configs['data']['normalise']
            )
        self.x_test, self.y_test = self.data.get_test_data(
            seq_len=self.configs['data']['sequence_length'],
            normalise=self.configs['data']['normalise']
        )

        x, y = self.data.get_train_data(
            seq_len=self.configs['data']['sequence_length'],
            normalise=self.configs['data']['normalise']
        )


    def build(self):

        if not os.path.exists(self.configs['model']['save_dir']): os.makedirs(self.configs['model']['save_dir'])

        self.model.build_model(self.configs)
        
        # out-of memory generative training
        steps_per_epoch = math.ceil((self.data.len_train - self.configs['data']['sequence_length']) / self.configs['training']['batch_size'])
        self.model.train_generator(
            data_gen=self.generatedData,
            epochs=self.configs['training']['epochs'],
            batch_size=self.configs['training']['batch_size'],
            steps_per_epoch=steps_per_epoch,
            save_dir=self.configs['model']['save_dir'],
            symbol=self.name
        )

        return self.model
    


    def plot_results(self, predicted_data, true_data):
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        ax.plot(true_data, label='True Data')
        plt.plot(predicted_data, label='Prediction')
        plt.legend()
        plt.show()


    def plot_results_multiple(self, predicted_data, true_data, prediction_len):
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        ax.plot(true_data, label='True Data')
        # Pad the list of predictions to shift it in the graph to it's correct start
        for i, data in enumerate(predicted_data):
            padding = [None for p in range(i * prediction_len)]
            plt.plot(padding + data, label='Prediction')
            plt.legend()
        plt.show()




