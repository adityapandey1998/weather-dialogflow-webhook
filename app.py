    
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
	#print(json.dumps(req, indent=4))
	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r=make_response(res)
	r.headers['Content-Type'] = 'application/json'
	
	return r

def makeWebhookResult(req):
	print(req.get('queryResult').get('action'))
	
	if req.get('queryResult').get('action') in ['WeatherInfo_context','WeatherInfo']:
		result = req.get('queryResult')
		parameters = result.get('parameters')
		loc = parameters.get('city')
		time = parameters.get('date')
		print("Parameters: ",parameters)
		
		print(time)
		time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
		#print(time_obj)
		time_in_sec = time_obj.timestamp()
		print(time_in_sec)
		
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
				time_obj.strftime("%d %B, %Y") +" in "+loc+" is as follows - "+
				"\n\nGeneral Weather: "+ current +
				"\n\nDay's Weather: "+ daily)
		except:
			report = "Not Able to obtain request from darksky.net or geoLocator"
		return  {
			"fulfillmentText": report,
			'source' : 'WeatherInfo'
		}

	elif req.get('queryResult').get('action') in ['TempInfo_context','TempInfo']:
		result = req.get('queryResult')
		parameters = result.get('parameters')
		loc = parameters.get('city')
		time = parameters.get('date')
		TempType = parameters.get('TempType')
		print("Parameters: ",parameters)
		
		time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
		time_in_sec = time_obj.timestamp()
		print(time_in_sec)
		try:
			geolocator = Nominatim(user_agent='adityapandey')
			location = geolocator.geocode(loc)
			darksky_api_key = "f71b7245c7fc873eaab6dee321cf5966"

			url = "https://api.darksky.net/forecast/"+darksky_api_key+"/"+str(location.latitude)+","+str(location.longitude)+","+str(int(time_in_sec))

			#location.latitude, location.longitude
			res = requests.get(url)
			response = res.json()
			print(url)
			if TempType=="maximum":
				Temp = response['daily']['data'][0]['temperatureHigh']
				TempTime = response['daily']['data'][0]['temperatureHighTime']
			elif TempType=="minimum":
				Temp = response['daily']['data'][0]['temperatureLow']
				TempTime = response['daily']['data'][0]['temperatureLowTime']
			elif TempType=="average":
				Temp = (response['daily']['data'][0]['temperatureHigh'] + response['daily']['data'][0]['temperatureLow'])/2
			else:
				Temp = response['currently']['temperature']
			print(Temp)
			Humidity = response['daily']['data'][0]['humidity']
			print(Humidity)
			report = ("The "+TempType+" temp for the day "+
				time_obj.strftime("%d %B, %Y") +" in "+loc+" is "+
				str(Temp)+" deg. Farenheight"+
				"\n\nHumidity level is: "+ str(Humidity))
			
		except:
			report = "Not Able to obtain request from darksky.net or geoLocator"
		return  {
			"fulfillmentText": report,
			'source' : 'TempInfo'
		}

	elif req.get('queryResult').get('action') in ['WeatherTypeInfo_context','WeatherTypeInfo']:
		result = req.get('queryResult')
		parameters = result.get('parameters')
		loc = parameters.get('city')
		time = parameters.get('date')
		duration = parameters.get('date-period')
		weatherType = parameters.get('WeatherType')
		print("Parameters: ",parameters)

		weatherTypeOptions = ["clear and sunny", "cloudy", "cold", "rainy", "windy", "snow", "sunny"]
		
		print(time)
		time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
		#print(time_obj)
		time_in_sec = time_obj.timestamp()
		print(time_in_sec)
		
		try:
			geolocator = Nominatim(user_agent='adityapandey')
			location = geolocator.geocode(loc)
			darksky_api_key = "f71b7245c7fc873eaab6dee321cf5966"

			url = "https://api.darksky.net/forecast/"+darksky_api_key+"/"+str(location.latitude)+","+str(location.longitude)+","+str(int(time_in_sec))

			#location.latitude, location.longitude
			res = requests.get(url)
			response = res.json()
			print(url)

			icon = response['daily']['icon']

			if icon in ["rain","sleet"]:
				weatherTypeActual = "rainy"
			
			elif icon in ["wind"]:
				weatherTypeActual = "windy"

			elif icon in ["clear-day", "clear-night"]:
				weatherTypeActual = "clear and sunny"
			
			elif icon in ["cloudy", "partly-cloudy-day", "partly-cloudy-night"]:
				weatherTypeActual = "cloudy"
			
			elif icon in ["snow"]:
				weatherTypeActual = "snow"
			
			elif icon in ["fog"]:
				weatherTypeActual = "cold"

			else: 
				weatherTypeActual = "Couldn't be determined"

			if weatherTypeActual == weatherType:
				report = "Yes"
			else:
				report = "No"

			
			report = (report + ", the Weather Report for the day "+
				time_obj.strftime("%d %B, %Y") +" in "+loc+" says that the day is expected/was \n"+
				weatherTypeActual)
		except:
			report = "Not Able to obtain request from darksky.net or geoLocator"
		return  {
			"fulfillmentText": report,
			'source' : 'WeatherTypeInfo'
		}

	else:
		return  {
			"fulfillmentText": "Action not coded yet",
			'source' : 'UnknownAction'
		}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
