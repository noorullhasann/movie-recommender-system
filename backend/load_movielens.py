"""
MovieLens Dataset Loader
Downloads and processes the MovieLens 100K dataset
"""

import os
import pandas as pd
import numpy as np
from urllib.request import urlopen
import zipfile
import io
import ssl

def download_movielens_100k():
    """Download MovieLens 100K dataset"""
    url = "http://files.grouplens.org/datasets/movielens/ml-100k.zip"
    
    print("📥 Downloading MovieLens 100K dataset (5MB)...")
    try:
        # Bypass SSL certificate verification (for development only)
        ssl_context = ssl._create_unverified_context()
        response = urlopen(url, context=ssl_context)
        zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
        zip_file.extractall("./ml-100k")
        print("✅ Dataset downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def process_movielens_data():
    """Process MovieLens data into CSV format"""
    data_path = "./ml-100k/ml-100k/u.data"
    item_path = "./ml-100k/ml-100k/u.item"
    
    if not os.path.exists(data_path):
        print("❌ MovieLens data files not found. Run download_movielens_100k() first.")
        return False
    
    print("📊 Processing MovieLens data...")
    
    # Load ratings
    ratings = pd.read_csv(
        data_path,
        sep='\t',
        header=None,
        names=['userId', 'movieId', 'rating', 'timestamp'],
        encoding='latin-1'
    )
    
    # Load movies
    movies = pd.read_csv(
        item_path,
        sep='|',
        header=None,
        names=['movieId', 'title', 'release_date', 'video_release_date', 'imdb_url', 
               'unknown', 'action', 'adventure', 'animation', 'childrens', 'comedy',
               'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror',
               'musical', 'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'],
        encoding='latin-1'
    )
    
    # Merge ratings with movie titles
    ratings_with_titles = ratings[['userId', 'movieId', 'rating']].merge(
        movies[['movieId', 'title']],
        on='movieId',
        how='left'
    )
    
    # Create the final dataset
    final_data = ratings_with_titles[['userId', 'title', 'rating']].copy()
    
    # Save to CSV
    final_data.to_csv('movielens_100k.csv', index=False)
    print(f"✅ Processed {len(final_data)} ratings")
    print(f"✅ {final_data['userId'].nunique()} unique users")
    print(f"✅ {final_data['title'].nunique()} unique movies")
    print("✅ Saved to movielens_100k.csv")
    
    return True

def load_movielens():
    """Complete pipeline: download and process MovieLens data"""
    # Check if already exists
    if os.path.exists('movielens_100k.csv'):
        print("✅ movielens_100k.csv already exists!")
        return True
    
    # Check if data is already extracted
    if not os.path.exists('./ml-100k'):
        if not download_movielens_100k():
            return False
    else:
        print("✅ MovieLens data found (already downloaded)")
    
    return process_movielens_data()

if __name__ == "__main__":
    load_movielens()
