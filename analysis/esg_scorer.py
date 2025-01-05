import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import spacy
import json

class ESGScorer:
    def __init__(self):
        # Download required NLTK data
        nltk.download('vader_lexicon')
        nltk.download('stopwords')
        
        self.sia = SentimentIntensityAnalyzer()
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.scaler = MinMaxScaler()
        self.nlp = spacy.load('en_core_web_sm')
        
        # Define ESG keywords and their weights
        self.esg_keywords = {
            'environmental': {
                'climate': 0.8,
                'emissions': 0.7,
                'renewable': 0.8,
                'sustainable': 0.6,
                'pollution': 0.7,
                'biodiversity': 0.6,
                'waste': 0.5,
                'energy': 0.7,
                'water': 0.6,
                'conservation': 0.5
            },
            'social': {
                'community': 0.7,
                'health': 0.8,
                'safety': 0.8,
                'diversity': 0.7,
                'inclusion': 0.7,
                'human rights': 0.9,
                'labor': 0.6,
                'education': 0.6,
                'poverty': 0.7,
                'equality': 0.8
            },
            'governance': {
                'transparency': 0.9,
                'compliance': 0.8,
                'ethics': 0.8,
                'corruption': 0.9,
                'accountability': 0.8,
                'risk': 0.7,
                'stakeholder': 0.6,
                'board': 0.7,
                'regulation': 0.7,
                'disclosure': 0.8
            }
        }

    def preprocess_text(self, text):
        """Preprocess text data"""
        doc = self.nlp(text.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        processed_sentences = []
        
        for sent in doc.sents:
            words = [token.text for token in sent if token.is_alpha and not token.is_stop]
            processed_sentences.append(' '.join(words))
        
        return ' '.join(processed_sentences)

    def calculate_keyword_score(self, text, category):
        """Calculate score based on keyword presence and weights"""
        text = text.lower()
        score = 0
        total_weight = 0
        
        for keyword, weight in self.esg_keywords[category].items():
            if keyword in text:
                score += text.count(keyword) * weight
                total_weight += weight
        
        return score / total_weight if total_weight > 0 else 0

    def calculate_sentiment_score(self, text):
        """Calculate sentiment score using VADER"""
        sentiment_scores = self.sia.polarity_scores(text)
        # Convert sentiment to 0-1 scale
        return (sentiment_scores['compound'] + 1) / 2

    def calculate_esg_scores(self, project_data):
        """
        Calculate ESG scores for a project
        project_data should contain:
        - description: text description of the project
        - metrics: dict of quantitative metrics
        - reports: list of relevant report texts
        """
        try:
            # Combine all text data
            all_text = project_data.get('description', '')
            all_text += ' ' + ' '.join(project_data.get('reports', []))
            processed_text = self.preprocess_text(all_text)
            
            # Calculate scores for each ESG component
            scores = {
                'environmental': {
                    'keyword_score': self.calculate_keyword_score(processed_text, 'environmental'),
                    'sentiment_score': self.calculate_sentiment_score(all_text)
                },
                'social': {
                    'keyword_score': self.calculate_keyword_score(processed_text, 'social'),
                    'sentiment_score': self.calculate_sentiment_score(all_text)
                },
                'governance': {
                    'keyword_score': self.calculate_keyword_score(processed_text, 'governance'),
                    'sentiment_score': self.calculate_sentiment_score(all_text)
                }
            }
            
            # Calculate quantitative metrics if available
            metrics = project_data.get('metrics', {})
            if metrics:
                for category in scores:
                    if category in metrics:
                        scores[category]['metric_score'] = self.calculate_metric_score(metrics[category])
            
            # Calculate final scores
            final_scores = self.calculate_final_scores(scores)
            
            return {
                'detailed_scores': scores,
                'final_scores': final_scores,
                'overall_score': sum(final_scores.values()) / 3
            }
        
        except Exception as e:
            print(f"Error calculating ESG scores: {str(e)}")
            return None

    def calculate_metric_score(self, metrics):
        """Calculate score from quantitative metrics"""
        if not metrics:
            return 0
            
        try:
            # Normalize metrics to 0-1 scale
            values = np.array(list(metrics.values())).reshape(-1, 1)
            normalized = self.scaler.fit_transform(values)
            return float(np.mean(normalized))
        except Exception as e:
            print(f"Error calculating metric score: {str(e)}")
            return 0

    def calculate_final_scores(self, scores):
        """Calculate final scores for each ESG component"""
        final_scores = {}
        
        for category in scores:
            category_scores = scores[category]
            # Weight distribution: keywords (40%), sentiment (30%), metrics (30%)
            final_score = (
                category_scores['keyword_score'] * 0.4 +
                category_scores['sentiment_score'] * 0.3 +
                category_scores.get('metric_score', 0) * 0.3
            )
            final_scores[category] = final_score
            
        return final_scores

    def get_recommendations(self, scores):
        """Generate recommendations based on ESG scores"""
        recommendations = []
        
        for category, score in scores['final_scores'].items():
            if score < 0.4:
                recommendations.append(f"Critical improvement needed in {category} aspects")
            elif score < 0.6:
                recommendations.append(f"Moderate improvement recommended in {category} aspects")
            elif score < 0.8:
                recommendations.append(f"Good performance in {category}, minor improvements possible")
            else:
                recommendations.append(f"Excellent performance in {category} aspects")
        
        return recommendations
