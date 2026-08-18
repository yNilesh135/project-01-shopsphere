from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to ShopSphere API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}