from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.app.services.recommendation import (
    recommend,
    search_movies,
    get_movie_details
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Movie Recommendation API",
    description="AI-powered movie recommendation system",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# RESPONSE MODELS
# ============================================================

class MovieRecommendation(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str
    rating: float
    vote_count: int


class RecommendationResponse(BaseModel):
    movie: str
    recommendations: List[MovieRecommendation]


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running"
    }


# ============================================================
# SEARCH MOVIES
# ============================================================

@app.get("/search")
def search(
    query: str,
    limit: int = 10
):

    if limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than 0"
        )

    if limit > 50:
        raise HTTPException(
            status_code=400,
            detail="Limit cannot be greater than 50"
        )

    results = search_movies(
        query,
        limit
    )

    return {
        "query": query,
        "results": results
    }


# ============================================================
# RECOMMEND MOVIES
# ============================================================

@app.get(
    "/recommend/{movie_name}",
    response_model=RecommendationResponse
)
def get_recommendations(
    movie_name: str
):

    recommendations = recommend(
        movie_name
    )

    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail=f"Movie '{movie_name}' not found"
        )

    return {
        "movie": movie_name,
        "recommendations": recommendations
    }


# ============================================================
# GET MOVIE DETAILS
# ============================================================

@app.get("/movie/{movie_id}")
def movie_details_endpoint(
    movie_id: int
):

    details = get_movie_details(
        movie_id
    )

    if details is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {
        "id": movie_id,
        "title": details.get(
            "title",
            ""
        ),
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
    }