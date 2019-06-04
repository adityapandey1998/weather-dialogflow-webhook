    
#!/usr/bin/env python

import urllib
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
	print("Request = ")
	print(json.dumps(req, indent=4))
	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r=make_response(res)
	r.headers['Content-Type'] = 'application/json'
	
	return r

def makeWebhookResult(req):
	if req.get('queryResult').get('action') in ['WeatherInfo_context','WeatherInfo']:
		#result = req.get('queryResult')
		#parameters = result.get('parameters')
		#speech ="The interest rate of "
		#print('Response:')
		#print(speech)
		return  {
			"fulfillmentText": "Weather Information",
			'source' : 'InterestRate'
		}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
