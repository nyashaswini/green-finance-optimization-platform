from data_collectors.environmental_data import EnvironmentalDataCollector
from data_collectors.project_data import ProjectDataCollector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_all_apis():
    print("Testing all APIs...")
    
    # Initialize collectors
    env_collector = EnvironmentalDataCollector()
    project_collector = ProjectDataCollector()
    
    # 1. Test OpenWeatherMap API
    print("\n1. Testing OpenWeatherMap API:")
    weather_data = env_collector.get_weather_data("London", "UK")
    print(f"Weather Data: {weather_data}")
    
    # 2. Test AQICN API
    print("\n2. Testing Air Quality API:")
    air_quality = env_collector.get_air_quality_data("London")
    print(f"Air Quality Data: {air_quality}")
    
    # 3. Test World Bank Climate API
    print("\n3. Testing World Bank Climate API:")
    climate_data = project_collector.get_world_bank_climate_data("USA")
    print(f"Climate Data: {climate_data}")
    
    # 4. Test Yahoo Finance API
    print("\n4. Testing Yahoo Finance API:")
    esg_data = project_collector.get_company_esg_data("AAPL")  # Using Apple as example
    print(f"ESG Data: {esg_data}")
    
    # 5. Test UN SDG API
    print("\n5. Testing UN SDG API:")
    sdg_data = project_collector.get_un_sdg_data()
    print(f"SDG Data: {sdg_data}")

if __name__ == "__main__":
    test_all_apis()
