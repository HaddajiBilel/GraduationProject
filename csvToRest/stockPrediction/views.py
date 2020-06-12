from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from .LSTM.run import lstmModel


class getPrediction(APIView):
    def get(self, request, symbol):
        lstm=lstmModel(symbol)
        lstm.generateData()
        lstm.loadModel()
        
        return Response({ symbol : lstm.predict(lstm.model)})


class trainModel(APIView):
    def get(self, request, symbol):
        lstm=lstmModel(symbol)
        lstm.generateData()
        lstm.build()
        
        return Response({ symbol : lstm.predict(lstm.model)})