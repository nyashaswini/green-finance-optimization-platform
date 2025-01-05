from pulp import *
import numpy as np

class InvestmentOptimizer:
    def __init__(self):
        self.model = None
        
    def optimize_portfolio(self, projects, total_budget, min_esg_score=50):
        """
        Optimize investment allocation across projects
        
        Parameters:
        - projects: list of dict containing project details
          (each with 'name', 'cost', 'esg_score', 'expected_return', 'risk_score')
        - total_budget: total available budget
        - min_esg_score: minimum acceptable ESG score
        """
        
        # Create optimization problem
        prob = LpProblem("Green_Investment_Optimization", LpMaximize)
        
        # Decision variables: how much to invest in each project
        investment_vars = LpVariable.dicts("Invest",
                                         ((i) for i in range(len(projects))),
                                         0,
                                         None)
        
        # Objective: Maximize total ESG impact while considering returns
        prob += lpSum([investment_vars[i] * (
            0.7 * projects[i]['esg_score']/100 +  # 70% weight on ESG score
            0.3 * projects[i]['expected_return']/100  # 30% weight on financial return
        ) for i in range(len(projects))])
        
        # Constraints
        
        # Budget constraint
        prob += lpSum([investment_vars[i] for i in range(len(projects))]) <= total_budget
        
        # Minimum investment constraints
        for i in range(len(projects)):
            prob += investment_vars[i] <= projects[i]['cost']
        
        # Minimum ESG score constraint
        prob += lpSum([investment_vars[i] * projects[i]['esg_score'] 
                      for i in range(len(projects))]) >= min_esg_score * total_budget
        
        # Risk diversification constraint
        for i in range(len(projects)):
            prob += investment_vars[i] <= 0.4 * total_budget  # No more than 40% in one project
        
        # Solve the optimization problem
        prob.solve()
        
        # Extract results
        results = []
        for i in range(len(projects)):
            if value(investment_vars[i]) > 0:
                results.append({
                    'project_name': projects[i]['name'],
                    'investment_amount': value(investment_vars[i]),
                    'esg_impact': projects[i]['esg_score'] * value(investment_vars[i]) / total_budget,
                    'expected_return': projects[i]['expected_return'] * value(investment_vars[i]) / total_budget,
                    'risk_score': projects[i]['risk_score']
                })
        
        return {
            'optimization_status': LpStatus[prob.status],
            'total_esg_impact': sum(r['esg_impact'] for r in results),
            'total_expected_return': sum(r['expected_return'] for r in results),
            'allocated_budget': sum(r['investment_amount'] for r in results),
            'project_allocations': results
        }
    
    def generate_synthetic_projects(self, n_projects=10):
        """Generate synthetic project data for demonstration"""
        np.random.seed(42)
        
        projects = []
        for i in range(n_projects):
            project = {
                'name': f'Green Project {i+1}',
                'cost': np.random.uniform(1000000, 5000000),
                'esg_score': np.random.uniform(60, 95),
                'expected_return': np.random.uniform(5, 15),
                'risk_score': np.random.uniform(0.1, 0.5)
            }
            projects.append(project)
        
        return projects
