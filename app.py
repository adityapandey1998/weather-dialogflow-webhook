    
#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from datetime import datetime
from geopy.geocoders import Nominatim
import requests

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
		result = req.get('queryResult')
		parameters = result.get('parameters')
		loc = parameters['city']
		time = parameters['date']
		duration = parameters['date-period']

		time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
		time_in_sec = time_obj.total_seconds()
		
		try:
			geolocator = Nominatim(user_agent='adityapandey')
			location = geolocator.geocode(loc)
			darksky_api_key = "f71b7245c7fc873eaab6dee321cf5966"

			url = "https://api.darksky.net/forecast/"+darksky_api_key+"/"+str(location.latitude)+","+str(location.longitude)+","+str(int(time_in_sec))

			#location.latitude, location.longitude
			res = requests.get(url)
			response = res.json()
			print(url)

			current = response['currently']['summary']
			daily = response['daily']['data'][0]['summary']
			report = ("The Weather Report for the day "+
				time_obj.strftime("%d %B, %Y") +" in "+loc+" is as follows - \n"+
				"General Weather: "+ current +
				"\nDay's Weather: "+ daily)
		except:
			report = "Not Able to obtain request from darksky.net or geoLocator"
		return  {
			"fulfillmentText": report,
			'source' : 'InterestRate'
		}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
