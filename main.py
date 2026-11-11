
from fastapi import FastAPI

app = FastAPI(
    title="Fintech API Integration Hub",
    description="A Python backend learning project",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Fintech API Integration Hub",
        "status": "running"
    }


@app.get("/about")
def about():
    return {
        "project": "Fintech API Integration Hub",
        "developer": "Your Name",
        "purpose": "Learning Python API Development",
        "version": "1.0"
    }
