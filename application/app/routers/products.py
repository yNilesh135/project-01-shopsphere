from fastapi import Depends
from sqlalchemy.orm import Session
from application.app.database import get_db
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from application.app.schemas import ProductCreate, ProductResponse, ProductUpdate

from application.app.models import Product



router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


products = [
    {"id": 1, "name": "Laptop", "price": 55000},
    {"id": 2, "name": "Headphones", "price": 3000}
]


@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    result = db.scalars(select(Product))
    return result.all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = product_update.name
    product.price = product_update.price

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()