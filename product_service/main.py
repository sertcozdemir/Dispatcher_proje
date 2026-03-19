from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Mongo bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["product_db"]
collection = db["products"]

# Model
class Product(BaseModel):
    id: int
    name: str
    price: float

# Ürün ekleme
@app.post("/products", status_code=201)
def create_product(product: Product):
    if collection.find_one({"id": product.id}):
        raise HTTPException(status_code=400, detail="Product already exists")

    collection.insert_one(product.model_dump())
    return product

# Ürün getirme
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = collection.find_one({"id": product_id}, {"_id": 0})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product