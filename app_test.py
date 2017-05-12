#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import urllib3
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming 
import base64
import json
import os
from textblob import TextBlob
import pandas as pd
import warnings
from flask import Flask, render_template
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    res = 0
    result = req.get("result")
    parameters = result.get("parameters")
    if req.get("result").get("action") == "help.emotion.info":
        query = parameters.get("any")
        score = sentimentAnalysis(query)
        if score < -0.3:
            res = makeEmotionSadWebhookResult()
        else:
            res = makeEmotionHappyWebhookResult()
    elif req.get("result").get("action") == "help.learning.info":
        skills = parameters.get("skills")[0]
        education = parameters.get("education")[0]
        userid = parameters.get("userid")[0]
        if skills is not None and education is not None and userid is not None:
            res = makeLearningWebhookResult(skills, education, userid)
    return res



def sentimentAnalysis(query):
    sentiment = TextBlob(query)
    score = sentiment.polarity
    return score
def bookMeta(isbn):
    title = books.at[isbn,"title"]
    author = books.at[isbn,"author"]
    return title, author
def faveBooks(user,N):
    userRatings = data[data["user"]==user]
    sortedRatings = pd.DataFrame.sort_values(userRatings,['rating'],ascending=[0])[:N] 
    sortedRatings["title"] = sortedRatings["isbn"].apply(bookMeta)
    return sortedRatings
def distance(user1,user2):
        try:
            user1Ratings = userItemRatingMatrix.transpose()[user1]
            user2Ratings = userItemRatingMatrix.transpose()[user2]
            distance = hamming(user1Ratings,user2Ratings)
        except: 
            distance = np.NaN
        return distance 
def nearestNeighbors(user,K=10):
    allUsers = pd.DataFrame(userItemRatingMatrix.index)
    allUsers = allUsers[allUsers.user!=user]
    allUsers["distance"] = allUsers["user"].apply(lambda x: distance(user,x))
    KnearestUsers = allUsers.sort_values(["distance"],ascending=True)["user"][:K]
    return KnearestUsers
def topN(user,N=3):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
   
        KnearestUsers = nearestNeighbors(user)
        NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)]
        avgRating = NNRatings.apply(np.nanmean).dropna()
        booksAlreadyRead = userItemRatingMatrix.transpose()[user].dropna().index
        avgRating = avgRating[~avgRating.index.isin(booksAlreadyRead)]
        topNISBNs = avgRating.sort_values(ascending=False).index[:N]
        return pd.Series(topNISBNs).apply(bookMeta)

KnearestUsers = nearestNeighbors(user)
def learningRecomendation(skills, education, userid):
	import pandas as pd
	dataFile='BX-Books-Ratings.csv'
	data=pd.read_csv(dataFile,sep=";",header=0,names=["user","isbn","rating"], encoding='latin-1')

	bookFile='BX-Books.csv'
	books=pd.read_csv(bookFile,sep=";",header=0,error_bad_lines=False, usecols=[0,1,2],index_col=0,names=['isbn',"title","author"],encoding='latin-1')

	data = data[data["isbn"].isin(books.index)]
	usersPerISBN = data.isbn.value_counts()
	ISBNsPerUser = data.user.value_counts()
	data = data[data["isbn"].isin(usersPerISBN[usersPerISBN>10].index)]
	data = data[data["user"].isin(ISBNsPerUser[ISBNsPerUser>10].index)]
	userItemRatingMatrix=pd.pivot_table(data, values='rating',index=['user'], columns=['isbn'])
	user = userid
	allUsers = pd.DataFrame(userItemRatingMatrix.index)
	allUsers = allUsers[allUsers.user!=user]
	KnearestUsers = nearestNeighbors(user)
	NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)]
	with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    avgRating = NNRatings.apply(np.nanmean).dropna()
	booksAlreadyRead = userItemRatingMatrix.transpose()[user].dropna().index
	booksAlreadyRead
	avgRating = avgRating[~avgRating.index.isin(booksAlreadyRead)]
	N=3
	topNISBNs = avgRating.sort_values(ascending=False).index[:N]
	pd.Series(topNISBNs).apply(bookMeta)
	speech = topN(204813,1)
    return speech

def makeEmotionSadWebhookResult():
    
    speech = "I understand this, let look at this video. It will help you. https://www.youtube.com/watch?v=LrhSJ1FHeaA"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }
def makeEmotionHappyWebhookResult():
    
    speech = "Glad to know that you are happy."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }

def makeLearningWebhookResult(skills, education, userid):
    
    speech = learningRecomendation(skills, education, userid)

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
