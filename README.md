# Movie Review Sentiment Analysis Website

A comprehensive web application for analyzing movie reviews using advanced AI sentiment analysis. Built with React frontend and Flask backend.

## Features

### 🎬 Famous Movies Section
- Browse popular movies with pre-analyzed reviews
- View detailed sentiment breakdowns with interactive charts
- See IMDB ratings and movie information
- Multiple visualization types (pie charts, bar charts)

### 📝 Custom Review Analysis
- Paste any movie review for instant analysis
- Get sentiment classification (Positive/Negative/Neutral)
- View confidence scores and detailed metrics
- Advanced visualizations including:
  - Sentiment distribution charts
  - VADER score breakdowns
  - TextBlob polarity and subjectivity analysis
  - Radar charts and line graphs

### 🔍 Movie Search by Name
- Search any movie by name
- Fetches data from IMDB via OMDB API
- Analyzes sentiment based on ratings
- Displays movie posters, plots, and ratings
- Sentiment analysis of movie descriptions

### 🔐 Authentication
- User registration and login
- JWT-based authentication
- Secure password hashing with bcrypt
- Protected routes and API endpoints

## Technology Stack

### Backend
- **Flask** - Python web framework
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SQLAlchemy** - Database ORM
- **VADER Sentiment** - Sentiment analysis
- **TextBlob** - Natural language processing
- **OMDB API** - Movie data integration

### Frontend
- **React** - UI framework
- **React Router** - Navigation
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file (copy from `.env.example`):
```bash
copy .env.example .env
```

6. Get a free OMDB API key from https://www.omdbapi.com/apikey.aspx and add it to `.env`:
```
OMDB_API_KEY=your-api-key-here
```

7. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Access your account
3. **Dashboard**: View overview of all features
4. **Famous Movies**: Browse and analyze popular movies
5. **Custom Analysis**: Paste any review for instant analysis
6. **Movie Search**: Search movies by name for sentiment insights

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/verify` - Verify JWT token

### Analysis
- `POST /api/analyze/review` - Analyze custom review text
- `POST /api/analyze/movie` - Search and analyze movie by name
- `GET /api/movies/famous` - Get famous movies with analysis
- `GET /api/history` - Get user's analysis history

## Sentiment Analysis Models

### VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Specialized for social media and short texts
- Provides compound, positive, negative, and neutral scores
- Range: -1 (most negative) to +1 (most positive)

### TextBlob
- Provides polarity and subjectivity scores
- Polarity: -1 (negative) to +1 (positive)
- Subjectivity: 0 (objective) to 1 (subjective)

## Project Structure

```
moviereviewanalysis/
├── backend/
│   ├── app.py                 # Flask application
│   ├── sentiment_analyzer.py  # Sentiment analysis logic
│   ├── movie_scraper.py       # Movie data fetching
│   ├── movie_data.py          # Famous movies data
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/         # Login/Signup
│   │   │   ├── Dashboard/    # Main dashboard
│   │   │   ├── Movies/       # Famous movies & search
│   │   │   ├── Analysis/     # Custom analysis
│   │   │   ├── Charts/       # Visualization components
│   │   │   └── Layout/       # Navbar
│   │   ├── context/
│   │   │   └── AuthContext.js # Authentication context
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Features in Detail

### Advanced Visualizations
- **Pie Charts**: Overall sentiment distribution
- **Bar Charts**: Comparative sentiment scores
- **Radar Charts**: Multi-dimensional VADER analysis
- **Line Charts**: Sentiment comparison across models
- **Progress Bars**: Confidence and score indicators

### Analysis Metrics
- Overall sentiment (Positive/Negative/Neutral)
- Confidence score
- VADER compound score
- Positive/Negative/Neutral percentages
- TextBlob polarity and subjectivity
- Word and character counts

## Security Features
- Password hashing with bcrypt
- JWT token authentication
- Protected API routes
- CORS configuration
- SQL injection prevention with SQLAlchemy

## Future Enhancements
- Integration with more movie databases (Letterboxd, Rotten Tomatoes)
- Real-time review scraping
- User review history and favorites
- Batch analysis of multiple reviews
- Export analysis results
- Social sharing features

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the MIT License.

## Support
For issues and questions, please create an issue in the repository.

## Acknowledgments
- VADER Sentiment Analysis
- TextBlob NLP Library
- OMDB API
- React and Flask communities
