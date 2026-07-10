import streamlit as st
from search import search_movies, get_all_movie_titles
from recommender import recommend_movies

# Page Configuration for a Premium Look
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

# Custom Styling (CSS) for a beautiful interface
st.markdown("""
    <style>
        .stButton>button {
            background: linear-gradient(45deg, #ff4b4b, #ff7676);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        }
        .recommendation-card {
            background-color: #f3f4f6;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 5px solid #ff4b4b;
            transition: transform 0.2s ease-in-out;
        }
        .recommendation-card:hover {
            transform: translateX(5px);
        }
        /* Dark mode compatibility for the cards */
        @media (prefers-color-scheme: dark) {
            .recommendation-card {
                background-color: #1f2937;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Page Title
st.title("🎬 Movie Recommendation System")
st.write("Search for a movie you like, and we will recommend similar titles based on their genres.")

# 1. Search Box
search_query = st.text_input(
    "🔍 Search for a Movie",
    placeholder="Type a movie title (e.g., toy, batmn, dark) or leave empty to browse all"
)

# Fetch options based on search query
if search_query.strip():
    results = search_movies(search_query)
else:
    results = get_all_movie_titles()

selected_movie = None

# 2. Dropdown (or search suggestions)
if not results:
    st.warning("⚠️ No movies available.")
elif results == ["No matching movies found."]:
    st.warning("⚠️ No matching movies found. Please try another search term.")
else:
    selected_movie = st.selectbox(
        "Select Movie",
        options=results
    )

# 3. Recommend Button & 4. Display Recommendations
if st.button("Recommend") and selected_movie:
    if selected_movie == "No matching movies found.":
        st.error("Please select a valid movie.")
    else:
        with st.spinner("Finding recommendations..."):
            recommendations = recommend_movies(selected_movie)
            
            if recommendations:
                st.subheader("Recommended Movies")
                for movie, score in recommendations:
                    # Display movie card
                    st.markdown(
                        f"""
                        <div class="recommendation-card">
                            <span style="font-size: 1.1em; font-weight: bold;">⭐ {movie}</span>
                            <br/>
                            <span style="color: #9ca3af; font-size: 0.9em;">Match Score: {score:.3f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No recommendations found for the selected movie.")