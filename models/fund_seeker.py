import json
from datetime import datetime
import os

class FundSeekerManager:
    def __init__(self):
        self.projects = []
        self._load_projects()

    def _save_projects(self):
        """Save projects to JSON file"""
        try:
            if not os.path.exists('data'):
                os.makedirs('data')
                print("Created data directory")
            
            projects_file = os.path.join('data', 'projects.json')
            print(f"Saving projects to: {projects_file}")
            
            # Convert projects to dictionary with ID as key
            projects_dict = {str(p['id']): p for p in self.projects}
            
            with open(projects_file, 'w') as f:
                json.dump(projects_dict, f, indent=2)
            print(f"Successfully saved {len(self.projects)} projects")
        except Exception as e:
            print(f"Error saving projects: {str(e)}")
            import traceback
            traceback.print_exc()

    def _load_projects(self):
        """Load projects from JSON file"""
        try:
            if not os.path.exists('data'):
                os.makedirs('data')
                print("Created data directory")
            
            projects_file = os.path.join('data', 'projects.json')
            print(f"Loading projects from: {projects_file}")
            
            if os.path.exists(projects_file):
                with open(projects_file, 'r') as f:
                    projects_dict = json.load(f)
                    # Convert dictionary back to list
                    self.projects = list(projects_dict.values())
                print(f"Loaded {len(self.projects)} projects")
            else:
                print("No projects file found, initializing empty list")
                self.projects = [
                    {
                        "id": "1",
                        "name": "Solar Farm Project",
                        "description": "Large-scale solar farm development in sunny Arizona",
                        "funding_required": 5000000,
                        "timeline": 24,
                        "location": "Arizona, USA",
                        "status": "approved",
                        "environmental_score": 85,
                        "social_score": 75,
                        "governance_score": 80,
                        "impact_metrics": [1000, 500, 200, 90],
                        "date_submitted": datetime.now().isoformat(),
                        "fund_seeker_id": "1"
                    },
                    {
                        "id": "2",
                        "name": "Wind Energy Initiative",
                        "description": "Offshore wind farm development project",
                        "funding_required": 8000000,
                        "timeline": 36,
                        "location": "Massachusetts, USA",
                        "status": "approved",
                        "environmental_score": 90,
                        "social_score": 70,
                        "governance_score": 85,
                        "impact_metrics": [1500, 300, 150, 95],
                        "date_submitted": datetime.now().isoformat(),
                        "fund_seeker_id": "2"
                    }
                ]
                self._save_projects()  # Create the initial file
        except Exception as e:
            print(f"Error loading projects: {str(e)}")
            import traceback
            traceback.print_exc()
            self.projects = []

    def get_user_projects(self, user_id):
        """Get all projects for a specific user"""
        try:
            print(f"Getting projects for user {user_id}")  # Debug print
            print(f"All projects: {self.projects}")  # Debug print
            user_projects = [p for p in self.projects if str(p.get('fund_seeker_id')) == str(user_id)]
            print(f"Found {len(user_projects)} projects for user {user_id}")  # Debug print
            print(f"User projects: {user_projects}")  # Debug print
            return user_projects
        except Exception as e:
            print(f"Error getting user projects: {str(e)}")
            return []

    def get_approved_projects(self):
        """Get all approved projects"""
        try:
            # Include both pending and approved projects for now (for testing)
            approved_projects = [p for p in self.projects if p.get('status') in ['pending', 'approved']]
            print(f"Found {len(approved_projects)} available projects")  # Debug print
            for project in approved_projects:
                print(f"Project: {project['name']}, Status: {project['status']}")  # Debug print
            return approved_projects
        except Exception as e:
            print(f"Error getting approved projects: {str(e)}")
            return []

    def get_all_projects(self):
        """Get all projects"""
        try:
            # Make sure each project has an ID
            for project in self.projects:
                if 'id' not in project:
                    project['id'] = str(self.projects.index(project) + 1)
            
            print(f"Returning {len(self.projects)} projects: {self.projects}")  # Debug print
            return self.projects
        except Exception as e:
            print(f"Error in get_all_projects: {str(e)}")
            return []

    def get_project_by_id(self, project_id):
        """Get a specific project by ID"""
        try:
            for project in self.projects:
                if str(project.get('id')) == str(project_id):
                    return project
            return None
        except Exception as e:
            print(f"Error getting project by ID: {str(e)}")
            return None

    def create_project(self, name, description, funding_required, timeline, sustainability_impact, fund_seeker_id):
        """Create a new project"""
        try:
            print(f"Creating project for fund seeker: {fund_seeker_id}")  # Debug print
            
            # Generate a new unique ID
            project_id = str(len(self.projects) + 1)
            while any(p['id'] == project_id for p in self.projects):
                project_id = str(int(project_id) + 1)
            
            print(f"Generated project ID: {project_id}")  # Debug print

            # Create the project dictionary
            project = {
                'id': project_id,
                'name': str(name),
                'description': str(description),
                'funding_required': float(funding_required),
                'timeline': int(timeline),
                'sustainability_impact': str(sustainability_impact),
                'status': 'pending',
                'date_submitted': datetime.now().isoformat(),
                'funding_progress': 0,
                'timeline_progress': 0,
                'updates': [],
                'feedback': [],
                'environmental_score': 0,
                'social_score': 0,
                'governance_score': 0,
                'impact_metrics': [0, 0, 0, 0],  # Carbon, Water, Jobs, Energy
                'fund_seeker_id': str(fund_seeker_id),  # Ensure fund_seeker_id is string
                'location': 'Not specified'  # Add default location
            }

            print(f"Created project object: {project}")  # Debug print
            
            # Add new project and save
            self.projects.append(project)
            print("Added project to projects list")  # Debug print
            self._save_projects()
            
            return project
            
        except Exception as e:
            print(f"Error in create_project: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def update_project_status(self, project_id, status):
        """Update project status (approved/rejected)"""
        try:
            for project in self.projects:
                if str(project.get('id')) == str(project_id):
                    project['status'] = status
                    self._save_projects()
                    return True
            return False
        except Exception as e:
            print(f"Error updating project status: {str(e)}")
            return False

    def add_project_update(self, project_id, update_text):
        """Add an update to a project"""
        try:
            for project in self.projects:
                if str(project.get('id')) == str(project_id):
                    if 'updates' not in project:
                        project['updates'] = []
                    project['updates'].append({
                        'text': update_text,
                        'date': datetime.now().isoformat()
                    })
                    self._save_projects()
                    return True
            return False
        except Exception as e:
            print(f"Error adding project update: {str(e)}")
            return False
