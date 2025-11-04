import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import SentimentChart from '../Charts/SentimentChart';
import { Search, Film, Star, TrendingUp } from 'lucide-react';
import './MovieSearch.css';

function MovieSearch() {
  const [movieName, setMovieName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { API_URL, getAuthHeader } = useAuth();

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!movieName.trim()) {
      setError('Please enter a movie name');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(
        `${API_URL}/analyze/movie`,
        { movie_name: movieName },
        { headers: getAuthHeader() }
      );
      setResult(response.data);
      
      if (response.data.error) {
        setError(response.data.error);
      }
    } catch (err) {
      console.error('Movie search error:', err);
      if (err.response?.status === 422 || err.response?.status === 401) {
        setError('Session expired. Please logout and login again.');
      } else {
        setError(err.response?.data?.error || 'Failed to search movie');
      }
    } finally {
      setLoading(false);
    }
  };

  const popularMovies = [
    'The Shawshank Redemption',
    'The Dark Knight',
    'Inception',
    'Pulp Fiction',
    'Forrest Gump',
    'The Matrix',
    'Interstellar',
    'Parasite'
  ];

  return (
    <div className="movie-search-container">
      <div className="search-header">
        <h1 className="fade-in">
          <Search size={36} />
          Movie Sentiment Search
        </h1>
        <p className="fade-in">Search for any movie and discover its sentiment based on ratings</p>
      </div>

      <div className="search-content">
        <div className="search-form-section card fade-in">
          <form onSubmit={handleSearch}>
            <div className="search-input-group">
              <Film size={24} color="#667eea" />
              <input
                type="text"
                className="search-input"
                value={movieName}
                onChange={(e) => setMovieName(e.target.value)}
                placeholder="Enter movie name (e.g., Inception, The Dark Knight)"
                required
              />
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? (
                  <span className="loading"></span>
                ) : (
                  <>
                    <Search size={20} />
                    Search
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="popular-movies">
            <h3>Popular Searches:</h3>
            <div className="popular-tags">
              {popularMovies.map((movie, index) => (
                <button
                  key={index}
                  className="popular-tag"
                  onClick={() => {
                    setMovieName(movie);
                    setResult(null);
                    setError('');
                  }}
                >
                  {movie}
                </button>
              ))}
            </div>
          </div>

          <div className="search-info">
            <h3>How it works:</h3>
            <ul>
              <li>Enter the name of any movie</li>
              <li>We fetch data from IMDB and other sources</li>
              <li>AI analyzes the ratings and reviews</li>
              <li>Get sentiment classification with detailed insights</li>
            </ul>
            <p className="info-note">
              <strong>Note:</strong> For best results, include the year if the movie name is common
              (e.g., "The Batman 2022")
            </p>
          </div>
        </div>

        {error && !result && (
          <div className="search-error card fade-in">
            <p>{error}</p>
            <p className="error-hint">Try checking the spelling or adding the release year</p>
          </div>
        )}

        {result && result.sources && result.sources.imdb && (
          <div className="search-results fade-in">
            <div className="search-result-header">
              <h2>Search Results for: <span className="searched-term">"{movieName}"</span></h2>
            </div>
            <div className="result-movie-info card">
              <div className="movie-poster-large">
                {result.sources.imdb.poster && result.sources.imdb.poster !== 'N/A' ? (
                  <img src={result.sources.imdb.poster} alt={result.sources.imdb.title} />
                ) : (
                  <div className="poster-placeholder">
                    <Film size={64} />
                  </div>
                )}
              </div>
              <div className="movie-details">
                <h2>{result.sources.imdb.title}</h2>
                <p className="movie-year">{result.sources.imdb.year}</p>
                
                {result.sources.imdb.imdb_rating && result.sources.imdb.imdb_rating !== 'N/A' && (
                  <div className="rating-section">
                    <div className="rating-item">
                      <Star size={24} fill="#fbbf24" color="#fbbf24" />
                      <div>
                        <span className="rating-value">{result.sources.imdb.imdb_rating}</span>
                        <span className="rating-label">IMDB Rating</span>
                      </div>
                    </div>
                    {result.sources.imdb.imdb_votes && result.sources.imdb.imdb_votes !== 'N/A' && (
                      <div className="rating-votes">
                        {result.sources.imdb.imdb_votes} votes
                      </div>
                    )}
                  </div>
                )}

                {result.sources.imdb.plot && result.sources.imdb.plot !== 'N/A' && (
                  <div className="movie-plot">
                    <h3>Plot</h3>
                    <p>{result.sources.imdb.plot}</p>
                  </div>
                )}
              </div>
            </div>

            <div className="result-sentiment-section card">
              <div className="sentiment-header">
                <TrendingUp size={32} color="#667eea" />
                <div>
                  <h3>Sentiment Analysis</h3>
                  <span className={`badge badge-${result.sentiment}`}>
                    {result.sentiment.toUpperCase()}
                  </span>
                </div>
              </div>
              <div className="confidence-bar">
                <div className="confidence-label">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </div>
                <div className="confidence-progress">
                  <div
                    className="confidence-fill"
                    style={{ width: `${result.confidence * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            <div className="result-charts-section card">
              <h3>Sentiment Distribution</h3>
              <SentimentChart data={result.detailed_scores} />
            </div>

            {result.sources.plot_analysis && (
              <div className="plot-analysis-section card">
                <h3>Plot Sentiment Analysis</h3>
                <div className="plot-sentiment-details">
                  <div className="sentiment-score">
                    <span className="score-label">VADER Compound Score</span>
                    <span className="score-value">
                      {result.sources.plot_analysis.vader_scores.compound}
                    </span>
                  </div>
                  <div className="sentiment-breakdown">
                    <div className="breakdown-item">
                      <span className="breakdown-label">Positive</span>
                      <span className="breakdown-value">
                        {(result.sources.plot_analysis.vader_scores.positive * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="breakdown-item">
                      <span className="breakdown-label">Neutral</span>
                      <span className="breakdown-value">
                        {(result.sources.plot_analysis.vader_scores.neutral * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="breakdown-item">
                      <span className="breakdown-label">Negative</span>
                      <span className="breakdown-value">
                        {(result.sources.plot_analysis.vader_scores.negative * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default MovieSearch;
