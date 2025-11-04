from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import timedelta, datetime
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Basic app config
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Use DATABASE_URL environment variable but treat it as the MongoDB URI
# If you want to keep the same env var name DATABASE_URL (as requested), set it in Render to the Atlas URI.
app.config["MONGO_URI"] = os.getenv(
    "DATABASE_URL",
    "mongodb+srv://dav:dav@dav.kpmskka.mongodb.net/dav?retryWrites=true&w=majority"
)

# Initialize extensions
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})
jwt = JWTManager(app)
mongo = PyMongo(app)

# Collections
users_col = mongo.db.users
history_col = mongo.db.analysis_history

# JWT error handlers
@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid token error: {error}")
    return jsonify({'error': 'Invalid token', 'message': str(error)}), 422

@jwt.unauthorized_loader
def unauthorized_callback(error):
    print(f"Unauthorized error: {error}")
    return jsonify({'error': 'Missing Authorization Header', 'message': str(error)}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print("Expired token")
    return jsonify({'error': 'Token has expired'}), 401

# -------------------
# Authentication Routes
# -------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        if users_col.find_one({'username': username}):
            return jsonify({'error': 'Username already exists'}), 400

        if users_col.find_one({'email': email}):
            return jsonify({'error': 'Email already exists'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }

        res = users_col.insert_one(new_user)
        user_id = str(res.inserted_id)
        access_token = create_access_token(identity=user_id)

        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 201
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400

        user = users_col.find_one({'username': username})
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=str(user['_id']))

        return jsonify({
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'username': user['username'],
                'email': user['email']
            }
        }), 200
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        user_id = get_jwt_identity()
        user = users_col.find_one({'_id': ObjectId(user_id)}, {'password': 0})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user['id'] = str(user.pop('_id'))
        return jsonify({'user': user}), 200
    except Exception as e:
        print(f"Verify error: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------
# Analysis Routes
# -------------------
@app.route('/api/analyze/review', methods=['POST'])
@jwt_required()
def analyze_review():
    try:
        data = request.get_json() or {}
        review_text = data.get('review_text')
        movie_name = data.get('movie_name', '')

        if not review_text:
            return jsonify({'error': 'Review text is required'}), 400

        # sentiment_analyzer should return a dict with at least 'sentiment' and 'confidence'
        from sentiment_analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text(review_text)

        # Save history
        user_id = get_jwt_identity()
        history_doc = {
            'user_id': ObjectId(user_id),
            'movie_name': movie_name,
            'review_text': review_text,
            'sentiment': result.get('sentiment'),
            'confidence': result.get('confidence'),
            'timestamp': datetime.utcnow()
        }
        history_col.insert_one(history_doc)

        return jsonify(result), 200
    except Exception as e:
        print(f"analyze_review error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze/movie', methods=['POST'])
@jwt_required()
def analyze_movie():
    try:
        data = request.get_json() or {}
        movie_name = data.get('movie_name')
        if not movie_name:
            return jsonify({'error': 'Movie name is required'}), 400

        from movie_scraper import MovieScraper
        scraper = MovieScraper()
        result = scraper.get_movie_sentiment(movie_name)

        return jsonify(result), 200
    except Exception as e:
        print(f"analyze_movie error: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------
# Movies / History / Dataset Routes
# -------------------
@app.route('/api/movies/famous', methods=['GET'])
def get_famous_movies():
    try:
        from movie_data import get_famous_movies_data
        movies = get_famous_movies_data()
        return jsonify(movies), 200
    except Exception as e:
        print(f"get_famous_movies error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        docs = history_col.find({'user_id': ObjectId(user_id)}).sort('timestamp', -1).limit(50)
        results = []
        for d in docs:
            results.append({
                'id': str(d.get('_id')),
                'movie_name': d.get('movie_name'),
                'review_text': d.get('review_text'),
                'sentiment': d.get('sentiment'),
                'confidence': d.get('confidence'),
                'timestamp': d.get('timestamp').isoformat() if d.get('timestamp') else None
            })
        return jsonify(results), 200
    except Exception as e:
        print(f"get_history error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/stats', methods=['GET'])
def get_dataset_stats():
    try:
        from movie_data import get_dataset_statistics
        stats = get_dataset_statistics()
        return jsonify(stats), 200
    except Exception as e:
        print(f"get_dataset_stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/reviews', methods=['GET'])
def get_dataset_reviews():
    try:
        from movie_data import get_random_reviews
        count = request.args.get('count', 10, type=int)
        reviews = get_random_reviews(count=count)
        return jsonify(reviews), 200
    except Exception as e:
        print(f"get_dataset_reviews error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/reviews/sentiment/<sentiment_type>', methods=['GET'])
def get_reviews_by_sentiment_type(sentiment_type):
    try:
        from movie_data import get_reviews_by_sentiment
        limit = request.args.get('limit', 10, type=int)
        reviews = get_reviews_by_sentiment(sentiment_type=sentiment_type, limit=limit)
        return jsonify({'sentiment': sentiment_type, 'reviews': reviews}), 200
    except Exception as e:
        print(f"get_reviews_by_sentiment_type error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/analyze-sample', methods=['GET'])
def analyze_sample():
    try:
        from movie_data import analyze_dataset_sample
        sample_size = request.args.get('sample_size', 50, type=int)
        results = analyze_dataset_sample(sample_size=sample_size)
        return jsonify(results), 200
    except Exception as e:
        print(f"analyze_sample error: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------
# Utility / Test endpoints
# -------------------
@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        # ping MongoDB
        mongo.db.command('ping')
        return jsonify({'status': 'Connected to MongoDB ✅'}), 200
    except Exception as e:
        print(f"test_db error: {e}")
        return jsonify({'error': str(e)}), 500

# -------------------
# Run
# -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
