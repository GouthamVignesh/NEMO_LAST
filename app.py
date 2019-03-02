from __future__ import print_function
from future.standard_library import install_aliases

install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import wolframalpha
import wikipedia
import requests
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify,request
import random

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    res = processRequest(req)
    print(res)
    return make_response(jsonify({'fulfillmentText':res}))

def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access.
    speech = ""
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'
    if action == "input.unknown":
        my_input = req.get('queryResult').get('queryText').lower()
        if ("news" in my_input) or ("top headlines" in my_input) or ("headlines" in my_input):
            x = news()
            speech = "" + x + ""
            res = makeWebhookResult(speech)
        else:
            try:
                app_id = "R2LUUJ-QTHXHRHLHK"
                client = wolframalpha.Client(app_id)
                r = client.query(my_input)
                answer = next(r.results).text
                speech = "" + answer + ""
                res = makeWebhookResult(speech)
            except:
                my_input = my_input.split(' ')
                my_input = " ".join(my_input[2:])
                answer = wikipedia.summary(my_input, sentences=2)
                speech = "" + answer + ""
                res = makeWebhookResult(speech)
    else:
        speech = "no input"
        res = makeWebhookResult(speech)
    return res

def makeWebhookResult(speech):
    return speech
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
