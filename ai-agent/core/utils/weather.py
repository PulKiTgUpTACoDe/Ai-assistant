import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path to help with imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

def get_weather(city):
    weather_api_key = os.getenv("WEATHER_API_KEY")
    url = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no'
    
    # Sending a GET request to fetch the weather data
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        description = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_speed = data['current']['wind_kph']
        cloud = data['current']['cloud']
        feelslike = data['current']['feelslike_c'] # Temperature perceived by the human body in Celsius
        time = data['current']['last_updated'] 
        
        return f"The current temperature in {city} is {temperature} degree celcius and is {description}, humidity is {humidity} percent, the wind speed is {wind_speed} kmph, its {cloud} percent cloudy, it feels like {feelslike} degree celcius and the current time is {time} hour"
    else:
        say("Failed to retrieve data. Please check the city name or API key.") 