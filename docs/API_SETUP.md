# API Setup Guide

This document explains how to set up and use the free APIs in this project.

## 1. OpenWeatherMap API
1. Go to https://home.openweathermap.org/users/sign_up
2. Create a free account
3. Get your API key from your account dashboard
4. Set environment variable: `OPENWEATHER_API_KEY`

Free Tier Limits:
- 60 calls/minute
- Current weather data
- Basic forecasts

## 2. Air Quality Open Data Platform (AQICN)
1. Visit https://aqicn.org/data-platform/token/
2. Request a free token
3. Set environment variable: `AQICN_API_KEY`

Free Tier Limits:
- 1000 calls/minute
- Real-time air quality data

## 3. World Bank Climate Data API
- No setup required!
- Completely free and open
- Base URL: http://climatedataapi.worldbank.org/climateweb/rest/v1/country
- Documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api

## 4. Yahoo Finance
- No setup required!
- Install via pip: `pip install yfinance`
- Free access to ESG data for public companies

## 5. UN Sustainable Development Goals API
- No setup required!
- Base URL: https://unstats.un.org/SDGAPI/v1/sdg
- Documentation: https://unstats.un.org/SDGAPI/swagger/

## Setting Up Environment Variables

Create a `.env` file in your project root:
```
OPENWEATHER_API_KEY=your_key_here
AQICN_API_KEY=your_key_here
```

Or set them in your system environment:

Windows:
```
set OPENWEATHER_API_KEY=your_key_here
set AQICN_API_KEY=your_key_here
```

Linux/Mac:
```
export OPENWEATHER_API_KEY=your_key_here
export AQICN_API_KEY=your_key_here
```

## Testing APIs

You can test if your APIs are working by running:
```python
from data_collectors.environmental_data import EnvironmentalDataCollector
from data_collectors.project_data import ProjectDataCollector

# Initialize collectors
env_collector = EnvironmentalDataCollector()
project_collector = ProjectDataCollector()

# Test weather data
weather_data = env_collector.get_weather_data("London", "UK")
print("Weather Data:", weather_data)

# Test air quality
air_quality = env_collector.get_air_quality_data("London")
print("Air Quality:", air_quality)
```
