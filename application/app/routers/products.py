from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Headphones", "price": 3000}
]


@router.get("/")
def get_products():
    return products


@router.get("/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/", status_code=201)
def create_product(product: ProductCreate):
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return new_product