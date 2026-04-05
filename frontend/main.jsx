import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

function MovieSearchDropdown({ value, onChange, onSelect }) {
  const [searchResults, setSearchResults] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (value.length < 1) {
      setSearchResults([]);
      return;
    }

    const searchMovies = async () => {
      try {
        const res = await fetch(
          `http://127.0.0.1:5000/api/search?q=${encodeURIComponent(value)}&limit=12`
        );
        const data = await res.json();
        setSearchResults(data);
        setIsOpen(true);
      } catch (err) {
        console.error("Search error:", err);
      }
    };

    const timer = setTimeout(searchMovies, 200);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div className="search-dropdown">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
        placeholder="🔍 Search for a movie..."
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
                {movie.genres && (
                  <div className="dropdown-genres">{movie.genres}</div>
                )}
                {movie.vote_average && (
                  <div className="dropdown-rating">
                    ⭐ {movie.vote_average.toFixed(1)}/10
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

function MovieCard({ movie, showReason = false }) {
  return (
    <div className="movie-card">
      <div className="movie-poster-wrapper">
        {movie.poster_url ? (
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="movie-poster"
            onError={(e) => {
              e.target.style.display = "none";
            }}
          />
        ) : (
          <div className="movie-poster-placeholder">
            <span>🎬</span>
          </div>
        )}
        <div className="movie-overlay">
          {movie.genres && (
            <div className="movie-genres">
              {movie.genres.split(",").map((genre, i) => (
                <span key={i} className="genre-badge">
                  {genre.trim()}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="movie-card-content">
        <h3 className="movie-title">{movie.title}</h3>
        {movie.overview && (
          <p className="movie-overview">{movie.overview.substring(0, 85)}...</p>
        )}
        <div className="movie-footer">
          <div className="movie-rating">
            {movie.vote_average && (
              <span className="rating-stars">
                ⭐ {movie.vote_average.toFixed(1)}
              </span>
            )}
            {movie.predicted_rating && (
              <span className="rating-stars">
                📊 {movie.predicted_rating.toFixed(2)}
              </span>
            )}
            {movie.similarity_score && (
              <span className="rating-stars">
                🎯 {(movie.similarity_score * 100).toFixed(0)}%
              </span>
            )}
            {movie.score && (
              <span className="rating-stars">📈 {movie.score.toFixed(1)}</span>
            )}
          </div>
          {showReason && movie.reason && (
            <div className="movie-reason">💡 {movie.reason}</div>
          )}
        </div>
      </div>
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
  const [selectedGenre, setSelectedGenre] = useState("");
  const [genres, setGenres] = useState([]);
  const [userRatings, setUserRatings] = useState([]);
  const [allMovies, setAllMovies] = useState([]);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState("recommend");
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const API_BASE = import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : "http://127.0.0.1:5000/api";

  // Fetch stats, movies, and genres on load
  useEffect(() => {
    fetchStats();
    fetchMovies();
    fetchGenres();
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
      const res = await fetch(`${API_BASE}/movies?limit=200`);
      const data = await res.json();
      setAllMovies(data);
    } catch (err) {
      console.error("Failed to fetch movies:", err);
    }
  };

  const fetchGenres = async () => {
    try {
      const res = await fetch(`${API_BASE}/genres`);
      const data = await res.json();
      setGenres(data);
    } catch (err) {
      console.error("Failed to fetch genres:", err);
    }
  };

  const getRecommendations = async () => {
    setError("");
    setLoading(true);

    try {
      // Primary method: Genre-based (no user_id needed)
      if (selectedGenre) {
        const res = await fetch(
          `${API_BASE}/recommend?method=genre&genre=${encodeURIComponent(selectedGenre)}`
        );
        const data = await res.json();
        
        if (data.error) {
          setError(data.error);
          setRecommendations([]);
        } else {
          setRecommendations(data.recommendations || []);
        }
      } else if (movieTitle) {
        // Content-based: similar movies
        const res = await fetch(
          `${API_BASE}/recommend?method=content&movie=${encodeURIComponent(movieTitle)}`
        );
        const data = await res.json();
        
        if (data.error) {
          setError(data.error);
          setRecommendations([]);
        } else {
          setRecommendations(data.recommendations || []);
        }
      } else {
        // Default: show popular movies
        const res = await fetch(`${API_BASE}/recommend?method=popular`);
        const data = await res.json();
        
        if (data.error) {
          setError(data.error);
          setRecommendations([]);
        } else {
          setRecommendations(data.recommendations || []);
        }
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
      setError("Please fill in all fields");
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
        setShowSuccessMessage(true);
        setTimeout(() => setShowSuccessMessage(false), 3000);
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
      setError("Please enter a User ID");
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
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <div className="header-title">
            <h1 className="main-title">🎬 CineMatch</h1>
            <p className="tagline">Your Personal Movie Genius</p>
          </div>
          <p className="subtitle">
            Discover movies you'll love • Powered by advanced ML algorithms
          </p>
        </div>
      </header>

      {stats && (
        <div className="stats-container">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">👥</div>
              <div className="stat-value">{stats.total_users}+</div>
              <div className="stat-label">Active Users</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">🎞️</div>
              <div className="stat-value">{stats.total_movies}+</div>
              <div className="stat-label">Movies</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">⭐</div>
              <div className="stat-value">{stats.avg_rating.toFixed(1)}</div>
              <div className="stat-label">Avg Rating</div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">🎭</div>
              <div className="stat-value">{stats.total_genres || 19}</div>
              <div className="stat-label">Genres</div>
            </div>
          </div>
        </div>
      )}

      <div className="container">
        <div className="tabs-container">
          <button
            className={`tab-button ${activeTab === "recommend" ? "active" : ""}`}
            onClick={() => setActiveTab("recommend")}
          >
            <span className="tab-icon">🎯</span> Discover
          </button>
          <button
            className={`tab-button ${activeTab === "genre" ? "active" : ""}`}
            onClick={() => setActiveTab("genre")}
          >
            <span className="tab-icon">🎭</span> By Genre
          </button>
          <button
            className={`tab-button ${activeTab === "rate" ? "active" : ""}`}
            onClick={() => setActiveTab("rate")}
          >
            <span className="tab-icon">⭐</span> Rate
          </button>
          <button
            className={`tab-button ${activeTab === "myratings" ? "active" : ""}`}
            onClick={() => setActiveTab("myratings")}
          >
            <span className="tab-icon">📋</span> My Ratings
          </button>
        </div>

        {error && <div className="error-alert">{error}</div>}
        {showSuccessMessage && (
          <div className="success-alert">✅ Rating saved successfully!</div>
        )}

        {/* DISCOVER TAB */}
        {activeTab === "recommend" && (
          <div className="content-section">
            <div className="section-header">
              <h2>🎯 Discover Movies For You</h2>
              <p>Browse by genre, search by movie, or discover popular hits</p>
            </div>

            <div className="card form-card">
              <div className="form-grid">
                <div className="form-group">
                  <label htmlFor="genre">📽️ Pick a Genre</label>
                  <select
                    id="genre"
                    value={selectedGenre}
                    onChange={(e) => setSelectedGenre(e.target.value)}
                    className="form-input"
                  >
                    <option value="">✨ All Recommendations</option>
                    {genres.map((genre) => (
                      <option key={genre} value={genre}>
                        {genre}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="orMovie">Or Search a Movie</label>
                  <MovieSearchDropdown
                    value={movieTitle}
                    onChange={setMovieTitle}
                    onSelect={setMovieTitle}
                  />
                </div>
              </div>

              <button
                className="btn btn-primary btn-large"
                onClick={getRecommendations}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span> Finding Perfect Matches...
                  </>
                ) : (
                  <>🔍 Get Recommendations</>
                )}
              </button>
            </div>

            {recommendations.length > 0 && (
              <div className="recommendations-section">
                <h3 className="recommendations-title">
                  ✨ Movies We Think You'll Love
                </h3>
                <div className="movie-grid">
                  {recommendations.map((rec, i) => (
                    <MovieCard key={i} movie={rec} showReason={true} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* GENRE TAB - Quick Genre Browsing */}
        {activeTab === "genre" && (
          <div className="content-section">
            <div className="section-header">
              <h2>🎭 Browse by Genre</h2>
              <p>Quick access to your favorite movie categories</p>
            </div>

            <div className="card form-card">
              <div className="genre-grid">
                {genres.map((genre) => (
                  <button
                    key={genre}
                    className="genre-button"
                    onClick={async () => {
                      setSelectedGenre(genre);
                      setError("");
                      setLoading(true);
                      try {
                        const res = await fetch(
                          `${API_BASE}/recommend?method=genre&genre=${encodeURIComponent(genre)}`
                        );
                        const data = await res.json();
                        if (data.error) {
                          setError(data.error);
                        } else {
                          setRecommendations(data.recommendations || []);
                        }
                      } catch (err) {
                        setError("Failed to fetch: " + err.message);
                      } finally {
                        setLoading(false);
                      }
                    }}
                  >
                    {genre}
                  </button>
                ))}
              </div>
            </div>

            {recommendations.length > 0 && (
              <div className="recommendations-section">
                <h3 className="recommendations-title">
                  🎬 {selectedGenre} Movies
                </h3>
                <div className="movie-grid">
                  {recommendations.map((rec, i) => (
                    <MovieCard key={i} movie={rec} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* RATE TAB */}
        {activeTab === "rate" && (
          <div className="content-section">
            <div className="section-header">
              <h2>⭐ Rate Movies</h2>
              <p>Help us learn what you love by rating movies</p>
            </div>

            <div className="card form-card">
              <form onSubmit={rateMovie}>
                <div className="form-group">
                  <label htmlFor="rateUserId">Your User ID</label>
                  <input
                    id="rateUserId"
                    type="number"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    placeholder="Enter your ID"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="rateMovieTitle">Movie Title</label>
                  <MovieSearchDropdown
                    value={movieTitle}
                    onChange={setMovieTitle}
                    onSelect={setMovieTitle}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="ratingSlider">
                    Your Rating: <span className="rating-value">{rating}/5</span>
                  </label>
                  <input
                    id="ratingSlider"
                    type="range"
                    min="0"
                    max="5"
                    step="0.5"
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                    className="rating-slider"
                  />
                  <div className="rating-scale">
                    <span>😞 Hate</span>
                    <span>😐 OK</span>
                    <span>😍 Love</span>
                  </div>
                </div>

                <button type="submit" className="btn btn-primary btn-large">
                  💾 Save My Rating
                </button>
              </form>
            </div>
          </div>
        )}

        {/* MY RATINGS TAB */}
        {activeTab === "myratings" && (
          <div className="content-section">
            <div className="section-header">
              <h2>📋 My Ratings</h2>
              <p>View all the movies you've rated</p>
            </div>

            <div className="card form-card">
              <div className="form-group">
                <label htmlFor="viewUserId">Your User ID</label>
                <input
                  id="viewUserId"
                  type="number"
                  value={userId}
                  onChange={(e) => setUserId(e.target.value)}
                  placeholder="Enter your user ID"
                  className="form-input"
                />
              </div>
              <button
                className="btn btn-primary btn-large"
                onClick={fetchUserRatings}
                disabled={loading || !userId}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span> Loading...
                  </>
                ) : (
                  <>📚 Load My Ratings</>
                )}
              </button>
            </div>

            {userRatings.length > 0 && (
              <div className="ratings-section">
                <h3>You've rated {userRatings.length} movies</h3>
                <div className="ratings-grid">
                  {userRatings.map((r, i) => (
                    <div key={i} className="rating-item">
                      <div className="rating-title">{r.title}</div>
                      <div className="rating-badge">
                        {"⭐".repeat(Math.round(r.rating))}
                      </div>
                      <div className="rating-score">{r.rating}/5</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {userRatings.length === 0 && userId && !loading && (
              <div className="empty-state">
                <p>No ratings found for user {userId}</p>
                <p className="hint">Start rating movies to get better recommendations!</p>
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="footer">
        <p>
          🚀 Built with React • ML-Powered Recommendations • Your taste, Our algorithm
        </p>
      </footer>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
