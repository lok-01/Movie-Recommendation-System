import pandas as pd
from data_loader import load_movies_raw, load_ratings_raw, load_and_merge_data

def run_dataset_exploration() -> None:
    """
    Perform dataset exploration and print key statistics to the console.
    
    Includes shape, columns, info, missing values, duplicate values,
    and merged dataset preview.
    """
    # Load raw datasets
    movies = load_movies_raw()
    ratings = load_ratings_raw()

    # Shape (rows, columns)
    print("Movies Shape:", movies.shape)
    print("Ratings Shape:", ratings.shape)
    print()

    # Column names
    print("Movies Columns:")
    print(movies.columns)
    print()

    print("Ratings Columns:")
    print(ratings.columns)
    print()

    # Information about datasets
    print("Movies Info")
    movies.info()
    print()

    print("Ratings Info")
    ratings.info()
    print()

    # Missing values
    print("Missing Values in Movies")
    print(movies.isnull().sum())
    print()

    print("Missing Values in Ratings")
    print(ratings.isnull().sum())
    print()

    # Duplicate Rows
    print("Duplicate Movies:", movies.duplicated().sum())
    print("Duplicate Ratings:", ratings.duplicated().sum())
    print()

    # Merged Data Info
    movie_data = load_and_merge_data()
    print("Merged Data Shape:", movie_data.shape)
    print(movie_data.head())

if __name__ == "__main__":
    run_dataset_exploration()
