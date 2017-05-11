#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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
    speech = "learning Webhook result"

    print("Response:")
    print(speech)
    print("hello from heroku")

    res =  {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
        }
   # res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    res = 0
    if req.get("result").get("action") != "help.emotion.info":
        return{}
    res = makeEmotionWebhookResult()
   # elif req.get("result").get("action") == "help.learning.info":
    # { score = learningRecomendation(req)
     #   res = makeLearningWebhookResult()
       }
    return res


def sentimentAnalysis(req):
    query =  req.get("result").get("resolvedQuery")
    data = urllib.parse.urlencode({"text": query }).encode("utf-8")
    req = urllib.request.Request("http://text-processing.com/api/sentiment/", data)
    with urllib.request.urlopen(req) as response:
    score = response.read()
    obj = json.loads(the_page)
    senti = obj.get("probability")
    print(senti.get("pos")) 
    return score

def learningRecomendation(req):
    query =  req.get("result").get("parameters").get("skills")
    #function for learning recomendation and response back with details




def makeEmotionWebhookResult():
    speech = "Webhook result: I understand this, let look at this video. It will help you. https://www.youtube.com/watch?v=LrhSJ1FHeaA"
    print("Response:")
    print(speech)

    return {
        "speech": webhook,
        "displayText": webhook,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
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
        "source": "apiai-weather-webhook-sample"
        }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
