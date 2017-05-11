#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import base64
import json
import os
from textblob import TextBlob

from flask import Flask
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
    if req.get("result").get("action") == "help.emotion.info":
        result = req.get("result")
        parameters = result.get("parameters")
        query = parameters.get("any")
        score = sentimentAnalysis(query)
        if score < -0.3:
            res = makeEmotionSadWebhookResult()
        else:
            res = makeEmotionHappyWebhookResult()
    elif req.get("result").get("action") == "help.learning.info":
        res = makeLearningWebhookResult()
      
    return res


def sentimentAnalysis(query):
    sentiment = TextBlob(query)
    score = sentiment.polarity
    return score

def learningRecomendation(req):
    query =  req.get("result").get("parameters").get("skills")
    #function for learning recomendation and response back with details




def makeEmotionSadWebhookResult():
    
    speech = "Webhook result: I understand this, let look at this video. It will help you. https://www.youtube.com/watch?v=LrhSJ1FHeaA"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }
def makeEmotionHappyWebhookResult():
    
    speech = "Webhook result: Glad to know that you are happy."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
    }
def makeLearningWebhookResult():
    
    speech = "learning Webhook result"

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
