# 🎬 Movie Recommendation System

An AI-powered movie recommendation system that recommends movies similar to a movie selected by the user.

The system uses **content-based filtering**, **NLP**, and **cosine similarity** to find movies with similar characteristics.

## 🚀 Features

- Search for movies
- Get movie recommendations
- Content-based recommendation
- NLP-based movie similarity
- FastAPI backend
- Simple web frontend
- Memory-efficient recommendation generation
- Movie details API

## 🧠 How It Works

The recommendation system works using content-based filtering.

Movie information such as genres, keywords, overview, cast, and other text-based features are combined into a single representation.

The text is converted into numerical vectors using `CountVectorizer`.

Cosine similarity is then used to determine how similar two movies are.

```text
Movie Dataset
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Text Processing
      ↓
CountVectorizer
      ↓
Movie Vectors
      ↓
Similarity Calculation
      ↓
Top Similar Movies
      ↓
FastAPI
      ↓
Frontend