import pandas as pd

# Load datasets
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")

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
print(movies.info())

print()

print("Ratings Info")
print(ratings.info())

print("Missing Values in Movies")
print(movies.isnull().sum())

print()

print("Missing Values in Ratings")
print(ratings.isnull().sum())

print()

# -------------------------------
# Duplicate Rows
# -------------------------------

print("Duplicate Movies:", movies.duplicated().sum())
print("Duplicate Ratings:", ratings.duplicated().sum())

movie_data=pd.merge(movies,ratings , on='movieId')

print("Merged Data Shape:", movie_data.shape)
print(movie_data.head())


movie_ratings=movie_data.groupby('title')["rating"].mean().sort_values(ascending=False)

print()

print(movie_ratings.head(10))


ratings_count=movie_data.groupby('title')["rating"].count().sort_values(ascending=False)

recommendation=pd.DataFrame()


recommendation["Average Rating"]=movie_ratings
recommendation["Rating Count"]=ratings_count

print(recommendation.head(10))


recommendation = recommendation[
    recommendation["Rating Count"] >= 50
]

# ============================
# Sort by Average Rating
# ============================

recommendation = recommendation.sort_values(
    by="Average Rating",
    ascending=False
)

# ============================
# Top 10 Movies
# ============================

print("\nTop 10 Recommended Movies")
print(recommendation.head(10))


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(movies["genres"])
print(tfidf_matrix.shape)
print(tfidf.get_feature_names_out())


from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(tfidf_matrix)

print(similarity.shape)


def recommend_movies(movie_name):
    
    # Check whether the movie exists
    if movie_name not in movies["title"].values:
        print("Movie not found!")
        return

    movie_index = movies[movies["title"] == movie_name].index[0]

    similarity_scores = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(similarity_scores)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    print("\nRecommended Movies:\n")

    for movie_index, score in movie_list:
        print(f"{movies.iloc[movie_index].title}  -->  Similarity : {score:.3f}")


movie = input("Enter Movie Name: ")

recommend_movies(movie)