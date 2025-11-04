import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import './Charts.css';

function DetailedAnalysis({ analysis }) {
  const vaderData = [
    { name: 'Positive', value: analysis.vader_scores.positive * 100 },
    { name: 'Negative', value: analysis.vader_scores.negative * 100 },
    { name: 'Neutral', value: analysis.vader_scores.neutral * 100 },
    { name: 'Compound', value: (analysis.vader_scores.compound + 1) * 50 } // Normalize to 0-100
  ];

  const comparisonData = [
    {
      metric: 'Positive',
      VADER: analysis.vader_scores.positive * 100,
      Distribution: analysis.detailed_scores.positive
    },
    {
      metric: 'Negative',
      VADER: analysis.vader_scores.negative * 100,
      Distribution: analysis.detailed_scores.negative
    },
    {
      metric: 'Neutral',
      VADER: analysis.vader_scores.neutral * 100,
      Distribution: analysis.detailed_scores.neutral
    }
  ];

  const textBlobData = [
    { name: 'Polarity', value: (analysis.textblob_scores.polarity + 1) * 50 },
    { name: 'Subjectivity', value: analysis.textblob_scores.subjectivity * 100 }
  ];

  return (
    <div className="detailed-analysis-container">
      <div className="analysis-grid">
        <div className="analysis-chart">
          <h4>VADER Scores Breakdown</h4>
          <ResponsiveContainer width="100%" height={250}>
            <RadarChart data={vaderData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="name" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar
                name="VADER Scores"
                dataKey="value"
                stroke="#667eea"
                fill="#667eea"
                fillOpacity={0.6}
                animationBegin={0}
                animationDuration={1000}
                animationEasing="ease-out"
              />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="analysis-chart">
          <h4>Sentiment Comparison</h4>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={comparisonData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="metric" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="VADER" 
                stroke="#667eea" 
                strokeWidth={2}
                animationBegin={0}
                animationDuration={1200}
                animationEasing="ease-in-out"
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line 
                type="monotone" 
                dataKey="Distribution" 
                stroke="#10b981" 
                strokeWidth={2}
                animationBegin={200}
                animationDuration={1200}
                animationEasing="ease-in-out"
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="scores-summary">
        <div className="score-card">
          <h5>VADER Compound Score</h5>
          <div className="score-value-large">{analysis.vader_scores.compound}</div>
          <div className="score-bar">
            <div
              className="score-fill"
              style={{
                width: `${((analysis.vader_scores.compound + 1) / 2) * 100}%`,
                background: analysis.vader_scores.compound >= 0 ? '#10b981' : '#ef4444'
              }}
            ></div>
          </div>
          <p className="score-description">
            Range: -1 (most negative) to +1 (most positive)
          </p>
        </div>

        <div className="score-card">
          <h5>TextBlob Polarity</h5>
          <div className="score-value-large">{analysis.textblob_scores.polarity}</div>
          <div className="score-bar">
            <div
              className="score-fill"
              style={{
                width: `${((analysis.textblob_scores.polarity + 1) / 2) * 100}%`,
                background: analysis.textblob_scores.polarity >= 0 ? '#10b981' : '#ef4444'
              }}
            ></div>
          </div>
          <p className="score-description">
            Range: -1 (most negative) to +1 (most positive)
          </p>
        </div>

        <div className="score-card">
          <h5>TextBlob Subjectivity</h5>
          <div className="score-value-large">{analysis.textblob_scores.subjectivity}</div>
          <div className="score-bar">
            <div
              className="score-fill"
              style={{
                width: `${analysis.textblob_scores.subjectivity * 100}%`,
                background: '#6366f1'
              }}
            ></div>
          </div>
          <p className="score-description">
            Range: 0 (objective) to 1 (subjective)
          </p>
        </div>
      </div>
    </div>
  );
}

export default DetailedAnalysis;
