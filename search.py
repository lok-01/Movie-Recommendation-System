import pandas as pd
from typing import List
from data_loader import load_movies_raw

def get_all_movie_titles() -> List[str]:
    """
    Get a list of all unique movie titles from the dataset.
    
    Returns:
        List[str]: A list of unique movie title strings.
    """
    movies_df = load_movies_raw()
    return movies_df["title"].dropna().unique().tolist()

def search_movies(query: str, titles: List[str] = None) -> List[str]:
    """
    Search for movie titles that match the search query.
    
    Supports:
      1. Case-insensitive matching.
      2. Space-insensitive matching (ignores leading/trailing and duplicate internal spaces).
      3. Partial search (substring matching).
      4. Fuzzy search (handles typos like 'batmn' -> 'Batman (1989)', 'avengrs' -> 'The Avengers (2012)').
      
    Args:
        query (str): The search query typed by the user.
        titles (List[str], optional): The list of movie titles to search. 
                                      If None, all titles from the dataset are loaded.
                                      
    Returns:
        List[str]: A list of matched movie titles, or ["No matching movies found."] if no matches.
    """
    if titles is None:
        titles = get_all_movie_titles()
        
    # Normalize query: strip whitespace, lowercase, and resolve multiple spaces to single spaces
    normalized_query = " ".join(query.strip().split()).lower()
    
    # If the search query is empty after normalization, return an empty list (or all titles, managed in UI)
    if not normalized_query:
        return []

    # Step 1: Substring/Partial Match (Case & space normalized)
    partial_matches = []
    for title in titles:
        normalized_title = " ".join(title.strip().split()).lower()
        if normalized_query in normalized_title:
            partial_matches.append(title)
            
    if partial_matches:
        return partial_matches

    # Step 2: Fuzzy Matching (Typos handling)
    # Attempt to use rapidfuzz; fallback to difflib
    fuzzy_matches = []
    try:
        from rapidfuzz import process, fuzz
        # WRatio is weighted ratio; excellent for search queries with minor typos/abbreviations
        results = process.extract(normalized_query, titles, scorer=fuzz.WRatio, limit=5)
        # 60.0 is a reasonable similarity threshold
        fuzzy_matches = [match[0] for match in results if match[1] >= 60.0]
    except ImportError:
        import difflib
        fuzzy_matches = difflib.get_close_matches(normalized_query, titles, n=5, cutoff=0.5)

    if fuzzy_matches:
        return fuzzy_matches

    # Step 3: No matches found
    return ["No matching movies found."]

if __name__ == "__main__":
    # Test cases to verify the search functionality
    print("Testing Search Feature:")
    titles = get_all_movie_titles()
    
    test_queries = [
        "toy",              # Case-insensitive / Substring
        "   toy story   ",  # Extra spaces
        "dark",             # Partial match
        "batmn",            # Fuzzy Match 1
        "avengrs",          # Fuzzy Match 2
        "xyzrandommovie",   # No match
    ]
    
    for q in test_queries:
        res = search_movies(q, titles)
        print(f"Query: '{q}' -> Results (first 4 shown): {res[:4]}")
