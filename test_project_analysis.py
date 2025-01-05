from analysis.esg_scorer import ESGScorer
from analysis.nlp_analyzer import NLPAnalyzer

def test_project_analysis():
    # Sample project data
    project_data = {
        'description': """
        This renewable energy project aims to install solar panels across 100 acres of land,
        generating 50MW of clean electricity. The project will reduce CO2 emissions by 75,000 tons annually.
        The initiative includes community engagement programs and will create 200 local jobs.
        Project governance includes quarterly audits and transparent reporting to stakeholders.
        """,
        'metrics': {
            'environmental': {
                'co2_reduction': 75000,
                'renewable_energy_generation': 50,
                'land_use_efficiency': 0.5
            },
            'social': {
                'jobs_created': 200,
                'community_programs': 5,
                'local_business_involvement': 0.7
            },
            'governance': {
                'audit_frequency': 4,
                'compliance_score': 0.95,
                'stakeholder_meetings': 12
            }
        },
        'reports': [
            """
            Environmental Impact Assessment Report:
            The solar installation will have minimal impact on local wildlife.
            Biodiversity protection measures are in place.
            Water consumption will be 50% lower than industry standard.
            """,
            """
            Social Impact Report:
            Local community feedback has been positive.
            Training programs will be provided for all new employees.
            25% of jobs reserved for underrepresented groups.
            """,
            """
            Governance Framework:
            Monthly stakeholder meetings scheduled.
            Risk assessment conducted quarterly.
            All permits and regulations have been obtained.
            """
        ]
    }

    print("Testing Project Analysis System...")
    print("=" * 50)

    # Initialize analyzers
    esg_scorer = ESGScorer()
    nlp_analyzer = NLPAnalyzer()

    # 1. ESG Scoring
    print("\n1. ESG Scoring Analysis")
    print("-" * 30)
    esg_scores = esg_scorer.calculate_esg_scores(project_data)
    
    if esg_scores:
        print("\nFinal ESG Scores:")
        for category, score in esg_scores['final_scores'].items():
            print(f"{category.capitalize()}: {score:.2f}")
        print(f"\nOverall ESG Score: {esg_scores['overall_score']:.2f}")
        
        print("\nRecommendations:")
        recommendations = esg_scorer.get_recommendations(esg_scores)
        for rec in recommendations:
            print(f"- {rec}")

    # 2. NLP Analysis
    print("\n2. Natural Language Processing Analysis")
    print("-" * 30)
    
    # Combine all text for analysis
    all_text = project_data['description'] + ' '.join(project_data['reports'])
    
    # Extract key phrases
    print("\nKey Phrases:")
    key_phrases = nlp_analyzer.extract_key_phrases(all_text)
    for phrase in key_phrases[:5]:  # Show top 5
        print(f"- {phrase}")
    
    # Extract ESG insights
    print("\nESG Insights:")
    insights = nlp_analyzer.extract_esg_insights(all_text)
    for category, sentences in insights.items():
        print(f"\n{category.capitalize()}:")
        for sentence in sentences[:2]:  # Show first 2 insights per category
            print(f"- {sentence}")
    
    # Sentiment analysis
    print("\nSentiment Analysis by Aspect:")
    sentiments = nlp_analyzer.analyze_sentiment_by_aspect(all_text)
    for aspect, sentiment in sentiments.items():
        print(f"{aspect.capitalize()}: {sentiment:.2f}")
    
    # Extract metrics
    print("\nExtracted Metrics:")
    metrics = nlp_analyzer.extract_metrics(all_text)
    for metric in metrics[:5]:  # Show top 5 metrics
        print(f"- {metric['value']} ({metric['type']}): {metric['context']}")

if __name__ == "__main__":
    test_project_analysis()
