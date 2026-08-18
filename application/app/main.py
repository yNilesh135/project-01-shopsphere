from fastapi import FastAPI
from application.app.routers import products

app = FastAPI()


app.include_router(products.router)


@app.get("/")
def home():
    return {"message": "Welcome to ShopSphere API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}