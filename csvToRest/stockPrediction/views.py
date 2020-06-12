from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from .LSTM.run import main


class getPrediction(APIView):
    def get(self, request, symbol):
        main()
        return Response({"pred": "somedata"})