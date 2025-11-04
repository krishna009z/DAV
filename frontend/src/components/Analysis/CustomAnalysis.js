import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../../context/AuthContext';
import SentimentChart from '../Charts/SentimentChart';
import DetailedAnalysis from '../Charts/DetailedAnalysis';
import { FileText, Send, TrendingUp } from 'lucide-react';
import './Analysis.css';

function CustomAnalysis() {
  const [reviewText, setReviewText] = useState('');
  const [movieName, setMovieName] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { API_URL, getAuthHeader } = useAuth();

  const handleAnalyze = async (e) => {
    e.preventDefault();
    
    if (!reviewText.trim()) {
      setError('Please enter a review to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const response = await axios.post(
        `${API_URL}/analyze/review`,
        {
          review_text: reviewText,
          movie_name: movieName
        },
        {
          headers: getAuthHeader()
        }
      );
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze review');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setReviewText('');
    setMovieName('');
    setAnalysis(null);
    setError('');
  };

  const sampleReviews = [
    "This movie was absolutely amazing! The cinematography was breathtaking and the performances were outstanding. I couldn't take my eyes off the screen.",
    "Terrible waste of time. The plot made no sense and the acting was wooden. I want my money back.",
    "It was okay, nothing special. Some good moments but overall pretty average and forgettable."
  ];

  const loadSample = (sample) => {
    setReviewText(sample);
    setAnalysis(null);
  };

  return (
    <div className="analysis-container">
      <div className="analysis-header">
        <h1 className="fade-in">
          <FileText size={36} />
          Custom Review Analysis
        </h1>
        <p className="fade-in">Paste any movie review and get instant sentiment analysis</p>
      </div>

      <div className="analysis-content">
        <div className="analysis-form-section card fade-in">
          <form onSubmit={handleAnalyze}>
            <div className="form-group">
              <label htmlFor="movieName">Movie Name (Optional)</label>
              <input
                id="movieName"
                type="text"
                className="input"
                value={movieName}
                onChange={(e) => setMovieName(e.target.value)}
                placeholder="Enter movie name (optional)"
              />
            </div>

            <div className="form-group">
              <label htmlFor="reviewText">Review Text *</label>
              <textarea
                id="reviewText"
                className="textarea"
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                placeholder="Paste or type your movie review here..."
                rows={8}
                required
              />
              <div className="character-count">
                {reviewText.length} characters
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? (
                  <span className="loading"></span>
                ) : (
                  <>
                    <Send size={20} />
                    Analyze Review
                  </>
                )}
              </button>
              <button type="button" className="btn btn-secondary" onClick={handleClear}>
                Clear
              </button>
            </div>
          </form>

          <div className="sample-reviews">
            <h3>Try Sample Reviews:</h3>
            <div className="sample-buttons">
              {sampleReviews.map((sample, index) => (
                <button
                  key={index}
                  className="sample-button"
                  onClick={() => loadSample(sample)}
                >
                  Sample {index + 1}
                </button>
              ))}
            </div>
          </div>
        </div>

        {analysis && (
          <div className="analysis-results fade-in">
            <div className="result-header card">
              <TrendingUp size={32} color="#667eea" />
              <div>
                <h2>Analysis Results</h2>
                {movieName && <p className="movie-name-result">for "{movieName}"</p>}
              </div>
            </div>

            <div className="result-sentiment card">
              <h3>Overall Sentiment</h3>
              <div className="sentiment-badge-large">
                <span className={`badge badge-${analysis.sentiment}`}>
                  {analysis.sentiment.toUpperCase()}
                </span>
                <span className="confidence-large">
                  {(analysis.confidence * 100).toFixed(1)}% Confidence
                </span>
              </div>
            </div>

            <div className="result-charts card">
              <h3>Sentiment Distribution</h3>
              <SentimentChart data={analysis.detailed_scores} />
            </div>

            <div className="result-detailed card">
              <h3>Detailed Analysis</h3>
              <DetailedAnalysis analysis={analysis} />
            </div>

            <div className="result-stats card">
              <h3>Text Statistics</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-label">Word Count</span>
                  <span className="stat-value">{analysis.word_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Character Count</span>
                  <span className="stat-value">{analysis.character_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Polarity</span>
                  <span className="stat-value">{analysis.textblob_scores.polarity.toFixed(3)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Subjectivity</span>
                  <span className="stat-value">{analysis.textblob_scores.subjectivity.toFixed(3)}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CustomAnalysis;
