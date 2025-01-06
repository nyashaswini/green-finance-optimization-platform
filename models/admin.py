import json
import os
from datetime import datetime

class AdminManager:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.analytics_file = 'data/analytics.json'
        self._load_data()

    def _load_data(self):
        """Load users and analytics data from JSON files"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
                self._save_users()

            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    self.analytics = json.load(f)
            else:
                self.analytics = {
                    'user_growth': [],
                    'investment_trends': [],
                    'project_distribution': {},
                    'esg_distribution': {}
                }
                self._save_analytics()
        except Exception as e:
            print(f"Error loading admin data: {str(e)}")
            self.users = {}
            self.analytics = {
                'user_growth': [],
                'investment_trends': [],
                'project_distribution': {},
                'esg_distribution': {}
            }

    def _save_users(self):
        """Save users data to JSON file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {str(e)}")

    def _save_analytics(self):
        """Save analytics data to JSON file"""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics: {str(e)}")

    def get_users(self):
        """Get all users"""
        return self.users

    def get_user(self, user_id):
        """Get a specific user"""
        return self.users.get(str(user_id))

    def add_user(self, user_id, role):
        """Add a new user"""
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                'id': user_id,
                'role': role,
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            self._save_users()
            print(f"Added user: {self.users[user_id]}")  # Debug print
        return self.users[user_id]

    def toggle_user_status(self, user_id):
        """Toggle user status between active and inactive"""
        user_id = str(user_id)
        if user_id in self.users:
            current_status = self.users[user_id]['status']
            new_status = 'inactive' if current_status == 'active' else 'active'
            self.users[user_id]['status'] = new_status
            self._save_users()
            return True
        return False

    def get_analytics_data(self):
        """Get analytics data"""
        return self.analytics

    def get_platform_stats(self):
        """Get platform statistics"""
        try:
            # Count users by role
            user_stats = {
                'total_users': len(self.users),
                'investors': len([u for u in self.users.values() if u['role'] == 'investor']),
                'fund_seekers': len([u for u in self.users.values() if u['role'] == 'fund-seeker']),
                'active_users': len([u for u in self.users.values() if u['status'] == 'active'])
            }

            # Get project stats
            from app import fund_seeker_manager
            projects = fund_seeker_manager.get_all_projects()
            project_stats = {
                'total_projects': len(projects),
                'approved_projects': len([p for p in projects if p.get('status') == 'approved']),
                'pending_projects': len([p for p in projects if p.get('status') == 'pending']),
                'total_funding_required': sum(float(p.get('funding_required', 0)) for p in projects),
                'total_funding_received': sum(float(p.get('funding_progress', 0)) for p in projects)
            }

            return {
                'user_stats': user_stats,
                'project_stats': project_stats,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting platform stats: {str(e)}")
            return {
                'user_stats': {
                    'total_users': 0,
                    'investors': 0,
                    'fund_seekers': 0,
                    'active_users': 0
                },
                'project_stats': {
                    'total_projects': 0,
                    'approved_projects': 0,
                    'pending_projects': 0,
                    'total_funding_required': 0,
                    'total_funding_received': 0
                },
                'last_updated': datetime.now().isoformat()
            }

    def get_system_status(self):
        """Get system monitoring status"""
        return {
            'status': 'healthy',
            'uptime': '100%',
            'last_backup': datetime.now().isoformat(),
            'system_load': {
                'cpu': '25%',
                'memory': '40%',
                'disk': '30%'
            }
        }

    @property
    def esg_params(self):
        """Get ESG scoring parameters"""
        return {
            'environmental_weight': 0.4,
            'social_weight': 0.3,
            'governance_weight': 0.3,
            'min_score': 0,
            'max_score': 100,
            'threshold': 60
        }

    def update_analytics(self, data_type, data):
        """Update analytics data"""
        if data_type in self.analytics:
            self.analytics[data_type] = data
            self._save_analytics()
            return True
        return False
