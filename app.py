import os
import json
from datetime import datetime

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Import managers
from models.fund_seeker import FundSeekerManager
from models.real_time_manager import RealTimeManager
from models.esg_scorer import ESGScorer
from models.nlp_analyzer import NLPAnalyzer
from models.investment_optimizer import InvestmentOptimizer
from models.admin import AdminManager

# Initialize Flask app and extensions
server = Flask(__name__)
server.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'home'
socketio = SocketIO(server, cors_allowed_origins="*")

# Initialize managers
fund_seeker_manager = FundSeekerManager()
real_time_manager = RealTimeManager(socketio)
esg_scorer = ESGScorer()
nlp_analyzer = NLPAnalyzer()
optimizer = InvestmentOptimizer()
admin_manager = AdminManager()

class User(UserMixin):
    def __init__(self, user_id, role):
        self._id = str(user_id)  # Ensure ID is string
        self._role = role

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        return self._role

    def get_id(self):
        return self._id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    if 'user_role' not in session:
        return None
    return User(user_id, session['user_role'])

# Initialize and train the ESG scorer
try:
    esg_scorer.train()
    print("ESG model initialized and trained successfully")
except Exception as e:
    print(f"Error initializing ESG model: {str(e)}")

# Create Dash app
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Define the Dash layout
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

# Flask routes
@server.route('/')
def home():
    return render_template('home.html')

@server.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    if request.method == 'POST':
        try:
            user_id = request.form.get('username')  # In production, verify credentials
            if not user_id:
                flash('Username is required', 'error')
                return render_template('login.html', user_type=user_type)
            
            print(f"Logging in user: {user_id} as {user_type}")  # Debug print
            
            # Create and login user
            user = User(user_id, user_type)
            login_user(user)
            
            # Add user to admin manager
            admin_manager.add_user(user_id, user_type)
            
            # Store in session
            session['user_role'] = user_type
            session['user_id'] = str(user_id)
            
            print(f"Session after login: {session}")  # Debug print
            print(f"Current user: {current_user}")  # Debug print
            print(f"Current user ID: {current_user.id}")  # Debug print
            print(f"Current user role: {current_user.role}")  # Debug print
            
            if user_type == 'investor':
                return redirect(url_for('investor_dashboard'))
            elif user_type == 'fund-seeker':
                return redirect(url_for('fund_seeker_dashboard'))
            elif user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(f"Error in login: {str(e)}")
            import traceback
            traceback.print_exc()
            flash('Login error occurred', 'error')
    
    return render_template('login.html', user_type=user_type)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Fund Seeker Routes
@server.route('/fund-seeker/dashboard')
@login_required
def fund_seeker_dashboard():
    try:
        print(f"Session in dashboard: {session}")  # Debug print
        print(f"Current user: {current_user}")  # Debug print
        print(f"Current user ID: {current_user.id}")  # Debug print
        print(f"Current user role: {current_user.role}")  # Debug print
        
        if current_user.role != 'fund-seeker':
            flash('Access denied. Please login as a fund seeker.', 'error')
            return redirect(url_for('home'))
        
        # Get user's projects
        user_id = str(current_user.id)
        projects = fund_seeker_manager.get_user_projects(user_id)
        print(f"Found {len(projects)} projects for user {user_id}")  # Debug print
        
        if not projects:
            print("No projects found for user")  # Debug print
            flash('You have no projects yet. Submit a new project to get started!', 'info')
        else:
            print(f"Projects: {json.dumps(projects, indent=2)}")  # Debug print
        
        return render_template('fund_seeker_dashboard.html', projects=projects)
    except Exception as e:
        print(f"Error in fund_seeker_dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        flash('Error loading dashboard', 'error')
        return redirect(url_for('home'))

@server.route('/fund-seeker/submit-project', methods=['POST'])
@login_required
def submit_project():
    try:
        print(f"Session in submit: {session}")  # Debug print
        print(f"Current user: {current_user}")  # Debug print
        print(f"Current user ID: {current_user.id}")  # Debug print
        print(f"Current user role: {current_user.role}")  # Debug print
        
        if current_user.role != 'fund-seeker':
            flash('Access denied. Please login as a fund seeker.', 'error')
            return redirect(url_for('home'))
        
        print(f"Form data: {request.form}")  # Debug print
        
        # Validate form data
        required_fields = ['project_name', 'project_description', 'funding_required', 'project_timeline', 'sustainability_impact']
        for field in required_fields:
            if field not in request.form or not request.form[field]:
                flash(f'Missing required field: {field}', 'error')
                return redirect(url_for('fund_seeker_dashboard'))
        
        try:
            funding_required = float(request.form['funding_required'])
            timeline = int(request.form['project_timeline'])
            if funding_required <= 0 or timeline <= 0:
                flash('Funding required and timeline must be positive numbers', 'error')
                return redirect(url_for('fund_seeker_dashboard'))
        except ValueError:
            flash('Invalid funding required or timeline values', 'error')
            return redirect(url_for('fund_seeker_dashboard'))
        
        # Create project
        project = fund_seeker_manager.create_project(
            name=request.form['project_name'],
            description=request.form['project_description'],
            funding_required=funding_required,
            timeline=timeline,
            sustainability_impact=request.form['sustainability_impact'],
            fund_seeker_id=str(current_user.id)  # Ensure ID is string
        )
        
        if project is None:
            flash('Error creating project. Please try again.', 'error')
            return redirect(url_for('fund_seeker_dashboard'))
        
        print(f"Created project: {project}")  # Debug print
        
        # Notify admins
        try:
            real_time_manager.notify_project_update(
                project['id'],
                'new_project',
                {
                    'name': project['name'],
                    'description': project['description'],
                    'funding_required': project['funding_required']
                }
            )
        except Exception as e:
            print(f"Error notifying admins (non-critical): {str(e)}")
        
        flash('Project submitted successfully!', 'success')
        return redirect(url_for('fund_seeker_dashboard'))
        
    except Exception as e:
        print(f"Error in submit_project: {str(e)}")
        import traceback
        traceback.print_exc()
        flash('Error submitting project. Please try again.', 'error')
        return redirect(url_for('fund_seeker_dashboard'))

@server.route('/fund-seeker/add-update', methods=['POST'])
@login_required
def add_project_update():
    if current_user.role != 'fund-seeker':
        return redirect(url_for('home'))
    
    project_id = request.form['project_id']
    update_text = request.form['update_text']
    
    if fund_seeker_manager.add_project_update(project_id, update_text):
        flash('Update added successfully!', 'success')
    else:
        flash('Failed to add update.', 'error')
    
    return redirect(url_for('fund_seeker_dashboard'))

# Admin Routes
@server.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    # Get all projects
    all_projects = fund_seeker_manager.get_all_projects()
    
    # Convert projects to list if it's not already
    if isinstance(all_projects, dict):
        projects_list = [
            {**project, 'id': pid} 
            for pid, project in all_projects.items()
        ]
    else:
        projects_list = all_projects
    
    print(f"Users: {admin_manager.get_users()}")  # Debug print
    print(f"Projects: {projects_list}")  # Debug print
    print(f"Stats: {admin_manager.get_platform_stats()}")  # Debug print
    
    return render_template('admin_dashboard.html',
                         users=admin_manager.get_users(),
                         projects=projects_list,
                         stats=admin_manager.get_platform_stats())

@server.route('/admin/toggle-user-status/<user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    success = admin_manager.toggle_user_status(user_id)
    
    if success:
        # Notify about user status change
        real_time_manager.notify_user_status_change(
            user_id,
            'inactive' if success else 'active'
        )
    
    return jsonify({'success': success})

@server.route('/admin/approve-project/<project_id>', methods=['POST'])
@login_required
def approve_project(project_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    success = admin_manager.approve_project(project_id)
    
    if success:
        # Notify relevant parties about project approval
        real_time_manager.notify_status_change(project_id, 'approved')
    
    return jsonify({'success': success})

@server.route('/admin/reject-project/<project_id>', methods=['POST'])
@login_required
def reject_project(project_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    success = admin_manager.reject_project(project_id)
    
    if success:
        # Notify relevant parties about project rejection
        real_time_manager.notify_status_change(project_id, 'rejected')
    
    return jsonify({'success': success})

@server.route('/admin/update-esg-params', methods=['POST'])
@login_required
def update_esg_params():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    success = admin_manager.update_esg_params(
        data['env_weight'],
        data['social_weight'],
        data['gov_weight']
    )
    
    if success:
        # Notify all users about ESG parameter changes
        real_time_manager.notify_esg_parameter_change({
            'env_weight': data['env_weight'],
            'social_weight': data['social_weight'],
            'gov_weight': data['gov_weight']
        })
    
    return jsonify({'success': success})

# Analytics Routes
@server.route('/admin/analytics/user-growth')
@login_required
def get_user_growth():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    analytics = admin_manager.get_analytics_data()
    return jsonify(analytics['user_growth'])

@server.route('/admin/analytics/investment-trends')
@login_required
def get_investment_trends():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    analytics = admin_manager.get_analytics_data()
    return jsonify(analytics['investment_trends'])

@server.route('/admin/analytics/project-distribution')
@login_required
def get_project_distribution():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    analytics = admin_manager.get_analytics_data()
    return jsonify(analytics['project_distribution'])

@server.route('/admin/analytics/esg-distribution')
@login_required
def get_esg_distribution():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    analytics = admin_manager.get_analytics_data()
    return jsonify(analytics['esg_distribution'])

# Investor Routes
@server.route('/investor/dashboard')
@login_required
def investor_dashboard():
    if current_user.role != 'investor':
        return redirect(url_for('home'))
    
    try:
        # Get all approved projects
        projects = fund_seeker_manager.get_approved_projects()
        print(f"Found {len(projects)} approved projects")  # Debug print
        return render_template('investor_dashboard.html', projects=projects)
    except Exception as e:
        print(f"Error in investor_dashboard: {str(e)}")
        return "An error occurred", 500

@server.route('/api/projects/<project_id>')
@login_required
def get_project_details(project_id):
    if current_user.role != 'investor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        project = fund_seeker_manager.get_project_by_id(project_id)
        if project is None:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(project)
    except Exception as e:
        print(f"Error getting project details: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@server.route('/investor/submit-feedback', methods=['POST'])
@login_required
def submit_feedback():
    if current_user.role != 'investor':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    project_id = data.get('project_id')
    feedback_text = data.get('feedback')
    
    # Add feedback to the project
    success = fund_seeker_manager.add_feedback(
        project_id,
        current_user.id,
        feedback_text
    )
    
    if success:
        # Notify fund seeker about new feedback
        real_time_manager.notify_project_update(
            project_id,
            'feedback',
            {
                'text': feedback_text,
                'investor': current_user.id,
                'date': datetime.now().isoformat()
            }
        )
        
        return jsonify({
            'success': True,
            'feedback': {
                'text': feedback_text,
                'investor': current_user.id,
                'date': datetime.now().isoformat()
            }
        })
    
    return jsonify({'success': False, 'error': 'Failed to add feedback'})

@server.route('/investor/invest', methods=['POST'])
@login_required
def invest_in_project():
    if current_user.role != 'investor':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    project_id = data.get('project_id')
    amount = data.get('amount')
    
    # Process investment
    success = fund_seeker_manager.add_investment(
        project_id,
        current_user.id,
        amount
    )
    
    if success:
        # Notify about new investment
        real_time_manager.notify_funding_update(
            project_id,
            amount,
            current_user.id
        )
        
        return jsonify({
            'success': True,
            'new_total': fund_seeker_manager.get_project_funding(project_id)
        })
    
    return jsonify({'success': False, 'error': 'Failed to process investment'})

@server.route('/investor/optimize-portfolio', methods=['POST'])
@login_required
def optimize_portfolio():
    if current_user.role != 'investor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    project_id = data.get('project_id')
    risk_tolerance = float(data.get('risk_tolerance'))
    esg_priority = float(data.get('esg_priority'))
    investment_horizon = int(data.get('investment_horizon'))
    
    # Get optimization results
    optimization_results = optimizer.optimize(
        project_id,
        risk_tolerance,
        esg_priority,
        investment_horizon
    )
    
    return jsonify(optimization_results)

if __name__ == '__main__':
    socketio.run(server, debug=True, port=5001)
