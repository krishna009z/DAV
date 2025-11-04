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
import requests
from dotenv import load_dotenv
from textblob import TextBlob  # ✅ Added for movie plot sentiment

load_dotenv()

app = Flask(__name__)

# Basic Config
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# MongoDB Connection
app.config["MONGO_URI"] = os.getenv(
    "DATABASE_URL",
    "mongodb+srv://dav:<db_password>@dav.kpmskka.mongodb.net/dav?retryWrites=true&w=majority"
)

CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)
mongo = PyMongo(app)

users_col = mongo.db.users
history_col = mongo.db.analysis_history


# ✅ Sentiment analysis function for movie plot
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "POSITIVE", round(polarity * 100, 1)
    elif polarity < -0.1:
        return "NEGATIVE", round(abs(polarity) * 100, 1)
    else:
        return "NEUTRAL", round(abs(polarity) * 100, 1)


# 🟦 AUTH ROUTES
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        if users_col.find_one({"username": username}):
            return jsonify({"error": "Username already exists"}), 400
        if users_col.find_one({"email": email}):
            return jsonify({"error": "Email already exists"}), 400

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = {
            "username": username,
            "email": email,
            "password": hashed,
            "created_at": datetime.utcnow()
        }
        result = users_col.insert_one(user)
        user_id = str(result.inserted_id)

        token = create_access_token(identity=user_id)

        return jsonify({
            "message": "User created successfully",
            "access_token": token,
            "user": {"id": user_id, "username": username, "email": email}
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        user = users_col.find_one({"username": username})
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user['_id']))

        return jsonify({
            "access_token": token,
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify():
    try:
        user_id = get_jwt_identity()
        user = users_col.find_one({"_id": ObjectId(user_id)}, {"password": 0})

        if not user:
            return jsonify({"error": "User not found"}), 404

        user['id'] = str(user.pop('_id'))
        return jsonify({"user": user}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🟩 ANALYSIS ROUTES
@app.route('/api/analyze/movie', methods=['POST'])
def analyze_movie():
    try:
        data = request.get_json() or {}
        title = data.get("title")
        year = data.get("year", "")

        if not title:
            return jsonify({"error": "Movie title required"}), 400

        omdb_api_key = os.getenv("OMDB_API_KEY")
        omdb_url = f"https://www.omdbapi.com/?t={title}&y={year}&apikey={omdb_api_key}"

        movie_resp = requests.get(omdb_url).json()
        print("OMDB Response ✅", movie_resp)

        if movie_resp.get("Response") != "True":
            return jsonify({"error": "Movie not found in OMDB"}), 404

        plot = movie_resp.get("Plot", "No plot available")
        poster = movie_resp.get("Poster") or None
        imdb_rating = movie_resp.get("imdbRating")

        # ✅ convert to float if valid
        try:
            imdb_rating = float(imdb_rating) if imdb_rating != "N/A" else None
        except:
            imdb_rating = None

        movie_year = movie_resp.get("Year", year)

        # ✅ Sentiment
        sentiment, polarity_percent = analyze_sentiment(plot)
        confidence = round(polarity_percent / 100, 2)

        # ✅ Pie + Bar chart data
        detailed_scores = {
            "positive": round((confidence if sentiment == "POSITIVE" else 0.15), 2),
            "neutral": round((0.7 if sentiment == "NEUTRAL" else 0.2), 2),
            "negative": round((confidence if sentiment == "NEGATIVE" else 0.15), 2)
        }

        # ✅ Normalize to 1.0 exactly
        total = sum(detailed_scores.values())
        for k in detailed_scores:
            detailed_scores[k] = round(detailed_scores[k] / total, 2)

        return jsonify({
            "sentiment": sentiment.lower(),  # ✅ lowercase for UI
            "confidence": confidence,
            "detailed_scores": detailed_scores,
            "sources": {
                "imdb": {
                    "title": title,
                    "year": movie_year,
                    "imdb_rating": imdb_rating,  # ✅ REAL rating / null
                    "plot": plot,
                    "poster": poster
                }
            }
        }), 200

    except Exception as e:
        print("🔥 Server Movie Error:", str(e))
        return jsonify({
            "error": "Movie analysis failed",
            "details": str(e),
            "sources": {
                "imdb": {
                    "title": title,
                    "year": year,
                    "imdb_rating": None,
                    "plot": "Plot unavailable due to API error",
                    "poster": None
                }
            },
            "sentiment": "neutral",
            "confidence": 0.0,
            "detailed_scores": {
                "positive": 0.33,
                "neutral": 0.34,
                "negative": 0.33
            }
        }), 500


@app.route("/api/analyze/review", methods=["POST"])
@jwt_required()
def analyze_review():
    try:
        from sentiment_analyzer import SentimentAnalyzer

        data = request.get_json() or {}
        review_text = data.get("review_text")
        movie_name = data.get("movie_name", "")

        if not review_text:
            return jsonify({"error": "Review text is required"}), 400

        analyzer = SentimentAnalyzer()
        result = analyzer.analyze_text(review_text)

        user_id = get_jwt_identity()
        history_col.insert_one({
            "user_id": ObjectId(user_id),
            "movie_name": movie_name,
            "review_text": review_text,
            "sentiment": result.get("sentiment"),
            "confidence": result.get("confidence"),
            "timestamp": datetime.utcnow()
        })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    docs = history_col.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1)

    return jsonify([
        {
            "id": str(d["_id"]),
            "movie_name": d.get("movie_name"),
            "review_text": d.get("review_text"),
            "sentiment": d.get("sentiment"),
            "confidence": d.get("confidence"),
            "timestamp": d["timestamp"].isoformat()
        } for d in docs
    ]), 200


@app.route("/api/test-db", methods=["GET"])
def test_db():
    try:
        mongo.db.command("ping")
        return {"status": "MongoDB connected ✅"}
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
