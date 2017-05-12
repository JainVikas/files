#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import urllib3
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import base64
import json
import os
from textblob import TextBlob

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
        if skills is None or education is None or userid is None :
            skills = parameters.get("skills")
            education = parameters.get("education")
            userid = parameters.get("userid")
            #if skills is not None and education is not None and userid is not None :
           # res = makeLearningWebhookResult(skills, education, userid)
    return {
        "speech": skills,
        "displayText": skills,
        # "data": data,
        # "contextOut": [],
    }



def sentimentAnalysis(query):
    sentiment = TextBlob(query)
    score = sentiment.polarity
    return score

def learningRecomendation(skills, education, userid):
    
    return skills

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
    
    speech = skills
    #learningRecomendation(skills, education, userid)

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
