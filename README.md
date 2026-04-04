# 🎬 Movie Recommender System - Full Stack ML Application

**Production-Ready | MovieLens 100K | TMDB Posters | Docker | Render & Vercel Deployment**

A complete movie recommendation engine using **Collaborative Filtering** and **Cosine Similarity** algorithms with both backend (Flask + scikit-learn) and frontend (React + Vite).

## 🎉 Latest Improvements (2024)

✅ **100K+ Movies** - Integrated MovieLens 100K dataset  
✅ **Movie Posters** - TMDB API integration for beautiful images  
✅ **Smart Search** - Real-time autocomplete dropdown  
✅ **Docker Ready** - Complete containerization support  
✅ **Deploy Anywhere** - Render (backend) + Vercel (frontend) configs  
✅ **Production Features** - Gunicorn, health checks, monitoring  

[See IMPROVEMENTS_SUMMARY.md for details](IMPROVEMENTS_SUMMARY.md)

## Features

### 🤖 Machine Learning Algorithms

1. **Collaborative Filtering**
   - User-user similarity using cosine similarity
   - Finds recommendations based on what similar users liked
   - Great for discovering new movies

2. **Content-Based Filtering**
   - Item-item similarity using cosine similarity
   - Finds movies similar to ones you already like
   - Consistent with user preferences

3. **Hybrid Approach**
   - Combines both collaborative and content-based methods
   - Provides more balanced and diverse recommendations

### ✨ Features

- Multi-method recommendation system (Hybrid, Collaborative, Content-Based)
- **100K+ Movies** (MovieLens dataset support)
- **Movie Posters** (TMDB API integration)
- Smart search with autocomplete dropdown
- Real-time statistics dashboard
- User rating system with persistent storage
- Beautiful, responsive UI with gradient design
- RESTful API backend
- Docker containerization
- Production-ready deployment configs

### 🎨 UI/UX Enhancements

- Beautiful gradient interface
- Movie poster images
- Smart autocomplete search
- Real-time recommendations
- Responsive design (mobile-friendly)
- Loading indicators
- Error handling
- Statistics dashboard

## Project Structure

```
movie_recommender_fullstack/
├── backend/
│   ├── app.py              # Flask API with ML models
│   ├── movies.csv          # Movie ratings dataset
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── main.jsx            # React app component
    ├── styles.css          # Styling
    ├── index.html          # HTML entry point
    ├── package.json        # Node.js dependencies
    ├── vite.config.js      # Vite configuration
    └── node_modules/       # Installed packages
```

## Installation

### Backend Setup

```bash
cd backend
python3 -m pip install -r requirements.txt
```

Dependencies:
- Flask 3.0.0
- Flask-CORS 4.0.0
- pandas 2.1.3
- scikit-learn 1.3.2
- numpy 1.24.3
- requests 2.31.0 (for TMDB)
- gunicorn 21.2.0 (for production)

### Frontend Setup

```bash
cd frontend
npm install
```

## 📊 Optional: Enhanced Features

### MovieLens 100K Dataset (Recommended)

Default demo uses 2 movies. Switch to 100K real movies for better recommendations:

```bash
cd backend
python3 load_movielens.py  # Downloads 5MB dataset
# App auto-detects and uses it!
```

### TMDB Movie Posters

Add free movie poster images. Get API key: https://www.themoviedb.org/settings/api

```bash
# Create backend/.env
echo "TMDB_API_KEY=your_key_here" > backend/.env

# Restart backend - posters now display!
```

## Running the Application

### Start the Backend

```bash
cd backend
python3 app.py
```

The Flask server will run on `http://127.0.0.1:5000`

### Start the Frontend

In a new terminal:

```bash
cd frontend
npm start
```

The Vite dev server will open on `http://localhost:3000`

### Or Use Docker Compose (Recommended)

```bash
docker-compose up
```

Everything starts with one command! Backend on 5000, frontend on 3000.

## 🚀 Deployment

### Quick Deploy to Render + Vercel

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy Backend to Render**
   - Go to https://render.com → New Blueprint
   - Connect repo → Deploy
   - Render reads `render.yaml` automatically

3. **Deploy Frontend to Vercel**
   - Go to https://vercel.com → New Project
   - Connect repo → Deploy
   - Set `VITE_API_URL` environment variable

[See DEPLOYMENT_GUIDE.md for detailed instructions](DEPLOYMENT_GUIDE.md)

## API Endpoints

### Get All Movies
```
GET /api/movies
```
Returns list of all movies with average ratings and rating counts.

### Get Recommendations
```
GET /api/recommend?method=hybrid&user_id=1
```

Methods:
- `hybrid` - Combines collaborative filtering and content-based
- `collaborative` - User-based collaborative filtering
- `content` - Content-based similar movies (requires `&movie=title`)

### Rate a Movie
```
POST /api/rate
Content-Type: application/json

{
  "user_id": 1,
  "title": "Toy Story (1995)",
  "rating": 5
}
```

### Get User Ratings
```
GET /api/user/1/ratings
```
Returns all movies rated by the specified user.

### System Statistics
```
GET /api/stats
```
Returns: total users, total movies, total ratings, average rating

## How It Works

### Collaborative Filtering Algorithm

1. **Build User-Item Matrix**: Create a matrix where rows are users, columns are movies, and values are ratings
2. **Calculate User Similarity**: Use cosine similarity to find users with similar taste
3. **Find Recommendations**: Get movies highly rated by similar users

```
Similarity = cos(θ) = (A · B) / (||A|| ||B||)
```

### Content-Based Filtering

1. **Build Item-Item Matrix**: Create similarity matrix of items (movies)
2. **Calculate Cosine Similarity**: Measure how similar movies are based on user ratings
3. **Recommend**: Suggest movies similar to ones the user already liked

### Hybrid Approach

Combines both methods:
- Uses collaborative filtering as primary
- Falls back to popular movies if user is new
- Balances discovery (collaborative) with consistency (content-based)

## Example Usage

### Getting Recommendations for User 1

**Frontend UI:**
1. Enter User ID: `1`
2. Select Method: `Hybrid`
3. Click "Get Recommendations"

**API Call:**
```bash
curl "http://127.0.0.1:5000/api/recommend?method=hybrid&user_id=1"
```

**Response:**
```json
{
  "method": "hybrid",
  "user_id": 1,
  "recommendations": [
    {
      "title": "Forrest Gump (1994)",
      "score": 4.5
    },
    {
      "title": "The Shawshank Redemption (1994)",
      "score": 4.3
    },
    ...
  ]
}
```

### Rating a Movie

**Frontend UI:**
1. Go to "Rate a Movie" tab
2. Enter User ID: `1`
3. Enter Movie: `Toy Story (1995)`
4. Set Rating: `5`
5. Click "Save Rating"

**API Call:**
```bash
curl -X POST "http://127.0.0.1:5000/api/rate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Toy Story (1995)",
    "rating": 5
  }'
```

## Data Format

### movies.csv
```
userId,title,rating
1,Toy Story (1995),5
1,Jumanji (1995),3
2,Toy Story (1995),4
2,Jumanji (1995),5
...
```

## Machine Learning Details

### Cosine Similarity
Measures the cosine of the angle between vectors in a multi-dimensional space.

For movies rated by users:
- Value of 1: identical movies/users
- Value of 0: no similarity
- Value of -1: opposite movies/users

### User-Based Collaborative Filtering
```
prediction(user_a, movie_x) = mean_rating(user_a) + 
  Σ(similarity(user_a, user_b) * (rating(user_b, movie_x) - mean_rating(user_b)))
  / Σ(similarity(user_a, user_b))
```

### Item-Based Collaborative Filtering
```
prediction(user, movie_a) = 
  Σ(similarity(movie_a, movie_b) * rating(user, movie_b))
  / Σ(similarity(movie_a, movie_b))
```

## Performance Considerations

- **Time Complexity**: O(n²) for similarity calculations (n = number of items/users)
- **Space Complexity**: O(n²) for storing similarity matrices
- Optimized for datasets up to thousands of movies
- Real-time recommendations with fast computation

## Improvements & Extensions

1. **Matrix Factorization** (SVD, NMF)
2. **Deep Learning Models** (Neural Collaborative Filtering)
3. **Temporal Dynamics** (older ratings weighted less)
4. **Implicit Feedback** (clicks, views, time spent)
5. **Cold Start Solutions** (new users/items)
6. **A/B Testing Framework**
7. **Recommendation Diversity** (reduce redundancy)
8. **Explanation Generation** (why items are recommended)

## Troubleshooting

### Port Already in Use
- Backend (5000): `lsof -i :5000` and `kill -9 <PID>`
- Frontend (3000): `lsof -i :3000` and `kill -9 <PID>`

### CORS Issues
- Flask-CORS is enabled in backend
- Ensure frontend is accessing correct API URLs

### CSV Not Found
- Make sure `movies.csv` is in the `backend/` folder
- Check file encoding (should be UTF-8)

### Dependencies Issues
- Use `python3 -m pip install --upgrade -r requirements.txt`
- Clear npm cache: `npm cache clean --force`

## Technologies Used

### Backend
- **Framework**: Flask 3.0.0
- **ML Library**: scikit-learn 1.3.2
- **Data Processing**: pandas 2.1.3
- **Numerical Computing**: numpy 1.24.3
- **CORS**: Flask-CORS 4.0.0

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.0
- **Styling**: CSS3 (modern gradient, flexbox, grid)
- **Server**: Vite Dev Server

## License

MIT License

## Author

Built with ❤️ for movie lovers and machine learning enthusiasts
