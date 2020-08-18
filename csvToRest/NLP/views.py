from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import nltk
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import csv
import pandas as pd


from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pprint

# Create your views here

def patchLexicon():
    print("Patching Vader with financial Lexicon")
    sia = SentimentIntensityAnalyzer()
    # # stock market lexicon
    stock_lex = pd.read_csv('NLP/lexicon_data/stock_lex.csv')
    stock_lex['sentiment'] = (stock_lex['Aff_Score'] + stock_lex['Neg_Score'])/2
    stock_lex = dict(zip(stock_lex.Item, stock_lex.sentiment))
    stock_lex = {k:v for k,v in stock_lex.items() if len(k.split(' '))==1}
    #print(stock_lex.items())
    stock_lex_scaled = {}
    for k, v in stock_lex.items():
        if v > 0:
            stock_lex_scaled[k] = v / max(stock_lex.values()) * 4
        else:
            stock_lex_scaled[k] = v / min(stock_lex.values()) * -4
    # Loughran and McDonald
    positive = []
    with open('NLP/lexicon_data/lm_positive.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            positive.append(row[0].strip())

    negative = []
    with open('NLP/lexicon_data/lm_negative.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            entry = row[0].strip().split(" ")
            if len(entry) > 1:
                negative.extend(entry)
            else:
                negative.append(entry[0])

    final_lex = {}
    final_lex.update({word:2.0 for word in positive})
    final_lex.update({word:-2.0 for word in negative})
    final_lex.update(stock_lex_scaled)
    final_lex.update(sia.lexicon)
    sia.lexicon = final_lex
    return sia
    

class getsentiments(APIView):
    model=patchLexicon()
    def get(self, request, symbol):
        try:
            #print("Hi there")
            date_sentiments = {}

            for i in range(1,3):
                print(i)
                page = urlopen('https://www.businesstimes.com.sg/search/facebook?page='+str(i)).read()
                soup = BeautifulSoup(page, features="html.parser")
                posts = soup.findAll("div", {"class": "media-body"})
                for post in posts:
                    time.sleep(1)
                    url = post.a['href']
                    date = post.time.text
                    title = post.a.getText()
                    #print(date, url)
                    try:
                        link_page = urlopen(url).read()
                        
                    except:
                        url = url[:-2]
                        link_page = urlopen(url).read()
                    link_soup = BeautifulSoup(link_page)
                    sentences = link_soup.findAll("p")
                    passage = ""
                    for sentence in sentences:
                        passage += sentence.text
                    
                    sentiment = self.model.polarity_scores(passage)
                    date_sentiments.setdefault(date, []).append([title, sentiment])
                #print(date_sentiments)
            date_sentiment = {}
            #print(date_sentiments)

            #print(date_sentiment)
    
            return Response(date_sentiments)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

