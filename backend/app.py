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
@app.route("/api/analyze/movie", methods=["POST"])
def analyze_movie():
    try:
        data = request.get_json() or {}
        title = data.get("title") or data.get("movie_name")

        if not title:
            return jsonify({"error": "Title is required"}), 400

        omdb_key = os.getenv("OMDB_API_KEY")
        if not omdb_key:
            return jsonify({"error": "OMDB API key missing"}), 500

        url = "https://www.omdbapi.com/"
        params = {"apikey": omdb_key, "t": title}

        response = requests.get(url, params=params)
        movie = response.json()

        if movie.get("Response") == "False":
            return jsonify({"error": "Movie not found"}), 404

        return jsonify({
            "success": True,
            "movie": {
                "title": movie.get("Title"),
                "overview": movie.get("Plot", ""),
                "release_date": movie.get("Released", "Unknown"),
                "rating": movie.get("imdbRating", "N/A")
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
