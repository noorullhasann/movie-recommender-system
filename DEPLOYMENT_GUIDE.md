# 🚀 Deployment Guide

Complete instructions for deploying the Movie Recommender System to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Environment Variables](#environment-variables)
5. [Using MovieLens Dataset](#using-movielens-dataset)
6. [TMDB API Setup](#tmdb-api-setup)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Accounts Needed
- [Render](https://render.com/) - For backend (free tier available)
- [Vercel](https://vercel.com/) - For frontend (free tier available)
- [The Movie Database (TMDB)](https://www.themoviedb.org/) - For movie posters (optional)
- GitHub account (recommended for CI/CD)

### Local Setup
```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

---

## Backend Deployment (Render)

### Option 1: Via render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/movie-recommender.git
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository
   - Click "Deploy"
   - Render will automatically read `render.yaml` and deploy both services

3. **Set Environment Variables**
   - Go to backend service settings
   - Add `TMDB_API_KEY` if you want poster images
   - Render will rebuild automatically

### Option 2: Manual Web Service Deployment

1. **Create a new Web Service**
   - Go to [render.com](https://render.com/)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Select the repository

2. **Configure the Service**
   ```
   Name: movie-recommender-backend
   Root Directory: backend/ (or leave blank if at root)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
   Plan: Free (or Pro for better performance)
   ```

3. **Add Environment Variables**
   - In dashboard: Environment section
   - Add key-value pairs:
     - `TMDB_API_KEY`: Your TMDB API key (optional)
     - `FLASK_ENV`: production
     - `PYTHONUNBUFFERED`: 1

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the service URL (e.g., `https://movie-recommender-backend.onrender.com`)

### Monitoring Backend

```bash
# Check logs
# In Render dashboard: Logs tab

# Check health endpoint
curl https://movie-recommender-backend.onrender.com/api/stats

# Test API
curl https://movie-recommender-backend.onrender.com/api/movies?limit=5
```

---

## Frontend Deployment (Vercel)

### Option 1: Via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Follow Prompts**
   - Link to GitHub project
   - Set project name
   - Confirm settings
   - Deployment starts automatically

### Option 2: Via GitHub (Recommended for Teams)

1. **Push to GitHub** (if not already done)
   ```bash
   git push origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com/)
   - Click "Add New..." → "Project"
   - Select GitHub repository
   - Click "Import"

3. **Configure Project**
   ```
   Framework Preset: Vite
   Root Directory: ./frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **Add Environment Variables**
   - In project settings: Environment Variables
   - Add:
     - `VITE_API_URL`: `https://movie-recommender-backend.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Visit your Vercel domain

### Option 3: Deploy to Custom Domain

1. **Purchase Domain** (or use existing)
   - Namecheap, GoDaddy, etc.

2. **Add Domain in Vercel**
   - Project settings → Domains
   - Add your domain
   - Follow instructions for DNS configuration

3. **Update Backend URL**
   - If using custom domain, update `VITE_API_URL` environment variable

---

## Environment Variables

### Backend (.env or Render Environment)

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000

# TMDB API (optional, for movie posters)
TMDB_API_KEY=your_tmdb_api_key_here

# CORS Configuration
CORS_ORIGINS=https://your-vercel-domain.vercel.app

# Data
DATA_FILE=movies.csv
# USE DATA_FILE=movielens_100k.csv if using MovieLens
```

### Frontend (.env or Vercel Environment)

```env
VITE_API_URL=https://movie-recommender-backend.onrender.com
```

---

## Using MovieLens Dataset

### Option 1: Download Locally and Commit

1. **Download and Process**
   ```bash
   cd backend
   python3 -c "from load_movielens import load_movielens; load_movielens()"
   ```

2. **Commit to Git**
   ```bash
   git add movielens_100k.csv
   git commit -m "Add MovieLens 100k dataset"
   git push
   ```

3. **On Render**
   - File will be included in deployment
   - App automatically uses it if present

### Option 2: Download During Deployment (Not Recommended)

Add to Render Build Command:
```bash
pip install -r requirements.txt && python3 load_movielens.py
```

⚠️ **Warning**: This adds 5-10 minutes to build time

### Option 3: Use in Development Only

Keep small `movies.csv` for production, use MovieLens locally:

```bash
# Local development
python3 load_movielens.py
# Edit backend/app.py to prefer movielens_100k.csv

# Git (don't commit large file)
echo "movielens_100k.csv" >> .gitignore
```

---

## TMDB API Setup

### Get Free API Key

1. **Create Account**
   - Visit [themoviedb.org](https://www.themoviedb.org/)
   - Sign up (free)

2. **Generate API Key**
   - Account Settings → API
   - Click "Create" under API Key
   - Accept terms and create
   - Copy API key (not auth token)

3. **Add to Environment**

   **Local Development:**
   ```bash
   # In backend/.env
   TMDB_API_KEY=your_api_key_here
   ```

   **Render:**
   - Dashboard → Environment Variables
   - Add `TMDB_API_KEY` with your key
   - Deploy

   **Vercel:**
   - Project Settings → Environment Variables
   - Add `VITE_API_URL` pointing to Render backend

### Testing TMDB Integration

```bash
# Test API key
curl "http://127.0.0.1:5000/api/movies?limit=1"
# Should return movies with poster_url if API key is valid
```

---

## Deployment Checklist

### Before Deploying

- [ ] Push code to GitHub
- [ ] Update `TMDB_API_KEY` in environment variables
- [ ] Test locally: `npm start` (frontend) + `python3 app.py` (backend)
- [ ] Check `vercel.json` and `render.yaml` are correct
- [ ] Update `VITE_API_URL` in Vercel to Render backend URL
- [ ] Add CORS origins to backend (Vercel domain)

### After Deploying

- [ ] Visit Vercel deployment URL
- [ ] Test getting recommendations
- [ ] Check movie posters display
- [ ] Test search functionality
- [ ] Monitor logs for errors
- [ ] Test with real user IDs

### Performance Optimization

**Backend (Render)**
- Free plan: ~0.5 seconds cold start
- Paid plan: No cold starts, faster response
- Recommendation: Use Pro for production

**Frontend (Vercel)**
- Edge caching for static assets
- Automatic image optimization
- Cold start: <100ms typically

---

## Updating Deployed Sites

### Push Updates

1. **Make Changes Locally**
   ```bash
   git add .
   git commit -m "Update: your changes"
   ```

2. **Push to GitHub**
   ```bash
   git push origin main
   ```

3. **Auto-Deploy**
   - Render watches main branch, auto-deploys
   - Vercel watches main branch, auto-deploys
   - No manual action needed!

### Manual Redeploy

**Render:**
- Dashboard → Click service
- Click "Manual Deploy" → "Latest Commit"

**Vercel:**
- Project → Deployments
- Click "..." on latest → "Redeploy"

---

## Troubleshooting Deployment

### Backend Won't Start

**Check Logs:**
```bash
# Render Dashboard → Logs tab
# Look for Python errors
```

**Common Issues:**

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure all packages in `requirements.txt` |
| `Port already in use` | Render assigns port via `$PORT` variable |
| `Data file not found` | Ensure `movies.csv` committed to Git |
| `TMDB_API_KEY invalid` | Check API key in environment variables |

### Frontend Won't Build

**Check Logs:**
```bash
# Vercel Dashboard → Deployments → Logs
```

**Common Issues:**

| Error | Solution |
|-------|----------|
| `VITE_API_URL undefined` | Add to Environment Variables |
| `Cannot find module` | Run `npm install` locally first |
| `Build fails` | Check `package.json` build script |
| `API calls 404` | Ensure backend URL in VITE_API_URL is correct |

### API Issues

**CORS Error:**
```javascript
// Browser console: "Access to XMLHttpRequest blocked by CORS"
// Solution: Update CORS_ORIGINS in backend environment
```

**Posters Not Showing:**
```
// Solution: Add TMDB_API_KEY to backend environment
// Or API rate limit exceeded, wait 30 seconds
```

**Search Not Working:**
```
// Solution: Check network tab, ensure API URL is correct
// API might be sleeping (Render free plan), visit site to wake up
```

---

## Performance Tips

### Render (Backend)
- Free tier: ~1 second response first request (cold start)
- Pro tier: Consistent <200ms response
- Use background jobs for heavy processing
- Cache responses when possible

### Vercel (Frontend)
- Static files: Cached globally
- Images: Optimized automatically
- <100ms cold start typical
- Monitor response times in Analytics

### Overall
- Reduce bundle size: Tree-shake unused code
- Optimize images: Vercel does this auto
- CDN caching: Both services include
- Database: Consider adding for persistence

---

## Monitoring & Logs

### Render
- Dashboard → Logs tab (real-time)
- Set up alerts for errors
- Export logs for analysis

### Vercel
- Analytics tab: Response times, edge metrics
- Edge function logs: Real-time
- Performance Insights: Core Web Vitals

---

## Scaling & Upgrades

### When to Upgrade Render
- Free tier hits request limit
- Response times >2 seconds
- Need persistent storage
- Production traffic requirements

**Upgrade Path:**
Free → Starter ($7/mo) → Standard ($25/mo) → Custom

### When to Upgrade Vercel
- Free tier usage exceeded
- Need Pro features (team collaboration)
- Self-hosting required

**Upgrade Path:**
Hobby (free) → Pro ($20/mo) → Enterprise (custom)

---

## Cost Estimates (Monthly)

| Service | Free Tier | Recommended | Enterprise |
|---------|-----------|-------------|-----------|
| Render | Free* | $7 | Custom |
| Vercel | Free | $20 | Custom |
| TMDB API | Free | Free† | Custom |
| **Total** | **$0** | **$27** | **Custom** |

*Render free tier: 750 hours/month
†TMDB free tier: 40 requests/second

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. Set up domain (optional)
4. Add monitoring/logging
5. Set up CI/CD pipeline
6. Consider database for persistence
7. Add authentication
8. Scale as needed

---

**Deployment complete! Your app is live! 🎉**
