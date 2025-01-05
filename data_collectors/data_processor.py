import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataProcessor:
    def __init__(self):
        self.processed_data = {}
        
    def process_environmental_data(self, data):
        """Process environmental metrics"""
        try:
            env_data = {
                'emissions': self._process_emissions(data.get('world_bank', {})),
                'climate': self._process_climate_data(data.get('noaa', {})),
                'energy': self._process_energy_data(data.get('iea', {}))
            }
            self.processed_data['environmental'] = env_data
            return env_data
        except Exception as e:
            print(f"Error processing environmental data: {str(e)}")
            return None

    def process_social_data(self, data):
        """Process social metrics"""
        try:
            social_data = {
                'sdg_progress': self._process_sdg_data(data.get('un_sdg', {})),
                'development': self._process_development_data(data.get('world_bank', {}))
            }
            self.processed_data['social'] = social_data
            return social_data
        except Exception as e:
            print(f"Error processing social data: {str(e)}")
            return None

    def process_governance_data(self, data):
        """Process governance metrics"""
        try:
            gov_data = {
                'policy_indicators': self._process_policy_data(data.get('eea', {})),
                'regulatory_compliance': self._process_compliance_data(data)
            }
            self.processed_data['governance'] = gov_data
            return gov_data
        except Exception as e:
            print(f"Error processing governance data: {str(e)}")
            return None

    def _process_emissions(self, data):
        """Process emissions data"""
        if not data:
            return None
            
        try:
            # Process CO2 emissions data
            emissions_data = pd.DataFrame(data.get('EN.ATM.CO2E.PC', {}))
            return {
                'latest_value': emissions_data.iloc[-1].values[0] if not emissions_data.empty else None,
                'trend': self._calculate_trend(emissions_data),
                'year': datetime.now().year - 1
            }
        except Exception as e:
            print(f"Error processing emissions data: {str(e)}")
            return None

    def _process_climate_data(self, data):
        """Process climate data"""
        if not data:
            return None
            
        try:
            # Process temperature and precipitation data
            return {
                'temperature_anomaly': self._calculate_temperature_anomaly(data),
                'precipitation_change': self._calculate_precipitation_change(data)
            }
        except Exception as e:
            print(f"Error processing climate data: {str(e)}")
            return None

    def _process_energy_data(self, data):
        """Process energy consumption and renewable energy data"""
        if not data:
            return None
            
        try:
            return {
                'renewable_share': self._calculate_renewable_share(data),
                'energy_intensity': self._calculate_energy_intensity(data)
            }
        except Exception as e:
            print(f"Error processing energy data: {str(e)}")
            return None

    def _process_sdg_data(self, data):
        """Process SDG indicators"""
        if not data:
            return None
            
        try:
            return {
                'goals_progress': self._calculate_sdg_progress(data),
                'latest_update': datetime.now().strftime('%Y-%m-%d')
            }
        except Exception as e:
            print(f"Error processing SDG data: {str(e)}")
            return None

    def _calculate_trend(self, data):
        """Calculate trend from time series data"""
        if data is None or data.empty:
            return None
            
        try:
            values = data.values.flatten()
            x = np.arange(len(values))
            z = np.polyfit(x, values, 1)
            return {
                'slope': float(z[0]),
                'direction': 'increasing' if z[0] > 0 else 'decreasing'
            }
        except Exception as e:
            print(f"Error calculating trend: {str(e)}")
            return None

    def _calculate_temperature_anomaly(self, data):
        """Calculate temperature anomaly from baseline"""
        # Implementation would depend on data structure
        return 0.0  # Placeholder

    def _calculate_precipitation_change(self, data):
        """Calculate precipitation change from baseline"""
        # Implementation would depend on data structure
        return 0.0  # Placeholder

    def _calculate_renewable_share(self, data):
        """Calculate share of renewable energy"""
        # Implementation would depend on data structure
        return 0.0  # Placeholder

    def _calculate_energy_intensity(self, data):
        """Calculate energy intensity of GDP"""
        # Implementation would depend on data structure
        return 0.0  # Placeholder

    def _calculate_sdg_progress(self, data):
        """Calculate progress towards SDG targets"""
        # Implementation would depend on data structure
        return {'overall_progress': 0.0}  # Placeholder

    def export_processed_data(self, filepath):
        """Export processed data to JSON"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.processed_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {str(e)}")
            return False
