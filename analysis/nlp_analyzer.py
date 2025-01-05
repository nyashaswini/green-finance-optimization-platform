import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import defaultdict
import re

class NLPAnalyzer:
    def __init__(self):
        # Download required NLTK data
        nltk.download('vader_lexicon')
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_sm')
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # ESG-related keywords
        self.esg_keywords = {
            'environmental': [
                'environment', 'climate', 'emissions', 'renewable', 'sustainable',
                'pollution', 'biodiversity', 'waste', 'energy', 'water', 'conservation'
            ],
            'social': [
                'community', 'health', 'safety', 'diversity', 'inclusion',
                'human rights', 'labor', 'education', 'poverty', 'equality'
            ],
            'governance': [
                'transparency', 'compliance', 'ethics', 'corruption', 'accountability',
                'risk', 'stakeholder', 'board', 'regulation', 'disclosure'
            ]
        }

    def extract_key_phrases(self, text, top_n=5):
        """Extract key phrases using spaCy's noun chunks"""
        doc = self.nlp(text)
        noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks]
        
        # Filter out short phrases and those with stop words
        filtered_chunks = []
        for chunk in noun_chunks:
            words = chunk.lower().split()
            if (len(words) > 1 and 
                not all(word in self.stop_words for word in words)):
                filtered_chunks.append(chunk)
        
        # Sort by length and return top N
        sorted_chunks = sorted(filtered_chunks, key=len, reverse=True)
        return sorted_chunks[:top_n]

    def extract_esg_insights(self, text):
        """Extract sentences containing ESG-related insights"""
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        insights = defaultdict(list)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check each ESG category
            for category, keywords in self.esg_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    insights[category].append(sentence)
        
        return insights

    def analyze_sentiment_by_aspect(self, text):
        """Analyze sentiment for different ESG aspects"""
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        sentiments = defaultdict(list)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check which ESG aspect the sentence belongs to
            for aspect, keywords in self.esg_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    sentiment = self.sia.polarity_scores(sentence)
                    sentiments[aspect].append(sentiment['compound'])
        
        # Calculate average sentiment for each aspect
        avg_sentiments = {}
        for aspect, scores in sentiments.items():
            if scores:
                avg_sentiments[aspect] = sum(scores) / len(scores)
            else:
                avg_sentiments[aspect] = 0.0
        
        return avg_sentiments

    def extract_metrics(self, text):
        """Extract numerical metrics and their context"""
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        metrics = []
        
        # Regular expressions for different metric patterns
        patterns = {
            'QUANTITY': r'\d+(?:,\d{3})*(?:\.\d+)?\s*(?:MW|GW|kW|tons?|acres?|jobs?|people|employees)',
            'PERCENT': r'\d+(?:\.\d+)?%',
            'MONEY': r'\$\s*\d+(?:,\d{3})*(?:\.\d+)?(?:\s*(?:million|billion|trillion))?'
        }
        
        # Find all sentences with numbers
        for sentence in sentences:
            for metric_type, pattern in patterns.items():
                matches = re.finditer(pattern, sentence)
                for match in matches:
                    metrics.append({
                        'value': match.group(),
                        'type': metric_type,
                        'context': sentence.strip()
                    })
        
        return metrics
