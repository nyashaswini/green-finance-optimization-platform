# Green Finance Optimization Platform

A platform that helps evaluate and optimize green finance investments using AI and data analytics.

## Project Structure
```
green_finance/
├── data/                 # Data storage
├── models/              # ML models
│   ├── esg_scorer.py    # ESG scoring model
│   ├── nlp_analyzer.py  # NLP analysis
│   └── optimizer.py     # Investment optimizer
├── dashboard/          # Web interface
│   ├── assets/         # CSS, JS files
│   └── layouts/        # Dashboard layouts
├── utils/             # Helper functions
└── app.py            # Main application
```

## Features
1. ESG Project Scoring
2. NLP-based Report Analysis
3. Investment Portfolio Optimization
4. Interactive Dashboard

## Free Data Sources Used
1. World Bank Climate Data API
2. Yahoo Finance ESG Data
3. EPA Environmental Database
4. UN Sustainable Development Goals Reports

## Setup
1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access dashboard at: http://localhost:8050
