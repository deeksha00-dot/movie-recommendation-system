from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Movie Recommendation API is running!"}