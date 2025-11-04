# Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Install Backend Dependencies

Open a terminal in the `backend` folder and run:

```bash
cd c:/moviereviewanalysis/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Get OMDB API Key (Optional but Recommended)

1. Visit https://www.omdbapi.com/apikey.aspx
2. Sign up for a FREE API key
3. Open `backend/.env` file
4. Add your API key: `OMDB_API_KEY=your-key-here`

**Note**: The app works without this, but the Movie Search feature requires it.

### Step 3: Start Backend Server

```bash
python app.py
```

You should see: `Running on http://127.0.0.1:5000`

### Step 4: Install Frontend Dependencies

Open a NEW terminal in the `frontend` folder:

```bash
cd c:/moviereviewanalysis/frontend
npm install
```

### Step 5: Start Frontend

```bash
npm start
```

Browser will open automatically at `http://localhost:3000`

## First Time Usage

1. **Sign Up**: Create an account with username, email, and password
2. **Login**: Use your credentials to login
3. **Explore Features**:
   - **Dashboard**: Overview of all features
   - **Famous Movies**: See 8 popular movies with sentiment analysis
   - **Custom Analysis**: Paste any review and click "Analyze Review"
   - **Movie Search**: Type a movie name (e.g., "Inception") and click "Search"

## Troubleshooting

### Backend Issues
- **Port 5000 already in use**: Change port in `app.py` (last line)
- **Module not found**: Make sure virtual environment is activated

### Frontend Issues
- **Port 3000 already in use**: The app will ask to use port 3001
- **npm install fails**: Try `npm install --legacy-peer-deps`

### API Issues
- **Movie Search not working**: Add OMDB API key to `.env` file
- **CORS errors**: Make sure backend is running on port 5000

## Sample Data

Try these movie names in Movie Search:
- The Shawshank Redemption
- The Dark Knight
- Inception
- Pulp Fiction
- Forrest Gump

Try these sample reviews in Custom Analysis:
- "This movie was absolutely amazing! The cinematography was breathtaking."
- "Terrible waste of time. The plot made no sense."
- "It was okay, nothing special. Pretty average overall."

## What You Get

✅ User authentication (signup/login)
✅ Famous movies with sentiment analysis
✅ Custom review analysis with AI
✅ Movie search by name (IMDB integration)
✅ Advanced visualizations:
   - Pie charts
   - Bar charts
   - Radar charts
   - Line graphs
   - Progress bars
✅ Multiple AI models (VADER + TextBlob)
✅ Beautiful modern UI
✅ Responsive design

Enjoy analyzing movie reviews! 🎬🍿
