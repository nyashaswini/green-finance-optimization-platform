import requests
import wbgapi
import pandas as pd
from datetime import datetime
import json
import os

def test_un_sdg():
    print("\nTesting UN SDG API...")
    try:
        url = "https://unstats.un.org/SDGAPI/v1/sdg/Goal/List"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] UN SDG API is working!")
            print(f"Number of SDG goals available: {len(data)}")
            return True
        else:
            print("[FAILED] UN SDG API failed")
            return False
    except Exception as e:
        print(f"[ERROR] Error with UN SDG API: {str(e)}")
        return False

def test_world_bank():
    print("\nTesting World Bank API...")
    try:
        # Get CO2 emissions data for World
        data = wbgapi.data.DataFrame('EN.ATM.CO2E.PC', economy='WLD', time=range(2015, 2023))
        print("[SUCCESS] World Bank API is working!")
        print(f"Years of CO2 emissions data available: {len(data)}")
        return True
    except Exception as e:
        print(f"[ERROR] Error with World Bank API: {str(e)}")
        return False

def test_noaa():
    print("\nTesting NOAA Climate API...")
    try:
        token = os.getenv('NOAA_TOKEN', '')
        if not token:
            print("[ERROR] NOAA API token not found. Please set NOAA_TOKEN environment variable")
            return False
            
        headers = {'token': token}
        url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("[SUCCESS] NOAA Climate API is working!")
            data = response.json()
            print(f"Number of datasets available: {len(data['results'])}")
            return True
        else:
            print("[FAILED] NOAA Climate API failed")
            print(f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Error with NOAA API: {str(e)}")
        return False

def test_nasa():
    print("\nTesting NASA Earth Data API...")
    try:
        url = "https://cmr.earthdata.nasa.gov/search/collections.json"
        params = {
            'keyword': 'temperature',
            'page_size': 5
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] NASA Earth Data API is working!")
            print(f"Number of collections found: {len(data.get('feed', {}).get('entry', []))}")
            return True
        else:
            print("[FAILED] NASA Earth Data API failed")
            return False
    except Exception as e:
        print(f"[ERROR] Error with NASA API: {str(e)}")
        return False

def test_iea():
    print("\nTesting IEA Data Access...")
    try:
        url = "https://www.iea.org/data-and-statistics/data-browser"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("[SUCCESS] IEA website is accessible!")
            print("Note: Full data access requires authentication")
            return True
        else:
            print("[FAILED] IEA website access failed")
            return False
    except Exception as e:
        print(f"[ERROR] Error accessing IEA: {str(e)}")
        return False

def test_eea():
    print("\nTesting EEA Reports API...")
    try:
        url = "https://www.eea.europa.eu/api/reports"
        params = {
            'topic': 'climate-change-adaptation',
            'format': 'json'
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("[SUCCESS] EEA Reports API is working!")
            print("Successfully accessed reports data")
            return True
        else:
            print("[FAILED] EEA Reports API failed")
            return False
    except Exception as e:
        print(f"[ERROR] Error with EEA API: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing all data sources...")
    print("=" * 50)
    
    results = {
        "UN SDG": test_un_sdg(),
        "World Bank": test_world_bank(),
        "NOAA Climate": test_noaa(),
        "NASA Earth": test_nasa(),
        "IEA Energy": test_iea(),
        "EEA Reports": test_eea()
    }
    
    print("\nSummary:")
    print("=" * 50)
    for source, success in results.items():
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{source}: {status}")
