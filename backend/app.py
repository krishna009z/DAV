from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///moviereview.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS to allow Authorization header
CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})
jwt = JWTManager(app)
db = SQLAlchemy(app)

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
    print(f"Expired token")
    return jsonify({'error': 'Token has expired'}), 401

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

class AnalysisHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_name = db.Column(db.String(200))
    review_text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'movie_name': self.movie_name,
            'review_text': self.review_text,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
        
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=str(new_user.id))
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        print(f"=== Login Request ===")
        print(f"Username: {username}")
        
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"User not found: {username}")
            return jsonify({'error': 'Invalid credentials'}), 401
            
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            print(f"Invalid password for user: {username}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        print(f"Login successful for user: {username}")
        print(f"=== End Login ===")
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analysis Routes
@app.route('/api/analyze/review', methods=['POST'])
@jwt_required()
def analyze_review():
    try:
        from sentiment_analyzer import SentimentAnalyzer
        
        data = request.get_json()
        review_text = data.get('review_text')
        movie_name = data.get('movie_name', '')
        
        if not review_text:
            return jsonify({'error': 'Review text is required'}), 400
        
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text(review_text)
        
        # Save to history
        user_id = get_jwt_identity()
        history = AnalysisHistory(
            user_id=user_id,
            movie_name=movie_name,
            review_text=review_text,
            sentiment=result['sentiment'],
            confidence=result['confidence']
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze/movie', methods=['POST'])
@jwt_required()
def analyze_movie():
    try:
        from movie_scraper import MovieScraper
        
        data = request.get_json()
        movie_name = data.get('movie_name')
        
        print(f"=== Movie Search Request ===")
        print(f"Movie name: {movie_name}")
        
        if not movie_name:
            return jsonify({'error': 'Movie name is required'}), 400
        
        scraper = MovieScraper()
        result = scraper.get_movie_sentiment(movie_name)
        
        print(f"Result: {result}")
        print(f"=== End Request ===")
        
        return jsonify(result), 200
    except Exception as e:
        print(f"ERROR in analyze_movie: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/famous', methods=['GET'])
def get_famous_movies():
    try:
        from movie_data import get_famous_movies_data
        
        movies = get_famous_movies_data()
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        user_id = get_jwt_identity()
        history = AnalysisHistory.query.filter_by(user_id=user_id).order_by(AnalysisHistory.timestamp.desc()).limit(50).all()
        
        return jsonify([h.to_dict() for h in history]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dataset Routes
@app.route('/api/dataset/stats', methods=['GET'])
def get_dataset_stats():
    try:
        from movie_data import get_dataset_statistics
        
        stats = get_dataset_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/reviews', methods=['GET'])
def get_dataset_reviews():
    try:
        from movie_data import get_random_reviews
        
        count = request.args.get('count', 10, type=int)
        reviews = get_random_reviews(count=count)
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/reviews/sentiment/<sentiment_type>', methods=['GET'])
def get_reviews_by_sentiment_type(sentiment_type):
    try:
        from movie_data import get_reviews_by_sentiment
        
        limit = request.args.get('limit', 10, type=int)
        reviews = get_reviews_by_sentiment(sentiment_type=sentiment_type, limit=limit)
        return jsonify({'sentiment': sentiment_type, 'reviews': reviews}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dataset/analyze-sample', methods=['GET'])
def analyze_sample():
    try:
        from movie_data import analyze_dataset_sample
        
        sample_size = request.args.get('sample_size', 50, type=int)
        results = analyze_dataset_sample(sample_size=sample_size)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
