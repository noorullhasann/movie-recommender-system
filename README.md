# 🎬 CineMatch - Movie Recommender System

A modern, AI-powered movie recommendation engine with multiple filtering strategies.

## 📦 Quick Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Server runs on `http://127.0.0.1:5000`

### Frontend
```bash
cd frontend
npm install
npm start
```
App runs on `http://localhost:5173`

---

## 🎯 Features

✅ **Genre-Based Recommendations** - Filter by 17+ genres (Action, Drama, Comedy, etc.)  
✅ **Content-Based Filtering** - Find similar movies based on a selection  
✅ **Collaborative Filtering** - Get recommendations based on user ratings (optional)  
✅ **Popular Movies** - Discover top-rated films  
✅ **Movie Search** - Autocomplete search with poster images  
✅ **User Ratings** - Rate movies and build personal preference profile  
✅ **Smart UI** - Genre buttons, movie cards, beautiful gradients  

---

## 🗂️ Project Structure

```
movie-recommender-system/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── create_movies.py       # Dataset creation script
│   ├── enhanced_movies.csv    # Movie database (70 films)
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # API keys (local only)
│   └── .env.example           # Template
├── frontend/
│   ├── main.jsx              # React app (main component)
│   ├── styles.css            # Styling
│   ├── index.html            # HTML entry point
│   ├── vite.config.js        # Bundler config
│   ├── package.json          # Dependencies
│   └── Dockerfile            # Container config
├── docker-compose.yml        # Docker orchestration
├── Dockerfile                # Main container
├── vercel.json              # Vercel deployment config
├── render.yaml              # Render deployment config
└── DATASET_UPDATE.md        # Dataset info
```

---

## 🚀 API Endpoints

### Get Recommendations
```bash
# By Genre
GET /api/recommend?method=genre&genre=Action
→ Returns 20 Action movies

# Similar to Movie
GET /api/recommend?method=content&movie=Avatar
→ Returns 20 movies similar to Avatar

# Popular Movies (default)
GET /api/recommend
→ Returns 25 top-rated movies

# User-Based (with ID)
GET /api/recommend?user_id=5&method=collaborative
→ Returns 20 personalized recommendations
```

### Search & Browse
```bash
GET /api/genres
→ Returns all available genres

GET /api/movies
→ Returns all movies with ratings

GET /api/search?q=avatar
→ Search movies by title

GET /api/stats
→ System statistics
```

### User Actions
```bash
POST /api/rate
→ Save movie rating for a user

GET /api/user/{user_id}/ratings
→ Get user's rated movies
```

---

## 💾 Dataset

**File**: `backend/enhanced_movies.csv`  
**Movies**: 70 hand-curated films  

**Genres**: Action, Adventure, Biography, Comedy, Crime, Drama, Family, Fantasy, Film-Noir, History, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War

### Add More Movies
Edit `create_movies.py` and add movies to `movies_data` list:
```python
movies_data = [
    {'title': 'Your Movie', 'genres': 'Action, Drama', 'vote_average': 8.5, ...},
]
```

Then regenerate:
```bash
python create_movies.py
```

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask, Pandas, Scikit-learn, NumPy |
| Frontend | React 18, Vite, CSS Grid |
| Data | CSV, Pandas DataFrames |
| Algorithms | Cosine Similarity, Collaborative Filtering |
| Deployment | Docker, Vercel, Render |

---

## 📊 Recommendation Algorithms

### 1. Genre-Based
- Filters movies by selected genre
- Ranks by rating (70%) + popularity (30%)
- **Returns**: 20 top-rated movies in genre

### 2. Content-Based
- Computes similarity using cosine distance
- Based on rating vectors across users
- **Returns**: 20 most similar movies

### 3. Collaborative Filtering
- Finds similar users based on ratings
- Recommends movies liked by similar users
- **Returns**: 20 personalized recommendations

### 4. Popular
- Sorts movies by average rating
- **Returns**: 25 top-rated movies

---

## 🐳 Docker Deployment

### Run Locally
```bash
docker-compose up
```

### Build Custom Image
```bash
docker build -t movie-recommender .
docker run -p 5000:5000 -p 3000:3000 movie-recommender
```

---

## 📋 Dependencies

### Backend (Python)
```
Flask==3.0.0
flask-cors==4.0.0
pandas==2.1.1
numpy==1.24.3
scikit-learn==1.3.0
python-dotenv==1.0.0
requests==2.31.0
```

### Frontend (Node)
```
React 18.2.0
Vite 5.0.0
```

---

## 🔐 Environment Setup

### `.env` Template
```
TMDB_API_KEY=your_key_here
FLASK_ENV=development
```

---

## ✨ Usage Examples

### 1. Discover by Genre
1. Open app → "By Genre" tab
2. Click a genre button
3. See 20 top-rated movies in that genre

### 2. Find Similar Movies
1. Go to "Discover" tab
2. Search and select a movie
3. See 20 similar movies

### 3. Get Popular Recommendations
1. Click "Get Recommendations" with no filters
2. See 25 highest-rated movies

### 4. Rate Movies & Get Personalized
1. Enter user ID
2. Go to "Rate" tab
3. Rate movies you've watched
4. Get collaborative recommendations

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No genres in dropdown | Restart backend, check `enhanced_movies.csv` |
| API connection error | Check backend running on port 5000 |
| Movies not loading | Ensure `enhanced_movies.csv` in `/backend/` |

---

## 📝 Recent Optimizations

✅ Removed backup files and old datasets  
✅ Cleaned up unused documentation  
✅ Removed redundant scripts  
✅ Optimized project structure  
✅ Increased recommendations: 10 → 20-25 movies  
✅ Added 70 curated movies with proper genres  

---

**Happy Watching! 🍿🎬**
