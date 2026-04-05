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
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_CACHE = {}  # Cache for movie metadata

# Load and prepare data
ratings_df = None
movies_df = None
user_item_matrix = None
user_similarity_df = None
item_similarity_df = None
movie_ratings = None
genre_map = {}

# Genre ID to Name mapping (TMDB)
GENRE_IDS = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Sci-Fi",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

def load_dataset():
    """Load dataset - prefer enhanced_movies if available, then MovieLens 100k, else movies.csv"""
    global ratings_df, movies_df, user_item_matrix, user_similarity_df, item_similarity_df, movie_ratings, genre_map
    
    # Try enhanced movies first
    if os.path.exists("enhanced_movies.csv"):
        print("📊 Loading enhanced movies dataset with genres...")
        movies_df = pd.read_csv("enhanced_movies.csv")
    elif os.path.exists("movielens_100k.csv"):
        print("📊 Loading MovieLens 100K dataset...")
        ratings_df = pd.read_csv("movielens_100k.csv")
    else:
        print("📊 Loading default movies.csv dataset...")
        ratings_df = pd.read_csv("movies.csv")
    
    # If we loaded enhanced movies, use it for both movies and create ratings
    if movies_df is not None:
        print(f"✅ Loaded {len(movies_df)} movies with genres")
        # Create a synthetic ratings dataframe for collaborative filtering
        # Use vote_average as ratings
        ratings_data = []
        for idx, row in movies_df.head(500).iterrows():  # Use top 500 for collaborative
            for user_id in range(1, min(101, int(row['popularity'] / 10) + 1)):
                ratings_data.append({
                    'userId': user_id,
                    'title': row['title'],
                    'rating': min(5, max(1, row['vote_average']))
                })
        
        ratings_df = pd.DataFrame(ratings_data)
    
    print(f"✅ Loaded {len(ratings_df)} ratings")
    
    # Create user-item interaction matrix for collaborative filtering
    user_item_matrix = ratings_df.pivot_table(
        index='userId', 
        columns='title', 
        values='rating'
    ).fillna(0)
    
    # Calculate user-user similarity (collaborative filtering)
    if len(user_item_matrix) > 1:
        user_similarity = cosine_similarity(user_item_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity, 
            index=user_item_matrix.index, 
            columns=user_item_matrix.index
        )
    
    # Calculate item-item similarity (content-based filtering)
    if len(user_item_matrix.columns) > 1:
        item_similarity = cosine_similarity(user_item_matrix.T)
        item_similarity_df = pd.DataFrame(
            item_similarity, 
            index=user_item_matrix.columns, 
            columns=user_item_matrix.columns
        )
    
    # Get average ratings for movies
    movie_ratings = ratings_df.groupby('title')['rating'].agg(['mean', 'count']).reset_index()
    movie_ratings.columns = ['title', 'avg_rating', 'num_ratings']
    
    # Add genres if available
    if movies_df is not None:
        # Only merge columns that exist in movies_df
        columns_to_merge = ['title']
        if 'genres' in movies_df.columns:
            columns_to_merge.append('genres')
        if 'overview' in movies_df.columns:
            columns_to_merge.append('overview')
        if 'vote_average' in movies_df.columns:
            columns_to_merge.append('vote_average')
        if 'release_date' in movies_df.columns:
            columns_to_merge.append('release_date')
        
        movie_ratings = movie_ratings.merge(
            movies_df[columns_to_merge], 
            on='title', 
            how='left'
        )

# Initialize on startup
load_dataset()

def get_collaborative_recommendations(user_id, n_recommendations=20):
    """Recommend based on similar users' preferences"""
    if user_item_matrix is None or len(user_item_matrix) < 2:
        return []
    
    if user_id not in user_similarity_df.index:
        return []
    
    # Get similar users
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:11].index.tolist()
    
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

def parse_genres(genre_str):
    """Parse genre string to list"""
    if pd.isna(genre_str):
        return []
    return [g.strip() for g in str(genre_str).split(',')]

def get_genre_recommendations(genre, n_recommendations=20):
    """Get recommendations for a specific genre"""
    if movies_df is None or 'genres' not in movies_df.columns:
        return []
    
    # Filter movies by genre
    genre_movies = movies_df[
        movies_df['genres'].str.contains(genre, case=False, na=False)
    ].copy()
    
    # Sort by rating and popularity
    genre_movies['score'] = (genre_movies['vote_average'] * 0.7 + 
                             genre_movies['popularity'] * 0.3)
    genre_movies = genre_movies.nlargest(n_recommendations, 'score')
    
    return [(row['title'], row['vote_average'], row['genres']) 
            for _, row in genre_movies.iterrows()]

def get_user_preferred_genres(user_id):
    """Get user's preferred genres based on rated movies"""
    user_movies = ratings_df[ratings_df['userId'] == user_id]
    if user_movies.empty or movies_df is None:
        return []
    
    # Find genres of highly rated movies
    high_rated = user_movies[user_movies['rating'] >= 4]['title'].tolist()
    
    genre_scores = {}
    for movie_title in high_rated:
        movie_genres = movies_df[movies_df['title'] == movie_title]['genres'].values
        if len(movie_genres) > 0:
            genres = parse_genres(movie_genres[0])
            for genre in genres:
                genre_scores[genre] = genre_scores.get(genre, 0) + 1
    
    return sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)

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
            genres = [GENRE_IDS.get(gid, '') for gid in movie.get('genre_ids', [])]
            return {
                'tmdb_id': movie.get('id'),
                'title': movie.get('title'),
                'poster_path': movie.get('poster_path'),
                'overview': movie.get('overview'),
                'release_date': movie.get('release_date'),
                'vote_average': movie.get('vote_average'),
                'genres': ', '.join([g for g in genres if g])
            }
    except Exception as e:
        print(f"TMDB API error: {e}")
    
    return None

def get_movie_metadata(movie_title):
    """Get movie metadata with poster image"""
    if movie_title in MOVIE_CACHE:
        return MOVIE_CACHE[movie_title]
    
    metadata = None
    
    # Try to get from movies_df first
    if movies_df is not None:
        movie_row = movies_df[movies_df['title'] == movie_title]
        if not movie_row.empty:
            movie_row = movie_row.iloc[0]
            metadata = {
                'title': movie_row['title'],
                'overview': movie_row.get('overview', ''),
                'poster_url': f"{TMDB_IMAGE_URL}{movie_row['poster_path']}" if movie_row.get('poster_path') else None,
                'vote_average': movie_row.get('vote_average', 0),
                'genres': movie_row.get('genres', ''),
                'release_date': movie_row.get('release_date', '')
            }
    
    # Fallback to TMDB API
    if metadata is None:
        metadata = search_tmdb_movie(movie_title)
    
    # Cache the result (even if None)
    MOVIE_CACHE[movie_title] = metadata
    return metadata

def get_content_based_recommendations(movie_name, n_recommendations=20):
    """Recommend similar movies based on ratings"""
    if item_similarity_df is None or movie_name not in item_similarity_df.columns:
        return []
    
    similar_movies = item_similarity_df[movie_name].sort_values(ascending=False)[1:n_recommendations+1]
    return [(movie, score) for movie, score in similar_movies.items()]

def get_hybrid_recommendations(user_id, n_recommendations=10):
    """Combine collaborative and content-based + genre preferences"""
    collab_recs = get_collaborative_recommendations(user_id, n_recommendations)
    
    if collab_recs:
        return collab_recs
    
    # Fallback to popular movies in user's preferred genres
    preferred_genres = get_user_preferred_genres(user_id)
    
    if preferred_genres:
        # Get movies from preferred genres
        genre = preferred_genres[0][0]
        genre_recs = get_genre_recommendations(genre, n_recommendations)
        return [(title, rating) for title, rating, _ in genre_recs]
    
    # Ultimate fallback to popular movies
    popular = movie_ratings.nlargest(n_recommendations, 'avg_rating')
    return [(row['title'], row['avg_rating']) for _, row in popular.iterrows()]

# ==================== API ENDPOINTS ====================

@app.route("/api/movies", methods=["GET"])
def get_movies():
    """Get all available movies with ratings (optionally search)"""
    search = request.args.get("search", "").lower()
    genre = request.args.get("genre", "")
    
    movies_list = movie_ratings.sort_values('avg_rating', ascending=False)
    
    # Filter by search term
    if search:
        movies_list = movies_list[movies_list['title'].str.lower().str.contains(search, na=False)]
    
    # Filter by genre
    if genre:
        movies_list = movies_list[movies_list['genres'].str.contains(genre, case=False, na=False)]
    
    result = []
    for _, row in movies_list.iterrows():
        movie_item = row.to_dict()
        metadata = get_movie_metadata(row['title'])
        if metadata:
            movie_item.update(metadata)
        result.append(movie_item)
    
    # Limit results for performance
    limit = request.args.get("limit", default=100, type=int)
    return jsonify(result[:limit])

@app.route("/api/genres", methods=["GET"])
def get_genres():
    """Get all unique genres from dataset"""
    if movies_df is None or 'genres' not in movies_df.columns:
        return jsonify([])
    
    all_genres = set()
    for genres_str in movies_df['genres'].dropna():
        genres = parse_genres(genres_str)
        all_genres.update(genres)
    
    return jsonify(sorted(list(all_genres)))

@app.route("/api/recommend", methods=["GET"])
def recommend():
    """Get recommendations - works with or without user_id. Genre & content-based primary."""
    user_id = request.args.get("user_id", type=int)
    method = request.args.get("method", "popular")  # popular, genre, content, collaborative
    movie_name = request.args.get("movie", None)
    genre = request.args.get("genre", None)
    
    try:
        if method == "content" and movie_name:
            # Content-based: find similar movies
            recs = get_content_based_recommendations(movie_name, 20)
            result_recs = []
            for r in recs:
                rec_item = {
                    "title": r[0], 
                    "similarity_score": float(r[1]),
                    "reason": f"Similar to {movie_name}"
                }
                metadata = get_movie_metadata(r[0])
                if metadata:
                    rec_item.update(metadata)
                result_recs.append(rec_item)
            
            return jsonify({
                "method": "content-based",
                "based_on": movie_name,
                "recommendations": result_recs
            })
        
        elif method == "genre" or genre:
            # Genre-based recommendations (primary method - no user_id needed)
            target_genre = genre
            if not target_genre and method == "popular":
                # Recommendation without user_id: show all popular movies
                return recommend_popular()
            
            if target_genre:
                recs = get_genre_recommendations(target_genre, 20)
                result_recs = []
                for title, rating, genres in recs:
                    rec_item = {
                        "title": title,
                        "predicted_rating": float(rating),
                        "genres": genres,
                        "reason": f"Popular {target_genre} movie"
                    }
                    metadata = get_movie_metadata(title)
                    if metadata:
                        rec_item.update(metadata)
                    result_recs.append(rec_item)
                
                return jsonify({
                    "method": "genre",
                    "genre": target_genre,
                    "recommendations": result_recs
                })
        
        elif method == "collaborative" and user_id:
            # Collaborative: find movies similar users liked (optional user_id)
            recs = get_collaborative_recommendations(user_id, 20)
            if recs:
                result_recs = []
                for r in recs:
                    rec_item = {
                        "title": r[0], 
                        "predicted_rating": float(r[1]),
                        "reason": "Users like you loved this"
                    }
                    metadata = get_movie_metadata(r[0])
                    if metadata:
                        rec_item.update(metadata)
                    result_recs.append(rec_item)
                
                return jsonify({
                    "method": "collaborative",
                    "user_id": user_id,
                    "recommendations": result_recs
                })
            else:
                # Fallback to popular if no collaborative data
                return recommend_popular()
        
        else:
            # Default: show popular movies
            return recommend_popular()
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def recommend_popular():
    """Recommend popular movies (no user_id needed)"""
    popular = movie_ratings.nlargest(25, 'avg_rating')
    result_recs = []
    for _, row in popular.iterrows():
        rec_item = {
            "title": row['title'],
            "score": float(row['avg_rating']),
            "reason": "Highly rated movie"
        }
        metadata = get_movie_metadata(row['title'])
        if metadata:
            rec_item.update(metadata)
        result_recs.append(rec_item)
    
    return jsonify({
        "method": "popular",
        "recommendations": result_recs
    })

@app.route("/api/search", methods=["GET"])
def search_movies():
    """Search for movies with autocomplete"""
    query = request.args.get("q", "").lower()
    limit = request.args.get("limit", default=10, type=int)
    
    if not query or len(query) < 1:
        return jsonify([])
    
    # Search in available movies
    if movies_df is not None:
        matches = movies_df[movies_df['title'].str.lower().str.contains(query, na=False)]
        results = []
        for _, movie in matches.head(limit).iterrows():
            result_item = {
                "title": movie['title'],
                "genres": movie.get('genres', ''),
                "vote_average": movie.get('vote_average', 0)
            }
            if movie.get('poster_path'):
                result_item['poster_url'] = f"{TMDB_IMAGE_URL}{movie['poster_path']}"
            if movie.get('release_date'):
                result_item['release_date'] = movie['release_date']
            results.append(result_item)
    else:
        matches = [m for m in movie_ratings['title'].unique() 
                   if query in m.lower()]
        results = [{"title": m} for m in matches[:limit]]
    
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

@app.route("/api/user/<int:user_id>/preferred-genres", methods=["GET"])
def get_user_preferred_genres_api(user_id):
    """Get user's preferred genres"""
    preferred = get_user_preferred_genres(user_id)
    return jsonify([{"genre": g[0], "count": g[1]} for g in preferred[:5]])

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get system statistics"""
    total_genres = 0
    if movies_df is not None:
        all_genres = set()
        for genres_str in movies_df['genres'].dropna():
            genres = parse_genres(genres_str)
            all_genres.update(genres)
        total_genres = len(all_genres)
    
    return jsonify({
        "total_users": int(ratings_df['userId'].nunique()),
        "total_movies": int(ratings_df['title'].nunique()),
        "total_ratings": int(len(ratings_df)),
        "avg_rating": float(ratings_df['rating'].mean()),
        "total_genres": total_genres
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
