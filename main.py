import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProductIn(BaseModel):
    name: str
    price: float
    category_id: int

@app.get("/")
def home():
    return {"message": "Shopping API is running"}

def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@app.get("/products")
def list_products():
    conn = get_db()
    rows = conn.execute(
        "SELECT products.id, products.name, products.price, "
        "categories.name AS category "
        "FROM products JOIN categories ON products.category_id = categories.id"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/products/{product_id}")
def get_product(product_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT products.id, products.name, products.price, "
        "categories.name AS category "
        "FROM products JOIN categories ON products.category_id = categories.id "
        "WHERE products.id = ?",
        (product_id,),
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)


@app.post("/products", status_code=201)
def create_product(product: ProductIn):
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO products (name, price, category_id) VALUES(?, ?, ?)",
            (product.name, product.price, product.category_id),
        )
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Category does not exist")
    finally:
        conn.close()
    return {"id": new_id, **product.model_dump()}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = get_db()
    cursor = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"deleted: product_id"}

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductIn):
    conn = get_db()
    try:
        cursor = conn.execute(
            "UPDATE products SET name = ?, price = ?, category_id = ? WHERE id = ?",
            (product.name, product.price, product.category_id, product_id),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Category does not exist")
    finally:
        conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product_id, **product.model_dump()}
