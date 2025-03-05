import requests
from config import config
from ..audio.text_to_speech import say

def get_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={config.wheatherAPI}&q={city}&aqi=no'
    
    # Sending a GET request to fetch the weather data
    response = requests.get(url)
    
    if response.status_code == 200:
        # If the request is successful
        data = response.json()
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        cloud = data['current']['cloud']
        feelslike = data['current']['feelslike_c'] # Temperature perceived by the human body in Celsius
        time = data['current']['last_updated'] 

        say(f"The current temperature in {city} is {temperature} degree celcius and is {description}, humidity is {humidity} percent, the wind speed is {wind_speed} kmph, its {cloud} percent cloudy, it feels like {feelslike} degree celcius and the current time is {time} hour")
        
    else:
        say("Failed to retrieve data. Please check the city name or API key.")

