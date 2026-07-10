import pandas as pd
from data_loader import load_and_merge_data

def get_popularity_recommendations(min_rating_count: int = 50) -> pd.DataFrame:
    """
    Calculate popularity-based recommendations by grouping merged movie data.
    
    Filters movies with ratings count >= min_rating_count and sorts by Average Rating.
    
    Args:
        min_rating_count (int): Minimum number of ratings required to be included. Default is 50.
        
    Returns:
        pd.DataFrame: DataFrame containing 'Average Rating' and 'Rating Count' columns,
                      indexed by movie title, sorted descending by Average Rating.
    """
    movie_data = load_and_merge_data()
    
    # Calculate average rating per movie title
    movie_ratings = movie_data.groupby('title')["rating"].mean()
    
    # Calculate rating count per movie title
    ratings_count = movie_data.groupby('title')["rating"].count()
    
    # Combine into a recommendation DataFrame
    recommendation = pd.DataFrame()
    recommendation["Average Rating"] = movie_ratings
    recommendation["Rating Count"] = ratings_count
    
    # Filter by minimum rating count
    recommendation = recommendation[recommendation["Rating Count"] >= min_rating_count]
    
    # Sort by Average Rating descending
    recommendation = recommendation.sort_values(by="Average Rating", ascending=False)
    
    return recommendation

if __name__ == "__main__":
    # Test/Demo execution mirroring the original console output
    print("Calculating popularity metrics...")
    
    movie_data = load_and_merge_data()
    
    # Average ratings
    movie_ratings = movie_data.groupby('title')["rating"].mean().sort_values(ascending=False)
    print("\nTop 10 average ratings (no count filter):")
    print(movie_ratings.head(10))
    
    # Rating counts
    ratings_count = movie_data.groupby('title')["rating"].count().sort_values(ascending=False)
    print("\nTop 10 rating counts:")
    print(ratings_count.head(10))
    
    # Combined & filtered recommendation
    print("\nApplying rating count threshold >= 50 and sorting by Average Rating...")
    recommendation = get_popularity_recommendations(min_rating_count=50)
    print("\nTop 10 Recommended Movies (Popularity-Based):")
    print(recommendation.head(10))
    print()
