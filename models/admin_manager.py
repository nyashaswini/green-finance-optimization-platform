import json
import os
from datetime import datetime, timedelta
import random
import numpy as np

class AdminManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.analytics_file = os.path.join(data_dir, 'analytics.json')
        self.esg_params_file = os.path.join(data_dir, 'esg_params.json')
        
        self._ensure_data_files()
        self.load_data()

    def _ensure_data_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize users file if it doesn't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({
                    'users': [
                        {
                            'id': '1',
                            'username': 'admin',
                            'role': 'admin',
                            'status': 'Active'
                        }
                    ]
                }, f, indent=2)
        
        # Initialize analytics file if it doesn't exist
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                json.dump({
                    'user_growth': [],
                    'investment_trends': [],
                    'project_distribution': {},
                    'esg_scores': []
                }, f, indent=2)
        
        # Initialize ESG parameters file if it doesn't exist
        if not os.path.exists(self.esg_params_file):
            with open(self.esg_params_file, 'w') as f:
                json.dump({
                    'env_weight': 0.4,
                    'social_weight': 0.3,
                    'gov_weight': 0.3
                }, f, indent=2)

    def load_data(self):
        with open(self.users_file, 'r') as f:
            self.users_data = json.load(f)
        
        with open(self.analytics_file, 'r') as f:
            self.analytics_data = json.load(f)
        
        with open(self.esg_params_file, 'r') as f:
            self.esg_params = json.load(f)

    def save_data(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users_data, f, indent=2)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(self.analytics_data, f, indent=2)
        
        with open(self.esg_params_file, 'w') as f:
            json.dump(self.esg_params, f, indent=2)

    def get_users(self):
        return self.users_data['users']

    def toggle_user_status(self, user_id):
        for user in self.users_data['users']:
            if user['id'] == user_id:
                user['status'] = 'Inactive' if user['status'] == 'Active' else 'Active'
                self.save_data()
                return True
        return False

    def update_esg_params(self, env_weight, social_weight, gov_weight):
        if abs(env_weight + social_weight + gov_weight - 1.0) < 0.01:
            self.esg_params = {
                'env_weight': env_weight,
                'social_weight': social_weight,
                'gov_weight': gov_weight
            }
            self.save_data()
            return True
        return False

    def get_system_status(self):
        # In a real implementation, this would check actual system components
        return {
            'database': {
                'status': 'good',
                'message': 'Operating normally'
            },
            'api': {
                'status': 'good',
                'message': 'All services running'
            },
            'ml_models': {
                'status': 'warning',
                'message': 'Model retraining recommended'
            }
        }

    def get_platform_stats(self):
        return {
            'total_users': len(self.users_data['users']),
            'active_projects': len(self.analytics_data.get('project_distribution', {})),
            'total_investment': sum(self.analytics_data.get('investment_trends', [])),
            'avg_esg_score': np.mean(self.analytics_data.get('esg_scores', [70]))
        }

    def get_analytics_data(self):
        # Generate some sample data for demonstration
        dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') 
                for x in range(30, 0, -1)]
        
        return {
            'user_growth': {
                'dates': dates,
                'users': [100 + i * 10 + random.randint(-5, 5) for i in range(30)]
            },
            'investment_trends': {
                'dates': dates,
                'investments': [1000000 + i * 50000 + random.randint(-10000, 10000) 
                              for i in range(30)]
            },
            'project_distribution': {
                'categories': ['Solar', 'Wind', 'Hydro', 'Biomass', 'Energy Efficiency'],
                'values': [30, 25, 15, 20, 10]
            },
            'esg_distribution': {
                'scores': [random.gauss(75, 10) for _ in range(100)]
            }
        }

    def approve_project(self, project_id):
        # Implement project approval logic
        return True

    def reject_project(self, project_id):
        # Implement project rejection logic
        return True
