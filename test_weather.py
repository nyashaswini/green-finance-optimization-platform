import requests

def test_openweather_api():
    api_key = "3f57fa5ba4be34a783675f3ee28c2b21"
    city = "London"
    
    # Direct API call to verify
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    print(f"Testing OpenWeatherMap API with key: {api_key}")
    print(f"URL being tested: {url}\n")
    
    try:
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAPI Test - SUCCESS!")
            print(f"City: {data['name']}")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Weather: {data['weather'][0]['description']}")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Wind Speed: {data['wind']['speed']} m/s")
        else:
            print("\nAPI Test - FAILED")
            print(f"Error Message: {response.json().get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_openweather_api()
