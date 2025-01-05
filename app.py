import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

from models.esg_scorer import ESGScorer
from models.nlp_analyzer import NLPAnalyzer
from models.optimizer import InvestmentOptimizer

# Initialize components
esg_scorer = ESGScorer()
nlp_analyzer = NLPAnalyzer()
optimizer = InvestmentOptimizer()

# Initialize and train the ESG scorer
try:
    esg_scorer.train()
    print("ESG model initialized and trained successfully")
except Exception as e:
    print(f"Error initializing ESG model: {str(e)}")

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Green Finance Optimization Platform"),
    
    # Project Input Section
    html.Div([
        html.H3("Project Details"),
        dcc.Textarea(
            id='project-description',
            placeholder='Enter project description...',
            style={'width': '100%', 'height': 100}
        ),
        html.Button('Analyze Project', id='analyze-button', n_clicks=0)
    ]),
    
    # ESG Scores Display
    html.Div([
        html.H3("ESG Analysis Results"),
        dcc.Graph(id='esg-scores-graph')
    ]),
    
    # Portfolio Optimization Section
    html.Div([
        html.H3("Portfolio Optimization"),
        html.Div([
            html.Label("Total Budget (USD)"),
            dcc.Input(
                id='budget-input',
                type='number',
                value=10000000
            ),
            html.Label("Minimum ESG Score"),
            dcc.Slider(
                id='min-esg-slider',
                min=0,
                max=100,
                step=5,
                value=50,
                marks={i: str(i) for i in range(0, 101, 10)}
            ),
            html.Button('Optimize Portfolio', id='optimize-button', n_clicks=0)
        ]),
        dcc.Graph(id='optimization-results')
    ])
])

# Callbacks
@app.callback(
    Output('esg-scores-graph', 'figure'),
    [Input('analyze-button', 'n_clicks')],
    [State('project-description', 'value')]
)
def update_esg_analysis(n_clicks, description):
    if n_clicks is None or not description:
        # Return empty figure if no input
        return go.Figure()
    
    try:
        # Score the project using the description
        scores = esg_scorer.score_project_description(description)
        
        if scores is None:
            raise ValueError("Failed to generate ESG scores")
        
        # Create bar chart of scores
        categories = ['ESG Score', 'Environmental', 'Social', 'Governance']
        values = [
            scores['esg_score'],
            scores['environmental_score'],
            scores['social_score'],
            scores['governance_score']
        ]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
            )
        ])
        
        fig.update_layout(
            title='ESG Analysis Results',
            yaxis_title='Score',
            yaxis=dict(range=[0, 100]),
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in ESG analysis: {str(e)}")
        # Return empty figure on error
        return go.Figure()

@app.callback(
    Output('optimization-results', 'figure'),
    Input('optimize-button', 'n_clicks'),
    State('budget-input', 'value'),
    State('min-esg-slider', 'value')
)
def update_optimization(n_clicks, budget, min_esg):
    if n_clicks == 0:
        return {}
    
    # Generate synthetic projects
    projects = optimizer.generate_synthetic_projects()
    
    # Run optimization
    results = optimizer.optimize_portfolio(
        projects,
        total_budget=budget,
        min_esg_score=min_esg
    )
    
    # Create visualization
    allocations = results['project_allocations']
    df = pd.DataFrame(allocations)
    
    fig = px.scatter(
        df,
        x='expected_return',
        y='esg_impact',
        size='investment_amount',
        color='risk_score',
        hover_data=['project_name'],
        title='Portfolio Optimization Results'
    )
    
    fig.update_layout(
        xaxis_title='Expected Return (%)',
        yaxis_title='ESG Impact Score'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
