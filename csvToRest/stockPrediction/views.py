from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
# Create your views here.
from .LSTM.run import lstmModel

def updateJsonFile(Data):
    jsonFile = open("./stockPrediction/LSTM/config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    ## Working with buffered content
    data["data"]["columns"] = Data["inputData"]
    data["data"]["sequence_length"] = Data["sequenceLength"]
    data["training"]["epochs"] = Data["epochs"]
    data["training"]["batch_size"] = Data["batchSize"]
    data["model"]["loss"] = Data["lossFunction"]
    data["model"]["optimizer"] = Data["optimizer"]

    ## Save our changes to JSON file
    jsonFile = open("./stockPrediction/LSTM/config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


class getPrediction(APIView):
    def get(self, request, symbol, model):
        try:
            lstm=lstmModel(symbol)
            lstm.generateData()
            lstm.loadModel(model)
            return Response({ symbol : lstm.predict(lstm.model)})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class trainModel(APIView):
    def get(self, request, symbol):
        lstm=lstmModel(symbol)
        lstm.generateData()
        lstm.build()
        
        return Response({ symbol : lstm.predict(lstm.model)})

class getConfig(APIView):
    def get(self, request):
        configs = json.load(open('./stockPrediction/LSTM/config.json', 'r'))
        return Response(configs)

    def put(self, request, format=None):
        try:
            print(request.data["inputData"])
            updateJsonFile(request.data)
            return Response(request.data)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    