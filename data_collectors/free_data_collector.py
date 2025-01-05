import requests
import pandas as pd
import json
from datetime import datetime
import os
import wbgapi  # World Bank API
from bs4 import BeautifulSoup
import time

class FreeDataCollector:
    def __init__(self):
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def get_un_sdg_data(self, indicator_code=None):
        """
        Collect data from UN SDG API
        Example indicator: SI_POV_DAY1 (Poverty indicator)
        """
        try:
            base_url = "https://unstats.un.org/SDGAPI/v1/sdg"
            if indicator_code:
                url = f"{base_url}/Indicator/{indicator_code}/Data"
            else:
                url = f"{base_url}/Goal/List"
                
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self._cache_data('un_sdg', data)
                return data
            return None
        except Exception as e:
            print(f"Error collecting UN SDG data: {str(e)}")
            return None

    def get_world_bank_data(self, indicator="EN.ATM.CO2E.PC", country_code="WLD"):
        """
        Collect World Bank data using wbgapi
        Example indicators:
        - EN.ATM.CO2E.PC: CO2 emissions
        - NY.GDP.MKTP.CD: GDP
        """
        try:
            data = wbgapi.data.DataFrame(indicator, 
                                       economy=country_code, 
                                       time=range(2015, datetime.now().year))
            self._cache_data('world_bank', data.to_dict())
            return data
        except Exception as e:
            print(f"Error collecting World Bank data: {str(e)}")
            return None

    def get_noaa_climate_data(self, station_id="GHCND:USW00094728", start_date="2020-01-01"):
        """
        Collect NOAA climate data
        Uses NOAA's CDO API
        """
        try:
            token = os.getenv('NOAA_TOKEN', 'your_token_here')
            base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
            headers = {'token': token}
            
            params = {
                'datasetid': 'GHCND',
                'stationid': station_id,
                'startdate': start_date,
                'enddate': datetime.now().strftime('%Y-%m-%d'),
                'limit': 1000
            }
            
            response = requests.get(f"{base_url}/data", headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                self._cache_data('noaa_climate', data)
                return data
            return None
        except Exception as e:
            print(f"Error collecting NOAA data: {str(e)}")
            return None

    def get_nasa_earth_data(self, dataset="GPM_L3"):
        """
        Collect NASA Earth Science data
        Uses NASA's CMR API
        """
        try:
            base_url = "https://cmr.earthdata.nasa.gov/search"
            params = {
                'collection_concept_id': dataset,
                'page_size': 10,
                'format': 'json'
            }
            
            response = requests.get(f"{base_url}/collections.json", params=params)
            if response.status_code == 200:
                data = response.json()
                self._cache_data('nasa_earth', data)
                return data
            return None
        except Exception as e:
            print(f"Error collecting NASA data: {str(e)}")
            return None

    def get_iea_data(self):
        """
        Collect IEA energy data from their free datasets
        """
        try:
            # IEA's free data endpoint
            url = "https://www.iea.org/data-and-statistics/data-browser"
            response = requests.get(url)
            
            if response.status_code == 200:
                # Parse the HTML to extract available free data
                soup = BeautifulSoup(response.text, 'html.parser')
                data = self._parse_iea_page(soup)
                self._cache_data('iea_energy', data)
                return data
            return None
        except Exception as e:
            print(f"Error collecting IEA data: {str(e)}")
            return None

    def get_eea_reports(self, topic="climate"):
        """
        Collect reports from European Environment Agency
        """
        try:
            base_url = "https://www.eea.europa.eu/api/reports"
            params = {
                'topic': topic,
                'format': 'json'
            }
            
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                self._cache_data('eea_reports', data)
                return data
            return None
        except Exception as e:
            print(f"Error collecting EEA reports: {str(e)}")
            return None

    def _cache_data(self, source, data):
        """Cache the collected data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        cache_file = os.path.join(self.cache_dir, f"{source}_{timestamp}.json")
        
        with open(cache_file, 'w') as f:
            if isinstance(data, pd.DataFrame):
                json.dump(data.to_dict(), f)
            else:
                json.dump(data, f)

    def _parse_iea_page(self, soup):
        """Parse IEA webpage for free data"""
        # Implementation would depend on page structure
        # This is a placeholder
        return {'status': 'placeholder'}

    def collect_all_data(self, country_code="WLD"):
        """
        Collect data from all available free sources
        """
        all_data = {}
        
        print("Starting comprehensive data collection...")
        
        # 1. UN SDG Data
        print("Collecting UN SDG data...")
        all_data['un_sdg'] = self.get_un_sdg_data()
        
        # 2. World Bank Data
        print("Collecting World Bank data...")
        indicators = ['EN.ATM.CO2E.PC', 'NY.GDP.MKTP.CD', 'EG.USE.PCAP.KG.OE']
        all_data['world_bank'] = {}
        for indicator in indicators:
            all_data['world_bank'][indicator] = self.get_world_bank_data(indicator, country_code)
            time.sleep(1)  # Respect API rate limits
        
        # 3. NOAA Climate Data
        print("Collecting NOAA climate data...")
        all_data['noaa'] = self.get_noaa_climate_data()
        
        # 4. NASA Earth Data
        print("Collecting NASA Earth data...")
        all_data['nasa'] = self.get_nasa_earth_data()
        
        # 5. IEA Energy Data
        print("Collecting IEA energy data...")
        all_data['iea'] = self.get_iea_data()
        
        # 6. EEA Reports
        print("Collecting EEA reports...")
        all_data['eea'] = self.get_eea_reports()
        
        return all_data
