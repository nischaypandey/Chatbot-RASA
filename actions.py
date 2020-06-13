from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import requests

class ActionWeather(Action):
	def name(self):
		return 'action_weather'
		
	def run(self, dispatcher, tracker, domain):
            from apixu.client import ApixuClient
            api_key = "3c6a1417de51be296b3de24709a52d49" #your apixu key
            client = ApixuClient(api_key)

            loc = tracker.get_slot('location')
            params = {
            'access_key': api_key,
            'query': str(loc)
            }
            print("Searching in location ", loc)
            api_result = requests.get('http://api.weatherstack.com/current', params)
            current= api_result.json()
            print ('res ', current)
            country = current['location']['country']
            city = current['location']['name']
            condition = current['current']['weather_descriptions']
            temperature_c = current['current']['temperature']
            humidity = current['current']['humidity']
            wind_mph = current['current']['wind_speed']

            response = """It is currently {} in {} at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.""".format(condition, city, temperature_c, humidity, wind_mph)

            dispatcher.utter_message(response)
            return [SlotSet('location',loc)]