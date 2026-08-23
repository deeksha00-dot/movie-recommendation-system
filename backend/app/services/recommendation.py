import os
import pickle
import pandas as pd


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        ".."
    )
)


# ============================================================
# FILE PATHS
# ============================================================

MOVIES_PATH = os.path.join(
    BASE_DIR,
    "data",
    "movies.pkl"
)

RECOMMENDATIONS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "recommendations.pkl"
)

MOVIE_DETAILS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "movie_details.pkl"
)


# ============================================================
# LOAD DATA
# ============================================================

# Main movie dataset used by the recommendation system
movies = pd.read_pickle(MOVIES_PATH)


# Pre-computed recommendation indices
with open(RECOMMENDATIONS_PATH, "rb") as f:
    recommendations = pickle.load(f)


# Movie metadata
movie_details = pd.read_pickle(MOVIE_DETAILS_PATH)


# ============================================================
# CREATE FAST MOVIE DETAILS LOOKUP
# ============================================================

movie_details_lookup = (
    movie_details
    .set_index("id")
    .to_dict(orient="index")
)


# ============================================================
# RECOMMEND MOVIES
# ============================================================

def recommend(movie: str):

    # Find the movie
    matches = movies[
        movies["title"]
        .str.lower()
        == movie.lower()
    ]

    # Movie not found
    if matches.empty:
        return []

    # Get the index of the selected movie
    movie_index = matches.index[0]

    # Get pre-computed recommendation indices
    recommended_indices = recommendations[movie_index]

    result = []

    for index in recommended_indices:

        # Get movie ID
        movie_id = int(
            movies.iloc[index]["id"]
        )

        # Get movie title
        title = movies.iloc[index]["title"]

        # Get additional movie information
        details = movie_details_lookup.get(
            movie_id,
            {}
        )

        result.append({
            "id": movie_id,
            "title": title,
            "overview": details.get(
                "overview",
                ""
            ),
            "release_date": details.get(
                "release_date",
                ""
            ),
            "rating": float(
                details.get(
                    "vote_average",
                    0
                )
            ),
            "vote_count": int(
                details.get(
                    "vote_count",
                    0
                )
            )
        })

    return result



def search_movies(
    query: str,
    limit: int = 10
):

    query = query.lower().strip()

    # Empty search
    if not query:
        return []

    # Find movies containing the search term
    matches = movies[
        movies["title"]
        .str.lower()
        .str.contains(
            query,
            na=False
        )
    ].head(limit)

    result = []

    for _, movie in matches.iterrows():

        movie_id = int(
            movie["id"]
        )

        result.append({
            "id": movie_id,
            "title": movie["title"]
        })

    return result



def get_movie_details(movie_id: int):

    return movie_details_lookup.get(
        movie_id
    )