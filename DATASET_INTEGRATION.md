# IMDB Dataset Integration

## Overview
The application now uses the **IMDB Dataset.csv** (50,000 movie reviews) instead of hardcoded movie data.

## Dataset Details
- **Location**: `C:\Users\KrishnaB\Downloads\IMDB Dataset.csv`
- **Total Reviews**: 50,000
- **Columns**: 
  - `review`: Movie review text
  - `sentiment`: Sentiment label (positive/negative)
- **Distribution**: 
  - Positive reviews: 25,000
  - Negative reviews: 25,000

## Changes Made

### 1. Updated `movie_data.py`
Replaced hardcoded movie data with CSV dataset functions:

#### New Functions:
- `load_imdb_dataset(limit=None)` - Load reviews from CSV
- `get_reviews_by_sentiment(sentiment_type, limit)` - Filter by sentiment
- `get_random_reviews(count)` - Get random sample
- `get_dataset_statistics()` - Get dataset stats
- `analyze_dataset_sample(sample_size)` - Analyze reviews with sentiment analyzer
- `get_famous_movies_data()` - Returns review collections organized by sentiment

### 2. Updated `app.py`
Added new API endpoints:

#### Dataset Endpoints:
- `GET /api/dataset/stats` - Get dataset statistics
- `GET /api/dataset/reviews?count=10` - Get random reviews
- `GET /api/dataset/reviews/sentiment/<type>?limit=10` - Get reviews by sentiment
- `GET /api/dataset/analyze-sample?sample_size=50` - Analyze sample reviews

### 3. Updated `requirements.txt`
Added pandas for CSV processing:
```
pandas>=2.1.0
```

## API Usage Examples

### Get Dataset Statistics
```bash
curl http://localhost:5000/api/dataset/stats
```

Response:
```json
{
  "total_reviews": 50000,
  "positive_reviews": 25000,
  "negative_reviews": 25000,
  "sentiment_distribution": {
    "positive": 25000,
    "negative": 25000
  }
}
```

### Get Random Reviews
```bash
curl http://localhost:5000/api/dataset/reviews?count=5
```

### Get Positive Reviews
```bash
curl http://localhost:5000/api/dataset/reviews/sentiment/positive?limit=10
```

### Get Negative Reviews
```bash
curl http://localhost:5000/api/dataset/reviews/sentiment/negative?limit=10
```

### Analyze Sample
```bash
curl http://localhost:5000/api/dataset/analyze-sample?sample_size=100
```

Response includes:
- Original sentiment from dataset
- Predicted sentiment from analyzer
- Confidence score
- Review preview

## Testing

Run the test script to verify integration:
```bash
cd backend
python test_dataset.py
```

## Configuration

To change the dataset location, update the `DATASET_PATH` variable in `movie_data.py`:
```python
DATASET_PATH = r'C:\path\to\your\IMDB Dataset.csv'
```

## Benefits

1. **Real Data**: Uses actual IMDB movie reviews instead of hardcoded samples
2. **Large Scale**: 50,000 reviews for comprehensive analysis
3. **Balanced**: Equal distribution of positive and negative sentiments
4. **Flexible**: Easy to filter, sample, and analyze subsets
5. **Extensible**: Can easily add more datasets or merge multiple sources

## Next Steps

Consider these enhancements:
1. Move CSV to backend folder for better organization
2. Add caching for faster repeated access
3. Implement pagination for large result sets
4. Add more filtering options (by length, keywords, etc.)
5. Create training/testing splits for model evaluation
6. Add data visualization endpoints
