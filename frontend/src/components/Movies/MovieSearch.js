import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import SentimentChart from '../Charts/SentimentChart';
import { Search, Film } from 'lucide-react';
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
          year: movieYear || null,
        },
        { headers: getAuthHeader() }
      );

      const data = response.data;
      console.log("✅ API Response:", data);

      if (data.error) {
        setError(data.error);
        return;
      }

      const imdb = data.sources?.imdb || {};

      const mappedResult = {
        sentiment: data.sentiment,
        confidence: data.confidence || 0,
        detailed_scores: data.detailed_scores || {
          positive: 0,
          neutral: 0,
          negative: 0,
        },
        sources: {
          imdb: {
            title: imdb.title || movieName,
            year: imdb.year || movieYear || "N/A",
            imdb_rating: imdb.imdb_rating !== null ? imdb.imdb_rating : "N/A",
            plot: imdb.plot || "Plot unavailable",
            poster: imdb.poster && imdb.poster !== "N/A"
              ? imdb.poster
              : "https://via.placeholder.com/300x450?text=No+Image",
          },
        },
      };

      setResult(mappedResult);

    } catch (err) {
      console.error("❌ API failed:", err.message);

      setError("Movie not found — showing mock data");

      setResult({
        sentiment: "neutral",
        confidence: 0.50,
        detailed_scores: {
          positive: 0.33,
          neutral: 0.34,
          negative: 0.33,
        },
        sources: {
          imdb: {
            title: movieName,
            year: movieYear || "2024",
            imdb_rating: "N/A",
            plot: "Plot unavailable — API failed.",
            poster: "https://via.placeholder.com/300x450?text=Movie+Poster"
          },
        },
      });
    } finally {
      setLoading(false);
    }
  };

  const popularMovies = [
    "The Shawshank Redemption", "The Dark Knight", "Inception",
    "Pulp Fiction", "Forrest Gump", "The Matrix",
    "Interstellar", "Parasite",
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

            <div className="result-movie-info card compact-header">
              <div className="movie-poster-large">
                {result.sources.imdb.poster ? (
                  <img src={result.sources.imdb.poster} alt="Movie Poster" />
                ) : <Film size={64} />}
              </div>

              <div className="movie-header-details">
                <h2 className="movie-title">{result.sources.imdb.title}</h2>
                <div className="movie-meta">

                  <span className="movie-year">{result.sources.imdb.year}</span>

                  <span className="imdb-badge">
                    ⭐ {result.sources.imdb.imdb_rating !== "N/A"
                      ? `${result.sources.imdb.imdb_rating}/10`
                      : "N/A"}
                  </span>

                  <span className={`sentiment-badge ${result.sentiment?.toLowerCase()}`}>
                    {result.sentiment?.toUpperCase()} • {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>

                <p className="movie-plot">{result.sources.imdb.plot}</p>
              </div>
            </div>

            {result.detailed_scores && (
              <div className="card">
                <h3>Sentiment Distribution</h3>
                <SentimentChart
                  data={result.detailed_scores}
                  showPie={true}
                  showBar={true}
                />
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
}

export default MovieSearch;
