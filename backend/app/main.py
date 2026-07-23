from fastapi import FastAPI

app = FastAPI(title="Chess Skill Assessment API")


@app.get("/")
def root():
    return {
        "message": "Chess Skill Assessment API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }