import sqlite3

cart = []


def search_products(category: str = None, max_price: float = None):
    """ Search the shop. category is 'electronics', 'books' or 'stationery'. max_price limits the price."""
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    query = (
        "SELECT products.id, products.name, products.price, "
        "categories.name AS category "
        "FROM products JOIN categories ON products.category_id = categories.id "
        "WHERE 1=1"
    )
    params = []
    if category:
        query += " AND categories.name = ?"
        params.append(category)
    if max_price is not None:
        query += " AND products.price <= ?"
        params.append(max_price)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_to_cart(product_id: int):
    """Add one product to the cart using its id."""
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT id, name, price FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return {"error": "Product not found"}
    cart.append(dict(row))
    return {"added": row["name"], "cart_size": len(cart)}
