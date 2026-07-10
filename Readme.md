# 🎬 Movie Recommendation System

A professionally refactored, production-ready **Content-Based and Popularity-Based Movie Recommendation System** in Python. Features include a dynamic UI built with Streamlit and a robust search utility supporting partial queries, case-insensitivity, and fuzzy typing fallback.

---

## 📂 Project Structure

The project has been organized following the **Separation of Concerns** principle:

```
Movie-Recommendation-System/
│
├── data/
│   ├── movies.csv             # Movie metadata (movieId, title, genres)
│   └── ratings.csv            # User rating scores (userId, movieId, rating, timestamp)
│
├── data_loader.py             # Handles reading CSV files and merging datasets
├── analysis.py                # Script for dataset exploration, duplicate/missing checks
├── popularity.py              # Logic for popular (average rating & rating count) recommendations
├── search.py                  # Space, case, partial, and fuzzy movie title search logic
├── recommender.py             # Content-based recommendation (TF-IDF & Cosine Similarity on genres)
├── app.py                     # Streamlit User Interface (UI layer only)
├── requirements.txt           # Declares Python package dependencies
├── README.md                  # Detailed overview of design and usage
└── .gitignore                 # Configured to ignore virtual env, cache, and system files
```

---

## 🔬 How the Search Algorithm Works

The search utility in `search.py` is implemented using a multi-layered waterfall approach to retrieve results with maximum responsiveness and accuracy:

1. **Query Normalization**:
   The input string is stripped of leading/trailing whitespace, converted to lowercase, and internal multi-spaces are collapsed to a single space.
2. **Layer 1: Partial Substring Match**:
   The algorithm first scans all movie titles for a case-insensitive substring match. For example, search query `"dark"` immediately returns `"The Dark Knight"` and `"The Dark Knight Rises"`.
3. **Layer 2: Fuzzy Match (Typo Tolerance)**:
   If no exact substring matches are found, it invokes a fuzzy matching algorithm.
   - It attempts to use **RapidFuzz's** `process.extract` with `fuzz.WRatio` (a weighted ratio score that excels at spelling errors or omitted letters).
   - If the user searches for `"batmn"`, the system returns `"Batman (1989)"`. If `"avengrs"` is typed, it returns `"The Avengers (2012)"`.
   - A threshold of `60.0` is enforced to prevent matching completely unrelated titles.
   - **Fallback**: If `rapidfuzz` is not installed, it seamlessly falls back to Python's standard `difflib.get_close_matches`.
4. **Layer 3: No-Match Handling**:
   If no matches are found in either step, it returns a list containing `["No matching movies found."]` rather than throwing an exception.

---

## ⚙️ Setup and Installation

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Applications

### Run Dataset Exploration
To run the exploratory data analysis report (equivalent to the first half of the original monolithic script):
```bash
python analysis.py
```

### Run Popularity Recommendations
To compute the top 10 recommended movies based on popularity metrics:
```bash
python popularity.py
```

### Run Content-Based Recommender (Console Demo)
To print genre-based TF-IDF metrics and similar movie list for `"Toy Story (1995)"`:
```bash
python recommender.py
```

### Launch the Streamlit Web Application
To run the visual interactive dashboard:
```bash
streamlit run app.py
```

---

## 🧠 Architectural & Refactoring Decisions

* **Separation of Concerns**: We isolated dataset exploration (`analysis.py`), data loading (`data_loader.py`), recommendation algorithms (`recommender.py` & `popularity.py`), search routines (`search.py`), and the UI (`app.py`). This decoupling makes components independently testable, reusable, and easy to maintain.
* **Module-Level Caching**: Loaded datasets, TF-IDF fits, and similarity calculations are computed once at the module level when `recommender.py` is imported, rather than recalculating them on every interaction. This guarantees sub-millisecond recommendation responses.
* **Beginner-Friendly Type Hints**: Standard Python type-hints (`List`, `Tuple`, etc.) and structured docstrings were added to make the code self-documenting and IDE-friendly, which is a major criteria in software engineering interviews.
* **Defensive Design**: Handled edge-cases (like missing inputs, empty search inputs, and missing movies) cleanly to prevent runtime crashes.