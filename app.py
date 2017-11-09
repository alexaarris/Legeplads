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

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    docpart = req.get("result").get("parameters").get("docpart")
    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + docpart + "')"
    yql_url = "https://query.yahooapis.com/v1/public/yql?" + urlencode({'q': yql_query}) + "&format=json"
    data = json.loads(urlopen(yql_url).read())
    res = makeWebhookResult(data, req)
    return res

def makeWebhookResult(data, req):
    docpart = req.get("result").get("parameters").get("docpart")
    unitsales = req.get("result").get("parameters").get("unitsales")
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
