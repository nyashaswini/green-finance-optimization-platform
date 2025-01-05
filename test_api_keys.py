import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_weather_api():
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = "London"
    country = "UK"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\nOpenWeatherMap API Test - SUCCESS")
            print(f"Temperature in {city}: {data['main']['temp']}°C")
            print(f"Weather: {data['weather'][0]['description']}")
        else:
            print("\nOpenWeatherMap API Test - FAILED")
            print(f"Error: {response.json().get('message', 'Unknown error')}")
    except Exception as e:
        print(f"\nError testing weather API: {str(e)}")

def test_air_quality_api():
    api_key = os.getenv('AQICN_API_KEY')
    city = "London"
    
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ok':
                print("\nAir Quality API Test - SUCCESS")
                print(f"Air Quality Index in {city}: {data['data']['aqi']}")
                print(f"Station: {data['data']['city']['name']}")
            else:
                print("\nAir Quality API Test - FAILED")
                print(f"Error: {data.get('message', 'Unknown error')}")
        else:
            print("\nAir Quality API Test - FAILED")
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"\nError testing air quality API: {str(e)}")

if __name__ == "__main__":
    print("Testing APIs with your keys...")
    print(f"OpenWeatherMap API Key: {os.getenv('OPENWEATHER_API_KEY')[:5]}...")
    print(f"AQICN API Key: {os.getenv('AQICN_API_KEY')[:5]}...")
    
    test_weather_api()
    test_air_quality_api()
