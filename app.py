#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response, jsonify

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
	return "Hi, there"


@app.route('/webhook', methods=['POST'])
def webhook():
    #req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))
    req = {}
    res = processRequest(req)
    # print(res)
    r = make_response(jsonify(res))
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
	#result = req.get('result')
	#parameters = result.get('parameters')
	speech ="This is a response from the webhook"
	print('Response:')
	print(speech)

	return  {
		'speech': speech,
		'displayText': speech
	}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
