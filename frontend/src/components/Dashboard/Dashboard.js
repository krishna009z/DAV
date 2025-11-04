import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Star, FileText, Search, TrendingUp, BarChart3, Activity } from 'lucide-react';
import axios from 'axios';
import './Dashboard.css';

function Dashboard() {
  const { user, API_URL, getAuthHeader } = useAuth();
  const [stats, setStats] = useState({
    totalAnalyses: 0,
    positiveCount: 0,
    negativeCount: 0,
    neutralCount: 0
  });
  const [loading, setLoading] = useState(true);
  const [testText, setTestText] = useState('');
  const [testResult, setTestResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchUserStats();
  }, []);

  const fetchUserStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/history`, {
        headers: getAuthHeader()
      });
      const history = response.data;
      
      const stats = {
        totalAnalyses: history.length,
        positiveCount: history.filter(h => h.sentiment === 'positive').length,
        negativeCount: history.filter(h => h.sentiment === 'negative').length,
        neutralCount: history.filter(h => h.sentiment === 'neutral').length
      };
      
      setStats(stats);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickTest = async () => {
    if (!testText.trim()) return;
    
    setAnalyzing(true);
    setTestResult(null);
    
    try {
      const response = await axios.post(
        `${API_URL}/analyze/review`,
        { review_text: testText, movie_name: 'Quick Test' },
        { headers: getAuthHeader() }
      );
      setTestResult(response.data);
    } catch (error) {
      console.error('Error analyzing:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const quickTestSamples = [
    "This movie is absolutely amazing! Best film I've ever seen!",
    "Terrible movie, waste of time and money.",
    "It was okay, nothing special."
  ];

  const features = [
    {
      icon: <Star size={48} />,
      title: 'Famous Movies',
      description: 'Explore sentiment analysis of popular movies with detailed reviews and visualizations',
      link: '/famous-movies',
      color: '#fbbf24'
    },
    {
      icon: <FileText size={48} />,
      title: 'Custom Analysis',
      description: 'Paste any movie review and get instant sentiment analysis with advanced graphs',
      link: '/custom-analysis',
      color: '#667eea'
    },
    {
      icon: <Search size={48} />,
      title: 'Movie Search',
      description: 'Search for any movie by name and discover its sentiment based on IMDB ratings',
      link: '/movie-search',
      color: '#10b981'
    }
  ];

  return (
    <div className="dashboard-container">
      <div className="dashboard-hero">
        <h1 className="fade-in">Welcome back, {user?.username}! 🎬</h1>
        <p className="fade-in">Analyze movie reviews and discover sentiment trends with AI-powered insights</p>
      </div>

      <div className="features-grid">
        {features.map((feature, index) => (
          <Link
            key={index}
            to={feature.link}
            className="feature-card fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="feature-icon" style={{ color: feature.color }}>
              {feature.icon}
            </div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
            <div className="feature-arrow">→</div>
          </Link>
        ))}
      </div>

      <div className="info-section fade-in">
        <div className="info-card stats-card">
          <Activity size={32} color="#667eea" />
          <h3>Your Analysis Stats</h3>
          {loading ? (
            <div className="loading"></div>
          ) : (
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-number">{stats.totalAnalyses}</div>
                <div className="stat-label">Total Analyses</div>
              </div>
              <div className="stat-item">
                <div className="stat-number" style={{ color: '#10b981' }}>{stats.positiveCount}</div>
                <div className="stat-label">Positive</div>
              </div>
              <div className="stat-item">
                <div className="stat-number" style={{ color: '#ef4444' }}>{stats.negativeCount}</div>
                <div className="stat-label">Negative</div>
              </div>
              <div className="stat-item">
                <div className="stat-number" style={{ color: '#6366f1' }}>{stats.neutralCount}</div>
                <div className="stat-label">Neutral</div>
              </div>
            </div>
          )}
        </div>
        <div className="info-card">
          <BarChart3 size={32} color="#10b981" />
          <h3>Quick AI Test</h3>
          <p style={{ fontSize: '14px', marginBottom: '12px', color: '#6b7280' }}>
            Test our AI models instantly! Type or select a sample review:
          </p>
          
          <div className="quick-test-samples">
            {quickTestSamples.map((sample, idx) => (
              <button
                key={idx}
                className="sample-btn"
                onClick={() => setTestText(sample)}
              >
                Sample {idx + 1}
              </button>
            ))}
          </div>

          <textarea
            className="quick-test-input"
            value={testText}
            onChange={(e) => setTestText(e.target.value)}
            placeholder="Type a movie review here..."
            rows={3}
          />

          <button 
            className="btn btn-primary btn-full"
            onClick={handleQuickTest}
            disabled={analyzing || !testText.trim()}
          >
            {analyzing ? <span className="loading"></span> : 'Analyze Now'}
          </button>

          {testResult && (
            <div className="quick-test-result">
              <div className="result-sentiment">
                <span className={`badge badge-${testResult.sentiment}`}>
                  {testResult.sentiment.toUpperCase()}
                </span>
                <span className="result-confidence">
                  {(testResult.confidence * 100).toFixed(0)}% confident
                </span>
              </div>
              <div className="result-scores">
                <div className="score-item">
                  <span>Positive: {testResult.detailed_scores.positive.toFixed(1)}%</span>
                </div>
                <div className="score-item">
                  <span>Negative: {testResult.detailed_scores.negative.toFixed(1)}%</span>
                </div>
                <div className="score-item">
                  <span>Neutral: {testResult.detailed_scores.neutral.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
