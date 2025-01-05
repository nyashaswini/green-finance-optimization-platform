import numpy as np
import pandas as pd
from pulp import *
from scipy.optimize import minimize
import yfinance as yf
from typing import Dict, List, Tuple

class GreenPortfolioOptimizer:
    def __init__(self, risk_free_rate: float = 0.02):
        """
        Initialize the Green Portfolio Optimizer
        
        Args:
            risk_free_rate: Annual risk-free rate (default: 2%)
        """
        self.risk_free_rate = risk_free_rate
        self.daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    def calculate_portfolio_metrics(self, weights: np.ndarray, returns: np.ndarray, 
                                 esg_scores: np.ndarray, cov_matrix: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate portfolio return, risk, and ESG score
        
        Args:
            weights: Array of portfolio weights
            returns: Array of expected returns
            esg_scores: Array of ESG scores
            cov_matrix: Covariance matrix of returns
            
        Returns:
            Tuple of (expected return, volatility, esg_score)
        """
        portfolio_return = np.sum(returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        portfolio_esg_score = np.sum(esg_scores * weights)
        
        return portfolio_return, portfolio_volatility, portfolio_esg_score
    
    def optimize_portfolio(self, expected_returns: Dict[str, float], 
                         esg_scores: Dict[str, float],
                         covariance_matrix: pd.DataFrame,
                         total_budget: float,
                         min_esg_score: float = 0.6,
                         max_volatility: float = None,
                         min_return: float = None) -> Dict:
        """
        Optimize portfolio allocation using linear programming
        
        Args:
            expected_returns: Dict of asset expected returns
            esg_scores: Dict of asset ESG scores
            covariance_matrix: Covariance matrix of asset returns
            total_budget: Total investment budget
            min_esg_score: Minimum required ESG score (0-1)
            max_volatility: Maximum allowed portfolio volatility
            min_return: Minimum required portfolio return
            
        Returns:
            Dict containing optimal weights and portfolio metrics
        """
        # Create optimization problem
        prob = LpProblem("Green_Portfolio_Optimization", LpMaximize)
        
        # Decision variables (portfolio weights)
        assets = list(expected_returns.keys())
        weights = LpVariable.dicts("weights", assets, lowBound=0, upBound=1)
        
        # Objective: Maximize Sharpe Ratio proxy (return/risk + ESG score)
        portfolio_return = lpSum([weights[asset] * expected_returns[asset] for asset in assets])
        esg_contribution = lpSum([weights[asset] * esg_scores[asset] for asset in assets])
        
        # We'll maximize a combination of return and ESG score
        prob += portfolio_return + esg_contribution
        
        # Constraints
        # 1. Budget constraint
        prob += lpSum([weights[asset] for asset in assets]) == 1
        
        # 2. Minimum ESG score
        prob += lpSum([weights[asset] * esg_scores[asset] for asset in assets]) >= min_esg_score
        
        # 3. Maximum position size (diversification)
        for asset in assets:
            prob += weights[asset] <= 0.4  # No more than 40% in any single asset
        
        # 4. Minimum position size (if taken)
        for asset in assets:
            prob += weights[asset] >= 0.05  # At least 5% if position is taken
        
        # Solve the optimization problem
        prob.solve()
        
        # Extract results
        optimal_weights = {asset: value(weights[asset]) for asset in assets}
        
        # Calculate portfolio metrics
        weight_array = np.array([optimal_weights[asset] for asset in assets])
        returns_array = np.array([expected_returns[asset] for asset in assets])
        esg_array = np.array([esg_scores[asset] for asset in assets])
        
        port_return, port_vol, port_esg = self.calculate_portfolio_metrics(
            weight_array, returns_array, esg_array, covariance_matrix.values
        )
        
        # Calculate Sharpe Ratio
        sharpe_ratio = (port_return - self.risk_free_rate) / port_vol if port_vol > 0 else 0
        
        return {
            'optimal_weights': optimal_weights,
            'expected_return': port_return,
            'volatility': port_vol,
            'esg_score': port_esg,
            'sharpe_ratio': sharpe_ratio,
            'total_investment': total_budget
        }
    
    def generate_efficient_frontier(self, expected_returns: Dict[str, float],
                                  esg_scores: Dict[str, float],
                                  covariance_matrix: pd.DataFrame,
                                  num_portfolios: int = 100) -> pd.DataFrame:
        """
        Generate the ESG-adjusted efficient frontier
        
        Args:
            expected_returns: Dict of asset expected returns
            esg_scores: Dict of asset ESG scores
            covariance_matrix: Covariance matrix of asset returns
            num_portfolios: Number of portfolios to generate
            
        Returns:
            DataFrame with portfolio metrics along the efficient frontier
        """
        # Create arrays for storing results
        all_weights = []
        ret_arr = np.zeros(num_portfolios)
        vol_arr = np.zeros(num_portfolios)
        esg_arr = np.zeros(num_portfolios)
        sharpe_arr = np.zeros(num_portfolios)
        
        assets = list(expected_returns.keys())
        num_assets = len(assets)
        
        for i in range(num_portfolios):
            # Generate random weights
            weights = np.random.random(num_assets)
            weights = weights / np.sum(weights)
            
            # Calculate portfolio metrics
            weight_array = weights
            returns_array = np.array([expected_returns[asset] for asset in assets])
            esg_array = np.array([esg_scores[asset] for asset in assets])
            
            port_return, port_vol, port_esg = self.calculate_portfolio_metrics(
                weight_array, returns_array, esg_array, covariance_matrix.values
            )
            
            # Store results
            all_weights.append(weights)
            ret_arr[i] = port_return
            vol_arr[i] = port_vol
            esg_arr[i] = port_esg
            sharpe_arr[i] = (port_return - self.risk_free_rate) / port_vol if port_vol > 0 else 0
        
        # Create results DataFrame
        results = pd.DataFrame({
            'Return': ret_arr,
            'Volatility': vol_arr,
            'ESG_Score': esg_arr,
            'Sharpe_Ratio': sharpe_arr
        })
        
        # Add individual asset weights
        for idx, asset in enumerate(assets):
            results[f'Weight_{asset}'] = [w[idx] for w in all_weights]
        
        return results

    def get_optimal_allocation(self, budget: float, risk_tolerance: float,
                             min_esg_score: float, assets: List[str]) -> Dict:
        """
        Get optimal portfolio allocation based on current market data
        
        Args:
            budget: Total investment budget
            risk_tolerance: Risk tolerance level (0-1)
            min_esg_score: Minimum required ESG score (0-1)
            assets: List of asset tickers
            
        Returns:
            Dict with optimal allocation and portfolio metrics
        """
        # Fetch market data
        market_data = {}
        for ticker in assets:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            market_data[ticker] = hist['Close']
        
        # Calculate returns and covariance
        returns_df = pd.DataFrame(market_data).pct_change()
        expected_returns = returns_df.mean().to_dict()
        covariance_matrix = returns_df.cov()
        
        # Get ESG scores (you would typically get these from your ESG scoring system)
        # For now, we'll use dummy scores
        esg_scores = {ticker: np.random.uniform(0.5, 1.0) for ticker in assets}
        
        # Calculate maximum allowed volatility based on risk tolerance
        max_vol = risk_tolerance * np.sqrt(np.max(np.diag(covariance_matrix)))
        
        # Optimize portfolio
        result = self.optimize_portfolio(
            expected_returns=expected_returns,
            esg_scores=esg_scores,
            covariance_matrix=covariance_matrix,
            total_budget=budget,
            min_esg_score=min_esg_score,
            max_volatility=max_vol
        )
        
        return result
