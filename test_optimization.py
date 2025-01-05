from optimization.portfolio_optimizer import GreenPortfolioOptimizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def test_portfolio_optimization():
    print("Testing Green Portfolio Optimization...")
    print("=" * 50)
    
    # Initialize optimizer
    optimizer = GreenPortfolioOptimizer(risk_free_rate=0.02)
    
    # Sample data for 5 green investments
    assets = [
        "Solar Project A",
        "Wind Farm B",
        "Energy Storage C",
        "Smart Grid D",
        "Green Building E"
    ]
    
    # Sample expected returns (annual)
    expected_returns = {
        "Solar Project A": 0.15,
        "Wind Farm B": 0.12,
        "Energy Storage C": 0.10,
        "Smart Grid D": 0.13,
        "Green Building E": 0.08
    }
    
    # Sample ESG scores (0-1)
    esg_scores = {
        "Solar Project A": 0.85,
        "Wind Farm B": 0.90,
        "Energy Storage C": 0.75,
        "Smart Grid D": 0.80,
        "Green Building E": 0.95
    }
    
    # Sample covariance matrix
    cov_data = [
        [0.04, 0.02, 0.01, 0.02, 0.01],
        [0.02, 0.05, 0.02, 0.02, 0.01],
        [0.01, 0.02, 0.03, 0.01, 0.01],
        [0.02, 0.02, 0.01, 0.04, 0.02],
        [0.01, 0.01, 0.01, 0.02, 0.02]
    ]
    covariance_matrix = pd.DataFrame(cov_data, columns=assets, index=assets)
    
    # Test portfolio optimization
    print("\n1. Optimal Portfolio Allocation")
    print("-" * 30)
    
    result = optimizer.optimize_portfolio(
        expected_returns=expected_returns,
        esg_scores=esg_scores,
        covariance_matrix=covariance_matrix,
        total_budget=1000000,  # $1M investment
        min_esg_score=0.8,
        max_volatility=0.15
    )
    
    print("\nOptimal Portfolio Weights:")
    for asset, weight in result['optimal_weights'].items():
        print(f"{asset}: {weight:.2%}")
    
    print(f"\nPortfolio Metrics:")
    print(f"Expected Return: {result['expected_return']:.2%}")
    print(f"Volatility: {result['volatility']:.2%}")
    print(f"ESG Score: {result['esg_score']:.2f}")
    print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
    
    # Generate efficient frontier
    print("\n2. Generating Efficient Frontier")
    print("-" * 30)
    
    frontier_df = optimizer.generate_efficient_frontier(
        expected_returns=expected_returns,
        esg_scores=esg_scores,
        covariance_matrix=covariance_matrix,
        num_portfolios=1000
    )
    
    # Plot efficient frontier
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    scatter = plt.scatter(frontier_df['Volatility'], 
                         frontier_df['Return'],
                         c=frontier_df['ESG_Score'],
                         cmap='viridis',
                         s=frontier_df['Sharpe_Ratio']*100)
    
    # Add colorbar
    plt.colorbar(scatter, label='ESG Score')
    
    # Add labels and title
    plt.xlabel('Portfolio Volatility')
    plt.ylabel('Expected Return')
    plt.title('ESG-Adjusted Efficient Frontier')
    
    # Save plot
    plt.savefig('efficient_frontier.png')
    plt.close()
    
    print("\nEfficient Frontier Statistics:")
    print("\nTop 5 Portfolios by Sharpe Ratio:")
    print(frontier_df.nlargest(5, 'Sharpe_Ratio')[['Return', 'Volatility', 'ESG_Score', 'Sharpe_Ratio']])
    
    # Test real-time optimization
    print("\n3. Testing Real-Time Portfolio Optimization")
    print("-" * 30)
    
    # Use some sample green energy stocks
    green_stocks = ['ICLN', 'TAN', 'FAN', 'PBW', 'QCLN']
    
    try:
        result = optimizer.get_optimal_allocation(
            budget=1000000,
            risk_tolerance=0.7,
            min_esg_score=0.7,
            assets=green_stocks
        )
        
        print("\nOptimal Stock Portfolio:")
        for asset, weight in result['optimal_weights'].items():
            print(f"{asset}: {weight:.2%}")
        
        print(f"\nPortfolio Metrics:")
        print(f"Expected Return: {result['expected_return']:.2%}")
        print(f"Volatility: {result['volatility']:.2%}")
        print(f"ESG Score: {result['esg_score']:.2f}")
        print(f"Sharpe Ratio: {result['sharpe_ratio']:.2f}")
    
    except Exception as e:
        print(f"Error in real-time optimization: {str(e)}")

if __name__ == "__main__":
    test_portfolio_optimization()
