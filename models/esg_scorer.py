import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd

class ESGScorer:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'carbon_emissions',
            'renewable_energy',
            'waste_recycled',
            'community_impact',
            'job_creation',
            'transparency_score',
            'compliance_score'
        ]
        
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic ESG data for training"""
        np.random.seed(42)
        
        # Environmental metrics (with realistic ranges)
        carbon_emissions = np.random.normal(100, 30, n_samples)  # CO2 tons/year
        renewable_energy = np.random.uniform(0, 100, n_samples)  # % of total energy
        waste_recycled = np.random.uniform(0, 100, n_samples)    # % of waste recycled
        
        # Social metrics
        community_impact = np.random.uniform(0, 10, n_samples)   # Impact score
        job_creation = np.random.normal(500, 150, n_samples)     # Number of jobs
        
        # Governance metrics
        transparency_score = np.random.uniform(0, 100, n_samples)
        compliance_score = np.random.uniform(70, 100, n_samples)
        
        # Create feature matrix
        X = pd.DataFrame({
            'carbon_emissions': carbon_emissions,
            'renewable_energy': renewable_energy,
            'waste_recycled': waste_recycled,
            'community_impact': community_impact,
            'job_creation': job_creation,
            'transparency_score': transparency_score,
            'compliance_score': compliance_score
        })
        
        # Generate ESG scores with domain knowledge
        # Environmental component (40% weight)
        env_score = (
            (100 - carbon_emissions/200) * 0.4 +  # Lower emissions better
            renewable_energy * 0.4 +              # Higher renewable % better
            waste_recycled * 0.2                  # Higher recycling % better
        ) * 0.4
        
        # Social component (30% weight)
        social_score = (
            (community_impact/10 * 100) * 0.5 +   # Scale to 0-100
            (job_creation/1000 * 100) * 0.5       # Scale to 0-100
        ) * 0.3
        
        # Governance component (30% weight)
        gov_score = (
            transparency_score * 0.5 +
            compliance_score * 0.5
        ) * 0.3
        
        # Combined ESG score
        y = env_score + social_score + gov_score
        
        # Ensure scores are in 0-100 range
        y = np.clip(y, 0, 100)
        
        return X, y
    
    def train(self):
        """Train the ESG scoring model"""
        try:
            # Generate and split data
            X, y = self.generate_synthetic_data(n_samples=2000)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            self.scaler = self.scaler.fit(X_train)
            X_train_scaled = self.scaler.transform(X_train)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            self.is_trained = True
            
            print("ESG Model trained successfully")
            
        except Exception as e:
            print(f"Error training ESG model: {str(e)}")
            self.is_trained = False
    
    def score_project(self, project_data):
        """Score a project based on its ESG metrics"""
        try:
            if not self.is_trained:
                self.train()

            # Convert input data to correct format
            if isinstance(project_data, list):
                if len(project_data) != len(self.feature_names):
                    raise ValueError(f"Expected {len(self.feature_names)} features, got {len(project_data)}")
                project_df = pd.DataFrame([project_data], columns=self.feature_names)
            elif isinstance(project_data, dict):
                missing_features = set(self.feature_names) - set(project_data.keys())
                if missing_features:
                    raise ValueError(f"Missing features: {missing_features}")
                project_df = pd.DataFrame([project_data])
            else:
                raise ValueError("project_data must be a list or dictionary")
            
            # Ensure all required features are present
            project_df = project_df[self.feature_names]
            
            # Scale features
            X_scaled = self.scaler.transform(project_df)
            
            # Predict ESG score
            esg_score = float(self.model.predict(X_scaled)[0])
            
            # Calculate component scores
            env_score = float(self._calculate_environmental_score(project_df.iloc[0]))
            social_score = float(self._calculate_social_score(project_df.iloc[0]))
            gov_score = float(self._calculate_governance_score(project_df.iloc[0]))
            
            return {
                'esg_score': esg_score,
                'environmental_score': env_score,
                'social_score': social_score,
                'governance_score': gov_score
            }
            
        except Exception as e:
            print(f"Error in ESG scoring: {str(e)}")
            return None
    
    def _calculate_environmental_score(self, data):
        """Calculate environmental component score"""
        weights = [0.4, 0.4, 0.2]  # Weights for environmental metrics
        metrics = [
            100 - data['carbon_emissions']/200,  # Lower is better
            data['renewable_energy'],
            data['waste_recycled']
        ]
        return np.average(metrics, weights=weights)
    
    def _calculate_social_score(self, data):
        """Calculate social component score"""
        weights = [0.5, 0.5]  # Weights for social metrics
        metrics = [
            data['community_impact'] * 10,  # Scale to 0-100
            data['job_creation'] / 10       # Scale to 0-100
        ]
        return np.average(metrics, weights=weights)
    
    def _calculate_governance_score(self, data):
        """Calculate governance component score"""
        weights = [0.5, 0.5]  # Weights for governance metrics
        metrics = [
            data['transparency_score'],
            data['compliance_score']
        ]
        return np.average(metrics, weights=weights)

    def extract_metrics_from_description(self, description):
        """Extract ESG metrics from project description text"""
        # Default base values
        metrics = {
            'carbon_emissions': 100,  # Average baseline
            'renewable_energy': 0,
            'waste_recycled': 0,
            'community_impact': 0,
            'job_creation': 0,
            'transparency_score': 70,  # Base compliance level
            'compliance_score': 70     # Base compliance level
        }
        
        description = description.lower()
        
        # Environmental metrics
        if any(word in description for word in ['solar', 'renewable', 'clean energy']):
            metrics['renewable_energy'] = 90
            metrics['carbon_emissions'] = 20
        
        if any(word in description for word in ['recycl', 'waste management']):
            metrics['waste_recycled'] = 80
        
        # Social metrics
        job_mentions = description.count('job')
        if job_mentions > 0:
            # Extract number of jobs if mentioned
            import re
            job_numbers = re.findall(r'(\d+)\s*(?:permanent |temporary )?jobs?', description)
            if job_numbers:
                metrics['job_creation'] = sum(int(num) for num in job_numbers)
            else:
                metrics['job_creation'] = 100 * job_mentions
        
        if any(word in description for word in ['community', 'social', 'education']):
            metrics['community_impact'] = 8
        
        # Governance metrics
        if any(word in description for word in ['transparen', 'report', 'disclosure']):
            metrics['transparency_score'] = 90
        
        if any(word in description for word in ['compliance', 'standard', 'regulation']):
            metrics['compliance_score'] = 90
            
        return metrics

    def score_project_description(self, description):
        """Score a project based on its text description"""
        try:
            # Extract metrics from description
            metrics = self.extract_metrics_from_description(description)
            
            # Get scores using the extracted metrics
            return self.score_project(metrics)
            
        except Exception as e:
            print(f"Error in scoring project description: {str(e)}")
            return None
