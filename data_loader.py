import os
import pandas as pd

# Define paths relative to this file to ensure reliability across environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_PATH = os.path.join(BASE_DIR, "data", "movies.csv")
RATINGS_PATH = os.path.join(BASE_DIR, "data", "ratings.csv")

def load_movies_raw() -> pd.DataFrame:
    """
    Load the raw movies dataset from the CSV file.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing columns: movieId, title, genres.
    """
    return pd.read_csv(MOVIES_PATH)

def load_ratings_raw() -> pd.DataFrame:
    """
    Load the raw ratings dataset from the CSV file.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing columns: userId, movieId, rating, timestamp.
    """
    return pd.read_csv(RATINGS_PATH)

def load_and_merge_data() -> pd.DataFrame:
    """
    Load movies and ratings datasets, and merge them on 'movieId'.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing the merged dataset.
    """
    movies_df = load_movies_raw()
    ratings_df = load_ratings_raw()
    return pd.merge(movies_df, ratings_df, on="movieId")

if __name__ == "__main__":
    # Small test runner to verify loading works as expected
    print("Testing data loader...")
    try:
        movies = load_movies_raw()
        ratings = load_ratings_raw()
        merged = load_and_merge_data()
        print(f"Success! Movies: {movies.shape}, Ratings: {ratings.shape}, Merged: {merged.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
