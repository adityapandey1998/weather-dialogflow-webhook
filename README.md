# Dialogflow - webhook implementation in Python

This is a really simple webhook implementation that gets Dialogflow classification JSON (i.e. a JSON output of Dialogflow /query endpoint) and returns a fulfillment response.

More info about Dialogflow webhooks could be found here:
[Dialogflow Webhook](https://dialogflow.com/docs/fulfillment)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a weather information fulfillment service that uses [Darksky Weather API](https://darksky.net) which gives weather information using the co-ordinates of the required location from [Nominatim](https://nominatim.openstreetmap.org/).

The service packs the result in the Dialogflow webhook-compatible response JSON and returns it to Dialogflow.
