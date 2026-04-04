from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import os
from functools import lru_cache
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# TMDB API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w342"
MOVIE_CACHE = {}  # Cache for movie metadata

# Load and prepare data
ratings_df = None
user_item_matrix = None
user_similarity_df = None
item_similarity_df = None
movie_ratings = None

def load_dataset():
    """Load dataset - prefer MovieLens 100k if available, else use movies.csv"""
    global ratings_df, user_item_matrix, user_similarity_df, item_similarity_df, movie_ratings
    
    # Try MovieLens first
    if os.path.exists("movielens_100k.csv"):
        print("📊 Loading MovieLens 100K dataset...")
        ratings_df = pd.read_csv("movielens_100k.csv")
    else:
        print("📊 Loading default movies.csv dataset...")
        ratings_df = pd.read_csv("movies.csv")
    
    print(f"✅ Loaded {len(ratings_df)} ratings")
    
    # Create user-item interaction matrix for collaborative filtering
    user_item_matrix = ratings_df.pivot_table(
        index='userId', 
        columns='title', 
        values='rating'
    ).fillna(0)
    
    # Calculate user-user similarity (collaborative filtering)
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity, 
        index=user_item_matrix.index, 
        columns=user_item_matrix.index
    )
    
    # Calculate item-item similarity (content-based filtering)
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_similarity_df = pd.DataFrame(
        item_similarity, 
        index=user_item_matrix.columns, 
        columns=user_item_matrix.columns
    )
    
    # Get average ratings for movies
    movie_ratings = ratings_df.groupby('title')['rating'].agg(['mean', 'count']).reset_index()
    movie_ratings.columns = ['title', 'avg_rating', 'num_ratings']

# Initialize on startup
load_dataset()

def get_collaborative_recommendations(user_id, n_recommendations=5):
    """Recommend based on similar users' preferences"""
    if user_id not in user_similarity_df.index:
        return []
    
    # Get similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:6].index.tolist()
    
    if not similar_users:
        return []
    
    # Get movies rated by similar users but not by current user
    user_rated = set(user_item_matrix.columns[user_item_matrix.loc[user_id] > 0])
    recommendations = {}
    
    for sim_user in similar_users:
        sim_user_ratings = user_item_matrix.loc[sim_user]
        for movie, rating in sim_user_ratings[sim_user_ratings > 0].items():
            if movie not in user_rated:
                if movie not in recommendations:
                    recommendations[movie] = []
                recommendations[movie].append(rating)
    
    # Average the scores
    rec_scores = {movie: np.mean(scores) for movie, scores in recommendations.items()}
    return sorted(rec_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]

@lru_cache(maxsize=1000)
def search_tmdb_movie(movie_title):
    """Search for movie on TMDB API"""
    if not TMDB_API_KEY:
        return None
    
    try:
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'type': 'movie'
        }
        response = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params, timeout=5)
        results = response.json().get('results', [])
        
        if results:
            movie = results[0]
            return {
                'tmdb_id': movie.get('id'),
                'title': movie.get('title'),
                'poster_path': movie.get('poster_path'),
                'overview': movie.get('overview'),
                'release_date': movie.get('release_date'),
                'vote_average': movie.get('vote_average')
            }
    except Exception as e:
        print(f"TMDB API error: {e}")
    
    return None

def get_movie_metadata(movie_title):
    """Get movie metadata with poster image"""
    if movie_title in MOVIE_CACHE:
        return MOVIE_CACHE[movie_title]
    
    # Try to get from TMDB
    metadata = search_tmdb_movie(movie_title)
    
    if metadata and metadata.get('poster_path'):
        metadata['poster_url'] = f"{TMDB_IMAGE_URL}{metadata['poster_path']}"
    
    # Cache the result (even if None)
    MOVIE_CACHE[movie_title] = metadata
    return metadata

def get_content_based_recommendations(movie_name, n_recommendations=5):
    """Recommend similar movies based on user ratings"""
    if movie_name not in item_similarity_df.columns:
        return []
    
    similar_movies = item_similarity_df[movie_name].sort_values(ascending=False)[1:n_recommendations+1]
    return [(movie, score) for movie, score in similar_movies.items()]

def get_hybrid_recommendations(user_id, n_recommendations=5):
    """Combine collaborative and content-based filtering"""
    collab_recs = get_collaborative_recommendations(user_id, n_recommendations)
    
    if not collab_recs:
        # Fallback to popular movies
        popular = movie_ratings.nlargest(n_recommendations, 'avg_rating')
        return [(row['title'], row['avg_rating']) for _, row in popular.iterrows()]
    
    return collab_recs

@app.route("/api/movies", methods=["GET"])
def get_movies():
    """Get all available movies with ratings (optionally search)"""
    search = request.args.get("search", "").lower()
    
    movies_list = movie_ratings.sort_values('avg_rating', ascending=False).to_dict('records')
    
    # Filter by search term
    if search:
        movies_list = [m for m in movies_list if search in m['title'].lower()]
    
    # Add TMDB metadata
    for movie in movies_list:
        metadata = get_movie_metadata(movie['title'])
        if metadata:
            movie['tmdb_id'] = metadata.get('tmdb_id')
            movie['poster_url'] = metadata.get('poster_url')
            movie['overview'] = metadata.get('overview')
            movie['release_date'] = metadata.get('release_date')
            movie['vote_average'] = metadata.get('vote_average')
    
    # Limit results for performance
    limit = request.args.get("limit", default=100, type=int)
    return jsonify(movies_list[:limit])

@app.route("/api/recommend", methods=["GET"])
def recommend():
    """Get recommendations for a user using collaborative filtering"""
    user_id = request.args.get("user_id", type=int)
    method = request.args.get("method", "hybrid")  # hybrid, collaborative, content
    movie_name = request.args.get("movie", None)
    
    try:
        if method == "content" and movie_name:
            # Content-based: find similar movies
            recs = get_content_based_recommendations(movie_name, 5)
            result_recs = []
            for r in recs:
                rec_item = {"title": r[0], "similarity_score": float(r[1])}
                metadata = get_movie_metadata(r[0])
                if metadata:
                    rec_item['poster_url'] = metadata.get('poster_url')
                    rec_item['overview'] = metadata.get('overview')
                result_recs.append(rec_item)
            
            return jsonify({
                "method": "content-based",
                "based_on": movie_name,
                "recommendations": result_recs
            })
        
        elif method == "collaborative" and user_id:
            # Collaborative: find movies similar users liked
            recs = get_collaborative_recommendations(user_id, 5)
            result_recs = []
            for r in recs:
                rec_item = {"title": r[0], "predicted_rating": float(r[1])}
                metadata = get_movie_metadata(r[0])
                if metadata:
                    rec_item['poster_url'] = metadata.get('poster_url')
                    rec_item['overview'] = metadata.get('overview')
                result_recs.append(rec_item)
            
            return jsonify({
                "method": "collaborative",
                "user_id": user_id,
                "recommendations": result_recs
            })
        
        elif method == "hybrid" and user_id:
            # Hybrid: combine both approaches
            recs = get_hybrid_recommendations(user_id, 5)
            result_recs = []
            for r in recs:
                rec_item = {"title": r[0], "score": float(r[1])}
                metadata = get_movie_metadata(r[0])
                if metadata:
                    rec_item['poster_url'] = metadata.get('poster_url')
                    rec_item['overview'] = metadata.get('overview')
                result_recs.append(rec_item)
            
            return jsonify({
                "method": "hybrid",
                "user_id": user_id,
                "recommendations": result_recs
            })
        
        else:
            return jsonify({"error": "Invalid parameters"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/search", methods=["GET"])
def search_movies():
    """Search for movies with autocomplete"""
    query = request.args.get("q", "").lower()
    limit = request.args.get("limit", default=10, type=int)
    
    if not query or len(query) < 2:
        return jsonify([])
    
    # Search in available movies
    matches = [m for m in movie_ratings['title'].unique() 
               if query in m.lower()]
    
    # Return with metadata
    results = []
    for movie in matches[:limit]:
        result_item = {"title": movie}
        metadata = get_movie_metadata(movie)
        if metadata:
            result_item['poster_url'] = metadata.get('poster_url')
            result_item['release_date'] = metadata.get('release_date')
        results.append(result_item)
    
    return jsonify(results)

@app.route("/api/rate", methods=["POST"])
def rate_movie():
    """Add or update a movie rating for a user"""
    try:
        data = request.json
        user_id = data.get("user_id")
        title = data.get("title")
        rating = data.get("rating")
        
        if not all([user_id, title, rating]):
            return jsonify({"error": "Missing required fields"}), 400
        
        if rating < 0 or rating > 5:
            return jsonify({"error": "Rating must be between 0 and 5"}), 400
        
        # Add to DataFrame
        new_rating = pd.DataFrame({
            'userId': [user_id],
            'title': [title],
            'rating': [rating]
        })
        
        global ratings_df, user_item_matrix
        ratings_df = pd.concat([ratings_df, new_rating], ignore_index=True)
        
        # Rebuild matrix
        user_item_matrix = ratings_df.pivot_table(
            index='userId',
            columns='title',
            values='rating'
        ).fillna(0)
        
        return jsonify({"success": True, "message": "Rating saved"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/user/<int:user_id>/ratings", methods=["GET"])
def get_user_ratings(user_id):
    """Get all ratings from a specific user"""
    user_movies = ratings_df[ratings_df['userId'] == user_id]
    if user_movies.empty:
        return jsonify([])
    
    return jsonify(user_movies.to_dict('records'))

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get system statistics"""
    return jsonify({
        "total_users": int(ratings_df['userId'].nunique()),
        "total_movies": int(ratings_df['title'].nunique()),
        "total_ratings": int(len(ratings_df)),
        "avg_rating": float(ratings_df['rating'].mean())
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
