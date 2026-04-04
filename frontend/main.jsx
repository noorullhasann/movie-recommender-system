import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

function MovieSearchDropdown({ value, onChange, onSelect }) {
  const [searchResults, setSearchResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (value.length < 2) {
      setSearchResults([]);
      return;
    }

    const searchMovies = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/search?q=${encodeURIComponent(value)}&limit=8`
        );
        const data = await res.json();
        setSearchResults(data);
        setIsOpen(true);
      } catch (err) {
        console.error("Search error:", err);
      }
    };

    const timer = setTimeout(searchMovies, 300);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div className="search-dropdown">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsOpen(true)}
        placeholder="Search for a movie..."
        className="search-input"
      />
      {isOpen && searchResults.length > 0 && (
        <div className="dropdown-menu">
          {searchResults.map((movie, idx) => (
            <div
              key={idx}
              className="dropdown-item"
              onClick={() => {
                onSelect(movie.title);
                setIsOpen(false);
                setSearchResults([]);
              }}
            >
              {movie.poster_url && (
                <img
                  src={movie.poster_url}
                  alt={movie.title}
                  className="dropdown-poster"
                />
              )}
              <div className="dropdown-info">
                <div className="dropdown-title">{movie.title}</div>
                {movie.release_date && (
                  <div className="dropdown-year">
                    {new Date(movie.release_date).getFullYear()}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function App() {
  const [userId, setUserId] = useState("");
  const [movieTitle, setMovieTitle] = useState("");
  const [rating, setRating] = useState(3);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [method, setMethod] = useState("hybrid");
  const [userRatings, setUserRatings] = useState([]);
  const [allMovies, setAllMovies] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState("recommend");

  const API_BASE = import.meta.env.VITE_API_URL 
    ? `${import.meta.env.VITE_API_URL}/api`
    : "http://127.0.0.1:5000/api";

  // Fetch stats and movies on load
  useEffect(() => {
    fetchStats();
    fetchMovies();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/stats`);
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    }
  };

  const fetchMovies = async () => {
    try {
      const res = await fetch(`${API_BASE}/movies`);
      const data = await res.json();
      setAllMovies(data);
    } catch (err) {
      console.error("Failed to fetch movies:", err);
    }
  };

  const getRecommendations = async () => {
    setError("");
    setLoading(true);

    try {
      let url = `${API_BASE}/recommend?method=${method}`;

      if (method === "collaborative" || method === "hybrid") {
        if (!userId) {
          setError("Please enter a User ID for this method");
          setLoading(false);
          return;
        }
        url += `&user_id=${userId}`;
      } else if (method === "content") {
        if (!movieTitle) {
          setError("Please enter a movie title for content-based recommendations");
          setLoading(false);
          return;
        }
        url += `&movie=${encodeURIComponent(movieTitle)}`;
      }

      const res = await fetch(url);
      const data = await res.json();

      if (data.error) {
        setError(data.error);
        setRecommendations([]);
      } else {
        setRecommendations(data.recommendations || []);
      }
    } catch (err) {
      setError("Failed to fetch recommendations: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const rateMovie = async (e) => {
    e.preventDefault();
    setError("");

    if (!userId || !movieTitle || rating === null) {
      setError("Please fill in all rating fields");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/rate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: parseInt(userId),
          title: movieTitle,
          rating: parseFloat(rating),
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Rating saved successfully!");
        setMovieTitle("");
        setRating(3);
        fetchUserRatings();
        fetchMovies();
      } else {
        setError(data.error || "Failed to save rating");
      }
    } catch (err) {
      setError("Error saving rating: " + err.message);
    }
  };

  const fetchUserRatings = async () => {
    if (!userId) {
      setError("Please enter a User ID first");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/user/${userId}/ratings`);
      const data = await res.json();
      setUserRatings(data);
      setActiveTab("ratings");
    } catch (err) {
      setError("Failed to fetch user ratings: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🎬 Movie Recommender System</h1>
        <p className="subtitle">
          Powered by Collaborative Filtering & Cosine Similarity
        </p>
      </header>

      {stats && (
        <div className="stats-bar">
          <div className="stat">
            <span className="stat-value">{stats.total_users}</span>
            <span className="stat-label">Users</span>
          </div>
          <div className="stat">
            <span className="stat-value">{stats.total_movies}</span>
            <span className="stat-label">Movies</span>
          </div>
          <div className="stat">
            <span className="stat-value">{stats.total_ratings}</span>
            <span className="stat-label">Ratings</span>
          </div>
          <div className="stat">
            <span className="stat-value">{stats.avg_rating.toFixed(2)}</span>
            <span className="stat-label">Avg Rating</span>
          </div>
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === "recommend" ? "active" : ""}`}
          onClick={() => setActiveTab("recommend")}
        >
          Get Recommendations
        </button>
        <button
          className={`tab-button ${activeTab === "rate" ? "active" : ""}`}
          onClick={() => setActiveTab("rate")}
        >
          Rate a Movie
        </button>
        <button
          className={`tab-button ${activeTab === "ratings" ? "active" : ""}`}
          onClick={() => setActiveTab("ratings")}
        >
          My Ratings
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {activeTab === "recommend" && (
        <div className="section">
          <h2>Get Movie Recommendations</h2>

          <div className="input-group">
            <label>User ID:</label>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter your user ID"
            />
          </div>

          <div className="input-group">
            <label>Recommendation Method:</label>
            <select value={method} onChange={(e) => setMethod(e.target.value)}>
              <option value="hybrid">Hybrid (Collaborative + Content-Based)</option>
              <option value="collaborative">Collaborative Filtering</option>
              <option value="content">Content-Based</option>
            </select>
          </div>

          {method === "content" && (
            <div className="input-group">
              <label>Movie Title:</label>
              <MovieSearchDropdown
                value={movieTitle}
                onChange={setMovieTitle}
                onSelect={setMovieTitle}
              />
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={getRecommendations}
            disabled={loading}
          >
            {loading ? "Loading..." : "Get Recommendations"}
          </button>

          {recommendations.length > 0 && (
            <div className="recommendations">
              <h3>Recommended Movies:</h3>
              <div className="movie-grid">
                {recommendations.map((rec, i) => (
                  <div key={i} className="movie-card">
                    {rec.poster_url && (
                      <div className="movie-poster-container">
                        <img
                          src={rec.poster_url}
                          alt={rec.title}
                          className="movie-poster"
                        />
                      </div>
                    )}
                    <div className="movie-card-content">
                      <h4>{rec.title}</h4>
                      {rec.overview && (
                        <p className="movie-overview">{rec.overview.substring(0, 100)}...</p>
                      )}
                      <div className="score">
                        {rec.predicted_rating && (
                          <p>Rating: {rec.predicted_rating.toFixed(2)}/5</p>
                        )}
                        {rec.similarity_score && (
                          <p>Similarity: {(rec.similarity_score * 100).toFixed(1)}%</p>
                        )}
                        {rec.score && <p>Score: {rec.score.toFixed(2)}</p>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === "rate" && (
        <div className="section">
          <h2>Rate a Movie</h2>

          <form onSubmit={rateMovie} className="form">
            <div className="input-group">
              <label>User ID:</label>
              <input
                type="number"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="Enter your user ID"
              />
            </div>

            <div className="input-group">
              <label>Movie Title:</label>
              <MovieSearchDropdown
                value={movieTitle}
                onChange={setMovieTitle}
                onSelect={setMovieTitle}
              />
            </div>

            <div className="input-group">
              <label>Rating: {rating}/5</label>
              <input
                type="range"
                min="0"
                max="5"
                step="0.5"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
                className="slider"
              />
              <div className="rating-labels">
                <span>0</span>
                <span>2.5</span>
                <span>5</span>
              </div>
            </div>

            <button type="submit" className="btn btn-primary">
              Save Rating
            </button>
          </form>
        </div>
      )}

      {activeTab === "ratings" && (
        <div className="section">
          <h2>Your Ratings</h2>

          <div className="input-group">
            <label>User ID:</label>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter your user ID"
            />
            <button
              className="btn btn-secondary"
              onClick={fetchUserRatings}
              disabled={loading}
            >
              Load Ratings
            </button>
          </div>

          {userRatings.length > 0 && (
            <div className="ratings-table">
              <h3>Your Movie Ratings ({userRatings.length})</h3>
              <table>
                <thead>
                  <tr>
                    <th>Movie Title</th>
                    <th>Your Rating</th>
                  </tr>
                </thead>
                <tbody>
                  {userRatings.map((rating, i) => (
                    <tr key={i}>
                      <td>{rating.title}</td>
                      <td>
                        <span className="rating-badge">
                          {rating.rating}/5
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <footer className="footer">
        <p>
          Built with Collaborative Filtering, Content-Based Filtering & Cosine
          Similarity
        </p>
      </footer>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
