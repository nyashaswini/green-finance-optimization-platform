import yfinance as yf
import pandas as pd
import requests
from datetime import datetime
import json

class ProjectDataCollector:
    def __init__(self):
        self.un_sdg_url = "https://unstats.un.org/SDGAPI/v1/sdg/Goal/List"
        
    def get_company_esg_data(self, ticker):
        """
        Collect ESG data for companies using Yahoo Finance
        """
        try:
            # Get company info using yfinance
            company = yf.Ticker(ticker)
            
            # Get ESG scores
            esg_data = company.sustainability
            
            if esg_data is not None:
                return {
                    'environmental_score': esg_data.loc['environmentScore'][0],
                    'social_score': esg_data.loc['socialScore'][0],
                    'governance_score': esg_data.loc['governanceScore'][0],
                    'total_esg': esg_data.loc['totalEsg'][0],
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except Exception as e:
            print(f"Error collecting ESG data: {str(e)}")
            return None

    def get_world_bank_climate_data(self, country_code):
        """
        Collect climate data from World Bank's Climate Data API
        """
        base_url = "http://climatedataapi.worldbank.org/climateweb/rest/v1/country"
        
        try:
            # Get temperature data
            temp_url = f"{base_url}/mavg/tas/{country_code}"
            temp_response = requests.get(temp_url)
            
            # Get precipitation data
            precip_url = f"{base_url}/mavg/pr/{country_code}"
            precip_response = requests.get(precip_url)
            
            if temp_response.status_code == 200 and precip_response.status_code == 200:
                return {
                    'temperature_data': temp_response.json(),
                    'precipitation_data': precip_response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            return None
        except Exception as e:
            print(f"Error collecting World Bank data: {str(e)}")
            return None

    def get_un_sdg_data(self):
        """
        Collect Sustainable Development Goals data from UN
        """
        try:
            response = requests.get(self.un_sdg_url)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error collecting UN SDG data: {str(e)}")
            return None

    def combine_project_data(self, project_id, location):
        """
        Combine all relevant data sources for a project
        """
        try:
            # Get environmental data for project location
            env_collector = EnvironmentalDataCollector()
            weather_data = env_collector.get_weather_data(location['city'], 
                                                        location['country_code'])
            air_quality = env_collector.get_air_quality_data(location['city'])
            
            # Get company ESG data if available
            company_data = None
            if 'company_ticker' in location:
                company_data = self.get_company_esg_data(location['company_ticker'])
            
            # Get regional climate data
            climate_data = self.get_world_bank_climate_data(location['country_code'])
            
            # Combine all data
            project_data = {
                'project_id': project_id,
                'location': location,
                'weather_data': weather_data,
                'air_quality_data': air_quality,
                'company_esg_data': company_data,
                'climate_data': climate_data,
                'collection_timestamp': datetime.now().isoformat()
            }
            
            return project_data
            
        except Exception as e:
            print(f"Error combining project data: {str(e)}")
            return None
