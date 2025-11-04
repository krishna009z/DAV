from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        # Remove special characters but keep punctuation for sentiment
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'@\w+', '', text)  # Remove mentions
        text = re.sub(r'#', '', text)  # Remove hashtags
        return text.strip()
    
    def analyze_with_vader(self, text):
        """Analyze sentiment using VADER"""
        scores = self.vader.polarity_scores(text)
        return scores
    
    def analyze_with_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        return {
            'polarity': polarity,
            'subjectivity': subjectivity
        }
    
    def get_sentiment_label(self, compound_score):
        """Convert compound score to sentiment label"""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_text(self, text):
        """Comprehensive sentiment analysis"""
        cleaned_text = self.clean_text(text)
        
        # VADER analysis
        vader_scores = self.analyze_with_vader(cleaned_text)
        
        # TextBlob analysis
        textblob_scores = self.analyze_with_textblob(cleaned_text)
        
        # Determine overall sentiment
        sentiment = self.get_sentiment_label(vader_scores['compound'])
        
        # Calculate confidence (using compound score magnitude)
        confidence = abs(vader_scores['compound'])
        
        # Detailed scores for visualization
        detailed_scores = {
            'positive': vader_scores['pos'] * 100,
            'negative': vader_scores['neg'] * 100,
            'neutral': vader_scores['neu'] * 100
        }
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'vader_scores': {
                'compound': round(vader_scores['compound'], 3),
                'positive': round(vader_scores['pos'], 3),
                'negative': round(vader_scores['neg'], 3),
                'neutral': round(vader_scores['neu'], 3)
            },
            'textblob_scores': {
                'polarity': round(textblob_scores['polarity'], 3),
                'subjectivity': round(textblob_scores['subjectivity'], 3)
            },
            'detailed_scores': detailed_scores,
            'word_count': len(cleaned_text.split()),
            'character_count': len(cleaned_text)
        }
    
    def analyze_multiple_reviews(self, reviews):
        """Analyze multiple reviews and aggregate results"""
        results = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        total_confidence = 0
        
        for review in reviews:
            analysis = self.analyze_text(review)
            results.append(analysis)
            sentiment_counts[analysis['sentiment']] += 1
            total_confidence += analysis['confidence']
        
        total_reviews = len(reviews)
        avg_confidence = total_confidence / total_reviews if total_reviews > 0 else 0
        
        # Calculate percentages
        sentiment_percentages = {
            'positive': (sentiment_counts['positive'] / total_reviews * 100) if total_reviews > 0 else 0,
            'negative': (sentiment_counts['negative'] / total_reviews * 100) if total_reviews > 0 else 0,
            'neutral': (sentiment_counts['neutral'] / total_reviews * 100) if total_reviews > 0 else 0
        }
        
        # Determine overall sentiment
        max_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        
        return {
            'overall_sentiment': max_sentiment,
            'average_confidence': round(avg_confidence, 3),
            'sentiment_counts': sentiment_counts,
            'sentiment_percentages': sentiment_percentages,
            'total_reviews': total_reviews,
            'individual_results': results
        }
