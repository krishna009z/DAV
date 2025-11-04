import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from sentiment_analyzer import SentimentAnalyzer

# Load environment variables
load_dotenv()

class MovieScraper:
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.omdb_api_key = os.getenv('OMDB_API_KEY', '')
        print(f"MovieScraper initialized with API key: {'*' * len(self.omdb_api_key) if self.omdb_api_key else 'NONE'}")
    
    def get_imdb_rating(self, movie_name):
        """Get IMDB rating using OMDB API"""
        try:
            if not self.omdb_api_key:
                print("ERROR: No OMDB API key found!")
                return None
            
            url = f"http://www.omdbapi.com/?apikey={self.omdb_api_key}&t={movie_name}"
            print(f"Fetching movie data from: {url}")
            response = requests.get(url, timeout=10)
            data = response.json()
            print(f"API Response: {data}")
            
            if data.get('Response') == 'True':
                return {
                    'title': data.get('Title'),
                    'year': data.get('Year'),
                    'imdb_rating': data.get('imdbRating'),
                    'imdb_votes': data.get('imdbVotes'),
                    'metascore': data.get('Metascore'),
                    'plot': data.get('Plot'),
                    'poster': data.get('Poster')
                }
            return None
        except Exception as e:
            print(f"Error fetching IMDB data: {e}")
            return None
    
    def estimate_sentiment_from_rating(self, rating):
        """Estimate sentiment from numeric rating"""
        try:
            rating_float = float(rating)
            if rating_float >= 7.0:
                return 'positive'
            elif rating_float >= 5.0:
                return 'neutral'
            else:
                return 'negative'
        except:
            return 'neutral'
    
    def get_movie_sentiment(self, movie_name):
        """Get movie sentiment based on ratings and reviews"""
        result = {
            'movie_name': movie_name,
            'sentiment': 'neutral',
            'confidence': 0.5,
            'sources': {}
        }
        
        # Try to get IMDB data
        imdb_data = self.get_imdb_rating(movie_name)
        
        if imdb_data:
            result['sources']['imdb'] = imdb_data
            
            # Estimate sentiment from IMDB rating
            if imdb_data.get('imdb_rating') and imdb_data['imdb_rating'] != 'N/A':
                rating = float(imdb_data['imdb_rating'])
                result['sources']['imdb']['sentiment'] = self.estimate_sentiment_from_rating(rating)
                result['sources']['imdb']['normalized_score'] = rating / 10.0
                
                # Update overall sentiment
                result['sentiment'] = result['sources']['imdb']['sentiment']
                result['confidence'] = rating / 10.0
            
            # Analyze plot as a review
            if imdb_data.get('plot') and imdb_data['plot'] != 'N/A':
                plot_analysis = self.analyzer.analyze_text(imdb_data['plot'])
                result['sources']['plot_analysis'] = plot_analysis
        else:
            result['error'] = 'Movie not found. Please check the movie name or try adding the year.'
        
        # Calculate detailed scores for visualization
        if result['sentiment'] == 'positive':
            result['detailed_scores'] = {
                'positive': result['confidence'] * 100,
                'negative': (1 - result['confidence']) * 30,
                'neutral': (1 - result['confidence']) * 20
            }
        elif result['sentiment'] == 'negative':
            result['detailed_scores'] = {
                'positive': (1 - result['confidence']) * 20,
                'negative': result['confidence'] * 100,
                'neutral': (1 - result['confidence']) * 30
            }
        else:
            result['detailed_scores'] = {
                'positive': 33.33,
                'negative': 33.33,
                'neutral': 33.34
            }
        
        return result
