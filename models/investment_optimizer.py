import numpy as np
from pulp import *

class InvestmentOptimizer:
    def __init__(self):
        """Initialize the Investment Optimizer"""
        pass

    def optimize_portfolio(self, projects, total_budget):
        """
        Optimize investment portfolio based on ESG scores and financial returns
        
        Args:
            projects (list): List of project dictionaries with ESG scores and expected returns
            total_budget (float): Total available budget for investment
            
        Returns:
            dict: Optimized allocation of funds to projects
        """
        try:
            # Create optimization problem
            prob = LpProblem("ESG_Portfolio_Optimization", LpMaximize)
            
            # Decision variables
            project_vars = LpVariable.dicts("Project",
                                          ((p['id']) for p in projects),
                                          0,
                                          1,
                                          LpContinuous)
            
            # Objective function: Maximize combined ESG score and expected return
            prob += lpSum([
                (p['environmental_score'] + p['social_score'] + p['governance_score']) * 0.7 +
                (float(p['funding_required']) * 0.3) * project_vars[p['id']]
                for p in projects
            ])
            
            # Budget constraint
            prob += lpSum([float(p['funding_required']) * project_vars[p['id']] for p in projects]) <= total_budget
            
            # Solve the problem
            prob.solve()
            
            # Get results
            allocation = {}
            for p in projects:
                allocation[p['id']] = project_vars[p['id']].value() if project_vars[p['id']].value() is not None else 0
            
            return allocation
            
        except Exception as e:
            print(f"Error in optimize_portfolio: {str(e)}")
            return None

    def calculate_esg_impact(self, projects, allocation):
        """
        Calculate the total ESG impact of the optimized portfolio
        
        Args:
            projects (list): List of project dictionaries
            allocation (dict): Optimized allocation of funds to projects
            
        Returns:
            dict: Total ESG impact scores
        """
        try:
            total_impact = {
                'environmental': 0,
                'social': 0,
                'governance': 0
            }
            
            for project in projects:
                if project['id'] in allocation:
                    weight = allocation[project['id']]
                    total_impact['environmental'] += project['environmental_score'] * weight
                    total_impact['social'] += project['social_score'] * weight
                    total_impact['governance'] += project['governance_score'] * weight
            
            return total_impact
            
        except Exception as e:
            print(f"Error in calculate_esg_impact: {str(e)}")
            return None

    def get_investment_recommendations(self, projects, budget):
        """
        Get investment recommendations based on optimization results
        
        Args:
            projects (list): List of project dictionaries
            budget (float): Available budget
            
        Returns:
            dict: Investment recommendations with allocations and impact scores
        """
        try:
            # Optimize portfolio
            allocation = self.optimize_portfolio(projects, budget)
            if not allocation:
                return None
            
            # Calculate impact
            impact = self.calculate_esg_impact(projects, allocation)
            if not impact:
                return None
            
            # Create recommendations
            recommendations = {
                'allocations': allocation,
                'impact_scores': impact,
                'total_investment': sum(float(p['funding_required']) * allocation[p['id']] 
                                     for p in projects if p['id'] in allocation),
                'projects_funded': len([pid for pid, alloc in allocation.items() if alloc > 0])
            }
            
            return recommendations
            
        except Exception as e:
            print(f"Error in get_investment_recommendations: {str(e)}")
            return None
