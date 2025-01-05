import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

class NLPAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        try:
            nltk.data.find('sentiment/vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
            
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        
        # ESG-related keywords
        self.esg_keywords = {
            'environmental': [
                'renewable', 'sustainable', 'green', 'emission', 'carbon',
                'climate', 'environmental', 'recycling', 'biodiversity'
            ],
            'social': [
                'community', 'diversity', 'inclusion', 'employee', 'safety',
                'health', 'human rights', 'labor', 'education'
            ],
            'governance': [
                'transparency', 'compliance', 'ethics', 'board', 'corruption',
                'risk management', 'stakeholder', 'accountability'
            ]
        }
    
    def analyze_text(self, text):
        """Analyze project description or report text"""
        sentences = sent_tokenize(text.lower())
        words = word_tokenize(text.lower())
        
        # Remove stop words
        words = [w for w in words if w not in self.stop_words]
        
        # Calculate keyword frequencies
        keyword_scores = self._calculate_keyword_scores(words)
        
        # Sentiment analysis
        sentiment_scores = self._analyze_sentiment(sentences)
        
        # Risk analysis
        risk_score = self._analyze_risks(sentences)
        
        return {
            'keyword_scores': keyword_scores,
            'sentiment_scores': sentiment_scores,
            'risk_score': risk_score
        }
    
    def _calculate_keyword_scores(self, words):
        """Calculate frequency of ESG-related keywords"""
        scores = {
            'environmental': 0,
            'social': 0,
            'governance': 0
        }
        
        for category, keywords in self.esg_keywords.items():
            category_matches = sum(1 for word in words if any(
                keyword in word for keyword in keywords
            ))
            scores[category] = category_matches / len(words) if words else 0
            
        return scores
    
    def _analyze_sentiment(self, sentences):
        """Analyze sentiment of the text"""
        sentiments = []
        for sentence in sentences:
            sentiment_score = self.sia.polarity_scores(sentence)
            sentiments.append(sentiment_score['compound'])
            
        return {
            'average_sentiment': np.mean(sentiments),
            'sentiment_std': np.std(sentiments)
        }
    
    def _analyze_risks(self, sentences):
        """Analyze potential risks in the text"""
        risk_keywords = [
            'risk', 'challenge', 'problem', 'issue', 'concern',
            'difficulty', 'threat', 'weakness', 'limitation'
        ]
        
        risk_count = 0
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in risk_keywords):
                risk_count += 1
                
        risk_score = risk_count / len(sentences) if sentences else 0
        return risk_score
    
    def extract_key_metrics(self, text):
        """Extract numerical metrics from text"""
        metrics = {}
        
        # Look for numbers followed by relevant units
        number_patterns = [
            (r'\$?\d+\.?\d*\s*million', 'investment_amount'),
            (r'\d+\.?\d*\s*%', 'percentage'),
            (r'\d+\.?\d*\s*tons?', 'emissions'),
            (r'\d+\.?\d*\s*MW', 'energy_capacity')
        ]
        
        # Implementation would go here
        # For prototype, return dummy data
        metrics = {
            'investment_amount': 1000000,
            'percentage': 85,
            'emissions': 500,
            'energy_capacity': 50
        }
        
        return metrics
