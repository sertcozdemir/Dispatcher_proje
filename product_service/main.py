from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Mongo bağlantısı
client = MongoClient("mongodb://mongo_product:27017/")
db = client["product_db"]
collection = db["products"]

# Model
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str
class ProductResponse(BaseModel):
    id: int
    name:str
    price:float
    stock: int
    category:str


# Ürün ekleme
@app.post("/products", status_code=201,
          response_model=ProductResponse,
          responses={
              201:{
                  "description":"Prod Created Succesfully"
              }
          },summary="Create Product")
def create_product(product: ProductCreate):
    last_product=collection.find_one(sort=[("id",-1)])
    new_id= 1 if last_product is None else last_product["id"]+1
    new_product={
        "id":new_id,
        "name":product.name,
        "price":product.price,
        "stock":product.stock,
        "category":product.category
    }
    collection.insert_one(new_product)
    return {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "category": product.category
    }

# Ürün getirme
@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = collection.find_one({"id": product_id}, {"_id": 0})

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product