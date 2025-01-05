"""
Configuration file for API endpoints and documentation
"""

API_CONFIGS = {
    'openweathermap': {
        'base_url': 'http://api.openweathermap.org/data/2.5/weather',
        'docs_url': 'https://openweathermap.org/api',
        'signup_url': 'https://home.openweathermap.org/users/sign_up',
        'free_tier_limits': {
            'calls_per_minute': 60,
            'total_calls_per_day': 1000000
        }
    },
    
    'aqicn': {
        'base_url': 'https://api.waqi.info/feed/',
        'docs_url': 'https://aqicn.org/api/',
        'signup_url': 'https://aqicn.org/data-platform/token/',
        'free_tier_limits': {
            'calls_per_minute': 1000,
            'total_calls_per_day': 1000000
        }
    },
    
    'world_bank_climate': {
        'base_url': 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country',
        'docs_url': 'https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api',
        'auth_required': False,
        'features': [
            'temperature_data',
            'precipitation_data',
            'climate_projections'
        ]
    },
    
    'yahoo_finance': {
        'library': 'yfinance',
        'pip_install': 'pip install yfinance',
        'docs_url': 'https://pypi.org/project/yfinance/',
        'auth_required': False,
        'features': [
            'esg_scores',
            'company_info',
            'sustainability_data'
        ]
    },
    
    'un_sdg': {
        'base_url': 'https://unstats.un.org/SDGAPI/v1/sdg',
        'docs_url': 'https://unstats.un.org/SDGAPI/swagger/',
        'auth_required': False,
        'features': [
            'sdg_indicators',
            'goals_list',
            'target_data'
        ]
    }
}

# Environment variable names for API keys
ENV_VARS = {
    'OPENWEATHER_API_KEY': 'API key for OpenWeatherMap',
    'AQICN_API_KEY': 'API key for Air Quality Open Data Platform'
}

# Rate limiting configurations
RATE_LIMITS = {
    'openweathermap': {
        'calls_per_minute': 60,
        'pause_after_calls': 1  # seconds
    },
    'aqicn': {
        'calls_per_minute': 1000,
        'pause_after_calls': 0.1  # seconds
    }
}
