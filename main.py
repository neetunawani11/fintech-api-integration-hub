from fastapi import FastAPI

app = FastAPI(
    title="Fintech API Intergration Hub",
    description="A Python backend learning project",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Fintech API Integration Hub",
        "status": "running"
    }