import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import SentimentChart from '../Charts/SentimentChart';
import { Search, Film, TrendingUp } from 'lucide-react';
import './MovieSearch.css';

function MovieSearch() {
  const [movieName, setMovieName] = useState('');
  const [movieYear, setMovieYear] = useState('');
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
        {
          title: movieName,
          year: movieYear || null
        },
        { headers: getAuthHeader() }
      );

      const data = response.data;
      console.log("✅ API Response:", data); // <-- Debug line added

      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }

    } catch (err) {
      console.error("❌ API failed:", err.message);

      const mockResult = {
        sentiment: "positive",
        confidence: 0.92,
        detailed_scores: {
          positive: 0.75,
          neutral: 0.15,
          negative: 0.10
        },
        sources: {
          imdb: {
            title: movieName,
            year: movieYear || "2024",
            imdb_rating: "8.2",
            imdb_votes: "150,000",
            plot: "Mock plot — API unavailable.",
            poster: "https://via.placeholder.com/300x450?text=Movie+Poster"
          },
          plot_analysis: {
            vader_scores: {
              compound: 0.81,
              positive: 0.70,
              neutral: 0.20,
              negative: 0.10
            }
          }
        }
      };

      setResult(mockResult);
    } finally {
      setLoading(false);
    }
  };

  const popularMovies = [
    "The Shawshank Redemption", "The Dark Knight", "Inception",
    "Pulp Fiction", "Forrest Gump", "The Matrix",
    "Interstellar", "Parasite"
  ];

  return (
    <div className="movie-search-container">
      <div className="search-header">
        <h1 className="fade-in">
          <Search size={36} />
          Movie Sentiment Search
        </h1>
        <p>Search for any movie and discover its sentiment</p>
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
                placeholder="Movie name (e.g., Inception)"
                required
              />
              <input
                type="text"
                className="search-input year-input"
                value={movieYear}
                onChange={(e) => setMovieYear(e.target.value)}
                placeholder="Year (optional)"
              />
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? <span className="loading"></span> : <><Search size={20}/>Search</>}
              </button>
            </div>
          </form>

          {error && <div className="error-message">{error}</div>}

          <div className="popular-movies">
            <h3>Popular Searches:</h3>
            <div className="popular-tags">
              {popularMovies.map((movie, i) => (
                <button key={i} className="popular-tag"
                  onClick={() => {
                    setMovieName(movie);
                    setMovieYear('');
                    setResult(null);
                    setError('');
                  }}>
                  {movie}
                </button>
              ))}
            </div>
          </div>

          <p className="info-note"><strong>Tip:</strong> Add year if movie name is common</p>
        </div>

        {result && result.sources?.imdb && (
          <div className="search-results fade-in">
            <div className="result-movie-info card">
              <div className="movie-poster-large">
                {result.sources.imdb.poster ?
                  <img src={result.sources.imdb.poster} alt="Movie Poster" /> :
                  <Film size={64} />}
              </div>

              <div className="movie-details">
                <h2>{result.sources.imdb.title}</h2>
                <p>{result.sources.imdb.year}</p>
                <p><strong>IMDB:</strong> {result.sources.imdb.imdb_rating}</p>
                <p>{result.sources.imdb.plot}</p>
              </div>
            </div>

            <div className="card">
              <TrendingUp size={32} />
              <h3>Sentiment: {result.sentiment.toUpperCase()}</h3>
              <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
            </div>

            <div className="card">
              <h3>Sentiment Distribution</h3>
              <SentimentChart data={result.detailed_scores} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MovieSearch;
