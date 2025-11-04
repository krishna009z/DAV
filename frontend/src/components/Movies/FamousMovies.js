import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import SentimentChart from '../Charts/SentimentChart';
import { Star, TrendingUp } from 'lucide-react';
import './Movies.css';

function FamousMovies() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const { API_URL } = useAuth();

  useEffect(() => {
    fetchFamousMovies();
  }, []);

  const fetchFamousMovies = async () => {
    try {
      const response = await axios.get(`${API_URL}/movies/famous`);
      setMovies(response.data);
    } catch (error) {
      console.error('Error fetching movies:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return '#10b981';
      case 'negative':
        return '#ef4444';
      default:
        return '#6366f1';
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading"></div>
        <p>Loading famous movies...</p>
      </div>
    );
  }

  return (
    <div className="movies-container">
      <div className="movies-header">
        <h1 className="fade-in">
          <Star size={36} />
          Famous Movies Analysis
        </h1>
        <p className="fade-in">Explore sentiment analysis of popular movies with detailed reviews</p>
      </div>

      <div className="movies-grid">
        {movies.map((movie, index) => (
          <div
            key={movie.id}
            className="movie-card fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
            onClick={() => setSelectedMovie(movie)}
          >
            <div className="movie-poster">
              <img src={movie.poster} alt={movie.title} />
              <div className="movie-rating">
                <Star size={16} fill="#fbbf24" color="#fbbf24" />
                {movie.imdb_rating}
              </div>
            </div>
            <div className="movie-info">
              <h3>{movie.title}</h3>
              <p className="movie-year">{movie.year}</p>
              <div className="movie-sentiment">
                <span
                  className={`badge badge-${movie.sentiment_analysis.overall_sentiment}`}
                >
                  {movie.sentiment_analysis.overall_sentiment.toUpperCase()}
                </span>
                <span className="sentiment-confidence">
                  {(movie.sentiment_analysis.average_confidence * 100).toFixed(0)}% confidence
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedMovie && (
        <div className="modal-overlay" onClick={() => setSelectedMovie(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedMovie(null)}>
              ×
            </button>
            
            <div className="modal-header">
              <img src={selectedMovie.poster} alt={selectedMovie.title} className="modal-poster" />
              <div className="modal-title-section">
                <h2>{selectedMovie.title}</h2>
                <p className="modal-year">{selectedMovie.year}</p>
                <div className="modal-rating">
                  <Star size={20} fill="#fbbf24" color="#fbbf24" />
                  <span>{selectedMovie.imdb_rating} IMDB Rating</span>
                </div>
              </div>
            </div>

            <div className="modal-sentiment">
              <div className="sentiment-overview">
                <TrendingUp size={24} />
                <div>
                  <h3>Overall Sentiment</h3>
                  <span className={`badge badge-${selectedMovie.sentiment_analysis.overall_sentiment}`}>
                    {selectedMovie.sentiment_analysis.overall_sentiment.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            <div className="modal-charts">
              <SentimentChart data={selectedMovie.sentiment_analysis.sentiment_percentages} />
            </div>

            <div className="modal-reviews">
              <h3>Sample Reviews ({selectedMovie.reviews.length})</h3>
              {selectedMovie.reviews.map((review, index) => (
                <div key={index} className="review-item">
                  <p>{review}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default FamousMovies;
