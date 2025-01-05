import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import os

class EnvironmentalDataCollector:
    def __init__(self):
        # OpenWeatherMap API - Free tier
        self.weather_api_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
        # Air Quality Open Data Platform - Free
        self.air_quality_api_key = os.getenv('AQICN_API_KEY', 'your_api_key_here')
        
    def get_weather_data(self, city, country_code):
        """Collect weather data from OpenWeatherMap API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        try:
            params = {
                'q': f"{city},{country_code}",
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'precipitation': data.get('rain', {}).get('1h', 0),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print(f"Error fetching weather data: {data.get('message')}")
                return None
        except Exception as e:
            print(f"Error in weather data collection: {str(e)}")
            return None

    def get_air_quality_data(self, city):
        """Collect air quality data from AQICN"""
        base_url = f"https://api.waqi.info/feed/{city}/"
        
        try:
            params = {'token': self.air_quality_api_key}
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('status') == 'ok':
                return {
                    'aqi': data['data']['aqi'],
                    'pm25': data['data'].get('iaqi', {}).get('pm25', {}).get('v'),
                    'pm10': data['data'].get('iaqi', {}).get('pm10', {}).get('v'),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print(f"Error fetching air quality data: {data.get('message')}")
                return None
        except Exception as e:
            print(f"Error in air quality data collection: {str(e)}")
            return None

    def get_epa_data(self):
        """Collect environmental data from EPA's API"""
        # EPA's API endpoint for air quality data
        base_url = "https://aqs.epa.gov/data/api/sampleData/bySite"
        
        try:
            # Example parameters for getting PM2.5 data
            params = {
                'email': 'your-email@example.com',  # Required for EPA API
                'key': 'your-key-here',
                'param': '88101',  # Parameter code for PM2.5
                'bdate': (datetime.now() - timedelta(days=7)).strftime('%Y%m%d'),
                'edate': datetime.now().strftime('%Y%m%d'),
                'state': '06',  # California
                'county': '037'  # Los Angeles
            }
            
            response = requests.get(base_url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error in EPA data collection: {str(e)}")
            return None
