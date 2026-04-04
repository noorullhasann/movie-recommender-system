#!/usr/bin/env bash

# Quick Deployment Reference
# Copy these commands to deploy Movie Recommender System

echo "🎬 Movie Recommender - Quick Deployment Commands"
echo "=================================================="
echo ""

# Local Development
echo "📍 LOCAL DEVELOPMENT (Recommended)"
echo "---"
echo "  docker-compose up"
echo ""

# Docker Build
echo "🐳 BUILD DOCKER IMAGES"
echo "---"
echo "  # Backend only"
echo "  docker build -t movie-recommender-backend ."
echo ""
echo "  # Frontend only"
echo "  docker build -t movie-recommender-frontend frontend/"
echo ""

# Push to GitHub
echo "📦 PUSH TO GITHUB (Required for cloud deployment)"
echo "---"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'Initial commit'"
echo "  git remote add origin https://github.com/YOUR_USERNAME/movie-recommender"
echo "  git push -u origin main"
echo ""

# Render Backend
echo "🚀 DEPLOY BACKEND TO RENDER"
echo "---"
echo "  1. Go to https://render.com"
echo "  2. Click 'New +' → 'Blueprint'"
echo "  3. Connect GitHub → Select repo"
echo "  4. Render auto-reads render.yaml and deploys!"
echo "  5. Note the backend URL (e.g., https://movie-recommender-backend.onrender.com)"
echo ""

# Vercel Frontend
echo "🌐 DEPLOY FRONTEND TO VERCEL"
echo "---"
echo "  1. Go to https://vercel.com"
echo "  2. Click 'New Project'"
echo "  3. Select GitHub repo → Import"
echo "  4. Add Environment Variable:"
echo "     • Name: VITE_API_URL"
echo "     • Value: https://movie-recommender-backend.onrender.com"
echo "  5. Click Deploy!"
echo ""

# MovieLens Dataset
echo "📊 LOAD MOVIELENS DATASET (Optional)"
echo "---"
echo "  cd backend"
echo "  python3 load_movielens.py"
echo ""

# TMDB API Key
echo "🎨 ADD TMDB POSTER IMAGES (Optional)"
echo "---"
echo "  1. Get free API key: https://www.themoviedb.org/settings/api"
echo "  2. Local:"
echo "     echo 'TMDB_API_KEY=your_key' > backend/.env"
echo "     python3 app.py"
echo ""
echo "  3. Render:"
echo "     Dashboard → Backend Service → Environment"
echo "     Add: TMDB_API_KEY = your_key"
echo "     Deploy"
echo ""

# Monitoring
echo "📊 MONITOR DEPLOYMENTS"
echo "---"
echo "  Render: https://dashboard.render.com → Select service → Logs"
echo "  Vercel: https://vercel.com → Select project → Deployments"
echo ""

# Testing
echo "✅ TEST DEPLOYMENT"
echo "---"
echo "  Backend Health:"
echo "    curl https://YOUR_RENDER_URL/api/stats"
echo ""
echo "  Frontend:"
echo "    Visit: https://YOUR_VERCEL_URL"
echo ""

# Troubleshooting
echo "🆘 QUICK TROUBLESHOOTING"
echo "---"
echo "  Port 5000 in use?"
echo "    lsof -i :5000"
echo "    kill -9 <PID>"
echo ""
echo "  Port 3000 in use?"
echo "    lsof -i :3000"
echo "    kill -9 <PID>"
echo ""
echo "  Docker issues?"
echo "    docker-compose down"
echo "    docker-compose up"
echo ""

# Full Guides
echo "📚 FULL GUIDES"
echo "---"
echo "  • DEPLOYMENT_GUIDE.md - Complete step-by-step"
echo "  • IMPROVEMENTS_SUMMARY.md - Features overview"
echo "  • README.md - Project overview"
echo ""

echo "=================================================="
echo "✨ Ready to deploy? Follow the commands above!"
echo ""
