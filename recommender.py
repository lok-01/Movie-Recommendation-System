import pandas as pd
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_movies_raw

# 1. Load movies dataset at module level to act as a cache
movies = load_movies_raw()

# 2. Fit TF-IDF Vectorizer on 'genres' column
# Ignore standard English stop words as per original algorithm
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# 3. Calculate the Cosine Similarity matrix
similarity = cosine_similarity(tfidf_matrix)

def recommend_movies(movie_name: str) -> List[Tuple[str, float]]:
    """
    Recommend movies similar to the given movie name based on genres.
    
    Args:
        movie_name (str): The exact movie title to get recommendations for.
        
    Returns:
        List[Tuple[str, float]]: A list of tuples containing (movie_title, similarity_score).
                                 Returns an empty list if the movie title is not found.
    """
    if movie_name not in movies["title"].values:
        return []

    # Find the index of the matching movie
    movie_index = movies[movies["title"] == movie_name].index[0]

    # Get similarity scores for all movies against this movie
    similarity_scores = similarity[movie_index]

    # Sort movies based on similarity scores (excluding the movie itself, returning top 5)
    movie_list = sorted(
        list(enumerate(similarity_scores)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommendations = []
    for index, score in movie_list:
        recommendations.append(
            (movies.iloc[index].title, float(score))
        )

    return recommendations

if __name__ == "__main__":
    # Test execution mirroring the original console output
    print("TF-IDF Matrix Shape:", tfidf_matrix.shape)
    print("\nFeature names (first 10):")
    print(tfidf.get_feature_names_out()[:10])
    
    print("\nSimilarity Matrix Shape:", similarity.shape)
    
    # Test movie recommendations
    test_movie = "Toy Story (1995)"
    print(f"\nRecommendations for '{test_movie}':")
    recs = recommend_movies(test_movie)
    for movie, score in recs:
        print(f"- {movie} (Score: {score:.4f})")
    print()
