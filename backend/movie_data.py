import pandas as pd
import os
from sentiment_analyzer import SentimentAnalyzer

# Path to the IMDB dataset
DATASET_PATH = r'C:\Users\KrishnaB\Downloads\IMDB Dataset.csv'

def load_imdb_dataset(limit=None):
    """Load IMDB dataset from CSV file"""
    try:
        df = pd.read_csv(DATASET_PATH)
        if limit:
            df = df.head(limit)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def get_reviews_by_sentiment(sentiment_type='positive', limit=10):
    """Get reviews filtered by sentiment type"""
    df = load_imdb_dataset()
    if df is None:
        return []
    
    filtered = df[df['sentiment'] == sentiment_type].head(limit)
    return filtered['review'].tolist()

def get_random_reviews(count=10):
    """Get random reviews from the dataset"""
    df = load_imdb_dataset()
    if df is None:
        return []
    
    sample = df.sample(n=min(count, len(df)))
    return sample.to_dict('records')

def get_dataset_statistics():
    """Get statistics about the dataset"""
    df = load_imdb_dataset()
    if df is None:
        return {}
    
    stats = {
        'total_reviews': len(df),
        'positive_reviews': len(df[df['sentiment'] == 'positive']),
        'negative_reviews': len(df[df['sentiment'] == 'negative']),
        'sentiment_distribution': df['sentiment'].value_counts().to_dict()
    }
    return stats

def analyze_dataset_sample(sample_size=100):
    """Analyze a sample of reviews from the dataset"""
    analyzer = SentimentAnalyzer()
    df = load_imdb_dataset(limit=sample_size)
    
    if df is None:
        return None
    
    results = []
    for idx, row in df.iterrows():
        analysis = analyzer.analyze_text(row['review'])
        results.append({
            'original_sentiment': row['sentiment'],
            'predicted_sentiment': analysis['sentiment'],
            'confidence': analysis['confidence'],
            'review_preview': row['review'][:100] + '...'
        })
    
    return results

def get_famous_movies_data():
    """Return sample reviews from IMDB dataset organized by sentiment"""
    analyzer = SentimentAnalyzer()
    df = load_imdb_dataset(limit=50)
    
    if df is None:
        return []
    
    # Group reviews by sentiment and create movie-like entries
    movies = []
    
    # Get positive reviews
    positive_reviews = df[df['sentiment'] == 'positive'].head(10)['review'].tolist()
    if positive_reviews:
        movies.append({
            'id': 1,
            'title': 'Highly Rated Movies Collection',
            'category': 'positive',
            'reviews': positive_reviews[:5],
            'total_reviews': len(positive_reviews)
        })
    
    # Get negative reviews
    negative_reviews = df[df['sentiment'] == 'negative'].head(10)['review'].tolist()
    if negative_reviews:
        movies.append({
            'id': 2,
            'title': 'Poorly Rated Movies Collection',
            'category': 'negative',
            'reviews': negative_reviews[:5],
            'total_reviews': len(negative_reviews)
        })
    
    # Analyze reviews for each collection
    for movie in movies:
        if movie['reviews']:
            analysis = analyzer.analyze_multiple_reviews(movie['reviews'])
            movie['sentiment_analysis'] = {
                'overall_sentiment': analysis['overall_sentiment'],
                'sentiment_percentages': analysis['sentiment_percentages'],
                'average_confidence': analysis['average_confidence'],
                'total_reviews': len(movie['reviews'])
            }
    
    return movies
