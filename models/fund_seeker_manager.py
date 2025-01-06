import json
from datetime import datetime

class FundSeekerManager:
    def __init__(self):
        self.projects = []
        self._load_projects()

    def _load_projects(self):
        try:
            with open('data/projects.json', 'r') as f:
                self.projects = json.load(f)
        except FileNotFoundError:
            # Initialize with some sample projects for testing
            self.projects = [
                {
                    'id': '1',
                    'name': 'Solar Farm Project',
                    'description': 'Large-scale solar farm development in sunny Arizona',
                    'funding_required': 5000000,
                    'timeline': 24,
                    'location': 'Arizona, USA',
                    'status': 'approved',
                    'environmental_score': 85,
                    'social_score': 75,
                    'governance_score': 80,
                    'impact_metrics': [1000, 500, 200, 90],
                    'date_submitted': datetime.now().isoformat(),
                    'fund_seeker_id': '1'
                },
                {
                    'id': '2',
                    'name': 'Wind Energy Initiative',
                    'description': 'Offshore wind farm development project',
                    'funding_required': 8000000,
                    'timeline': 36,
                    'location': 'Massachusetts, USA',
                    'status': 'approved',
                    'environmental_score': 90,
                    'social_score': 70,
                    'governance_score': 85,
                    'impact_metrics': [1500, 300, 150, 95],
                    'date_submitted': datetime.now().isoformat(),
                    'fund_seeker_id': '2'
                }
            ]
            self._save_projects()

    def _save_projects(self):
        try:
            with open('data/projects.json', 'w') as f:
                json.dump(self.projects, f)
        except FileNotFoundError:
            import os
            os.makedirs('data', exist_ok=True)
            with open('data/projects.json', 'w') as f:
                json.dump(self.projects, f)

    def get_approved_projects(self):
        """Get all approved projects"""
        return [project for project in self.projects if project['status'] == 'approved']

    def get_all_projects(self):
        """Get all projects"""
        return self.projects

    def submit_project(self, project_data):
        """Submit a new project"""
        project_id = str(len(self.projects) + 1)
        project = {
            'id': project_id,
            'status': 'pending',
            'date_submitted': datetime.now().isoformat(),
            **project_data
        }
        self.projects.append(project)
        self._save_projects()
        return project_id

    def get_project_by_id(self, project_id):
        """Get a specific project by ID"""
        for project in self.projects:
            if project['id'] == project_id:
                return project
        return None

    def update_project_status(self, project_id, status):
        """Update project status (approved/rejected)"""
        for project in self.projects:
            if project['id'] == project_id:
                project['status'] = status
                self._save_projects()
                return True
        return False
