import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from optimization.portfolio_optimizer import GreenPortfolioOptimizer
from analysis.esg_scorer import ESGScorer

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Initialize our optimization and scoring engines
optimizer = GreenPortfolioOptimizer()
esg_scorer = ESGScorer()

# Sample project data (in production, this would come from your database)
SAMPLE_PROJECTS = {
    "Solar Farm A": {
        "cost": 5000000,
        "expected_return": 0.15,
        "timeline_years": 5,
        "description": "50MW solar installation in Nevada",
        "category": "Solar",
        "risk_level": "Medium",
    },
    "Wind Farm B": {
        "cost": 8000000,
        "expected_return": 0.12,
        "timeline_years": 7,
        "description": "Offshore wind farm in Massachusetts",
        "category": "Wind",
        "risk_level": "High",
    },
    "Energy Storage C": {
        "cost": 3000000,
        "expected_return": 0.10,
        "timeline_years": 3,
        "description": "Grid-scale battery storage",
        "category": "Storage",
        "risk_level": "Low",
    },
    "Smart Grid D": {
        "cost": 4000000,
        "expected_return": 0.13,
        "timeline_years": 4,
        "description": "Smart grid implementation in California",
        "category": "Grid",
        "risk_level": "Medium",
    },
    "Green Building E": {
        "cost": 6000000,
        "expected_return": 0.08,
        "timeline_years": 10,
        "description": "LEED Platinum office complex",
        "category": "Building",
        "risk_level": "Low",
    }
}

def create_project_cards():
    """Create project information cards"""
    cards = []
    for name, data in SAMPLE_PROJECTS.items():
        card = html.Div([
            html.H4(name),
            html.P(f"Cost: ${data['cost']:,}"),
            html.P(f"Expected Return: {data['expected_return']*100:.1f}%"),
            html.P(f"Timeline: {data['timeline_years']} years"),
            html.P(f"Risk Level: {data['risk_level']}")
        ], className='project-card')
        cards.append(card)
    return cards

app.layout = html.Div([
    html.H1("Green Finance Investment Dashboard", className='dashboard-title'),
    
    # Main content container
    html.Div([
        # Left sidebar with filters
        html.Div([
            html.H3("Filters"),
            html.Label("Investment Budget Range"),
            dcc.RangeSlider(
                id='budget-range',
                min=1000000,
                max=20000000,
                step=1000000,
                marks={i: f"${i/1000000}M" for i in range(1000000, 21000000, 5000000)},
                value=[3000000, 10000000]
            ),
            
            html.Label("Minimum ESG Score"),
            dcc.Slider(
                id='min-esg-score',
                min=0,
                max=1,
                step=0.1,
                marks={i/10: str(i/10) for i in range(0, 11)},
                value=0.7
            ),
            
            html.Label("Risk Tolerance"),
            dcc.Slider(
                id='risk-tolerance',
                min=0,
                max=1,
                step=0.1,
                marks={i/10: str(i/10) for i in range(0, 11)},
                value=0.5
            ),
            
            html.Button("Run Scenario Analysis", id='scenario-button', className='button'),
            
        ], className='sidebar'),
        
        # Main content area
        html.Div([
            # Top row with key metrics
            html.Div([
                html.Div([
                    html.H4("Portfolio Overview"),
                    dcc.Graph(id='portfolio-sunburst')
                ], className='metric-card'),
                
                html.Div([
                    html.H4("ESG Distribution"),
                    dcc.Graph(id='esg-distribution')
                ], className='metric-card'),
                
                html.Div([
                    html.H4("Risk-Return Profile"),
                    dcc.Graph(id='risk-return-scatter')
                ], className='metric-card')
            ], className='metrics-row'),
            
            # Middle row with charts
            html.Div([
                html.Div([
                    html.H4("Efficient Frontier"),
                    dcc.Graph(id='efficient-frontier')
                ], className='chart-card'),
                
                html.Div([
                    html.H4("Project Rankings"),
                    dcc.Graph(id='project-rankings')
                ], className='chart-card')
            ], className='charts-row'),
            
            # Bottom row with scenario analysis
            html.Div([
                html.H3("Scenario Analysis"),
                html.Div([
                    dcc.Graph(id='scenario-comparison')
                ], className='scenario-card')
            ], className='scenario-row')
            
        ], className='main-content')
    ], className='content-container'),
    
    # Store for intermediate data
    dcc.Store(id='scenario-store'),
], className='dashboard-container')

@app.callback(
    [Output('portfolio-sunburst', 'figure'),
     Output('esg-distribution', 'figure'),
     Output('risk-return-scatter', 'figure'),
     Output('efficient-frontier', 'figure'),
     Output('project-rankings', 'figure'),
     Output('scenario-comparison', 'figure')],
    [Input('budget-range', 'value'),
     Input('min-esg-score', 'value'),
     Input('risk-tolerance', 'value'),
     Input('scenario-button', 'n_clicks')],
    [State('scenario-store', 'data')]
)
def update_dashboard(budget_range, min_esg_score, risk_tolerance, n_clicks, stored_scenarios):
    # Convert project data to DataFrame
    df = pd.DataFrame.from_dict(SAMPLE_PROJECTS, orient='index')
    df['name'] = df.index
    
    # Calculate ESG scores
    esg_scores = {name: np.random.uniform(0.6, 0.95) for name in SAMPLE_PROJECTS.keys()}
    df['esg_score'] = df.index.map(esg_scores)
    
    # 1. Portfolio Sunburst
    sunburst_fig = px.sunburst(
        df,
        path=['category', 'name'],
        values='cost',
        color='expected_return',
        color_continuous_scale='RdYlGn',
        title='Portfolio Composition'
    )
    
    # 2. ESG Distribution
    esg_fig = go.Figure()
    esg_fig.add_trace(go.Box(
        y=df['esg_score'],
        name='ESG Scores',
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    ))
    esg_fig.update_layout(title='ESG Score Distribution')
    
    # 3. Risk-Return Scatter
    risk_levels = {'Low': 0.2, 'Medium': 0.5, 'High': 0.8}
    df['risk_value'] = df['risk_level'].map(risk_levels)
    
    scatter_fig = px.scatter(
        df,
        x='risk_value',
        y='expected_return',
        size='cost',
        color='esg_score',
        hover_name='name',
        color_continuous_scale='RdYlGn',
        title='Risk-Return Profile'
    )
    
    # 4. Efficient Frontier
    frontier_results = optimizer.generate_efficient_frontier(
        expected_returns={name: data['expected_return'] for name, data in SAMPLE_PROJECTS.items()},
        esg_scores=esg_scores,
        covariance_matrix=pd.DataFrame(np.random.rand(5,5)*0.1, 
                                     index=SAMPLE_PROJECTS.keys(),
                                     columns=SAMPLE_PROJECTS.keys()),
        num_portfolios=100
    )
    
    frontier_fig = px.scatter(
        frontier_results,
        x='Volatility',
        y='Return',
        color='ESG_Score',
        color_continuous_scale='RdYlGn',
        title='Efficient Frontier'
    )
    
    # 5. Project Rankings
    df['score'] = (df['expected_return'] * 0.4 + 
                  df['esg_score'] * 0.4 + 
                  (1 - df['risk_value']) * 0.2)
    
    rankings_fig = px.bar(
        df.sort_values('score', ascending=True),
        y='name',
        x='score',
        orientation='h',
        color='score',
        color_continuous_scale='RdYlGn',
        title='Project Rankings'
    )
    
    # 6. Scenario Comparison
    # Generate three scenarios with different risk tolerances
    scenarios = {
        'Conservative': risk_tolerance * 0.5,
        'Balanced': risk_tolerance,
        'Aggressive': min(risk_tolerance * 1.5, 1.0)
    }
    
    scenario_results = []
    for scenario, risk_level in scenarios.items():
        result = optimizer.optimize_portfolio(
            expected_returns={name: data['expected_return'] for name, data in SAMPLE_PROJECTS.items()},
            esg_scores=esg_scores,
            covariance_matrix=pd.DataFrame(np.random.rand(5,5)*0.1, 
                                         index=SAMPLE_PROJECTS.keys(),
                                         columns=SAMPLE_PROJECTS.keys()),
            total_budget=budget_range[1],
            min_esg_score=min_esg_score,
            max_volatility=risk_level
        )
        scenario_results.append({
            'Scenario': scenario,
            'Return': result['expected_return'],
            'Risk': result['volatility'],
            'ESG Score': result['esg_score']
        })
    
    scenario_df = pd.DataFrame(scenario_results)
    
    scenario_fig = make_subplots(rows=1, cols=3, 
                                subplot_titles=('Expected Return', 'Risk', 'ESG Score'))
    
    metrics = ['Return', 'Risk', 'ESG Score']
    for i, metric in enumerate(metrics, 1):
        scenario_fig.add_trace(
            go.Bar(x=scenario_df['Scenario'], y=scenario_df[metric], name=metric),
            row=1, col=i
        )
    
    scenario_fig.update_layout(height=400, title_text="Scenario Comparison")
    
    return sunburst_fig, esg_fig, scatter_fig, frontier_fig, rankings_fig, scenario_fig

if __name__ == '__main__':
    app.run_server(debug=True)
