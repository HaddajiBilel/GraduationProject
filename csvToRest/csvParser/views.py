from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import csv, json
import os
from .CalculateInd import addIndicators
# Create your views here.



def getJsonFromCSV(csvPath, csvSymbol, size):
    print('converting ' + csvSymbol + ' data ...')
    data=[]
    with open(csvPath + csvSymbol+".csv") as File:
        csvReader = csv.DictReader(File)
        for rows in csvReader:
            data.append(rows)
            if (size == len(data)):
                break
    
    return data


def updateCSV(csvPath, csvSymbol):  
    print('fetching ' + csvSymbol + ' data ...')
    api_key='H579PUKW0SVGRIK9'
    url ="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=" + csvSymbol + "&apikey=" + api_key + "&datatype=csv"
    r = requests.get(url, allow_redirects=True)
    os.makedirs(os.path.dirname(csvPath + csvSymbol + '.csv'), exist_ok=True)
    open(csvPath + csvSymbol + '.csv', 'wb').write(r.content)


class GetStockList(APIView):
    def get(self, request):
        directories=[]
        jsonResult=[]
        for dirpath, dirname, filename in os.walk("./data"):
            directories.append(dirname)
        for directory in directories[0]:
            
            jsonResult.append({"symbol" :directory})
        return Response(jsonResult)

class getModels(APIView):
    
    def get(self, request, symbol):
        Models=[]
        files= os.listdir("./data/" + symbol)
        for file in files:
            if (file.endswith('.h5')):
                Models.append({"model" :file})
        return Response(Models)        


class GetData(APIView):
    def get(self, request, symbol, size=None):
        csvFilesPath="./data/" + symbol + "/"
        return Response(getJsonFromCSV(csvPath=csvFilesPath ,csvSymbol=symbol, size=size))

class UpdateCreateData(APIView):
    def get(self, request, symbol):
        csvFilesPath="./data/" + symbol + "/"
        updateCSV(csvPath=csvFilesPath ,csvSymbol=symbol)
        addIndicators(path=csvFilesPath, symbol=symbol)
        return Response({symbol: "Updated successfully and Indicators created"})

class GetIndicators(APIView):
    def get(self, request, symbol, size=None):
        csvFilesPath="./data/" + symbol + "/"
        return Response(getJsonFromCSV(csvPath=csvFilesPath ,csvSymbol=symbol+"Indicators", size=size))