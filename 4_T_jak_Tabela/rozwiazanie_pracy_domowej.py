import sqlite3
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

ALLOWED_ORDERS = {
    "last_name": "ORDER BY last_name ASC",
    "first_name": "ORDER BY first_name ASC",
    "city": "ORDER BY city ASC",
}


class Category(BaseModel):
    name: str


@contextmanager
def fetch_single_product(product_id: int):
    app.db_connection.row_factory = sqlite3.Row
    product = app.db_connection.execute(
        "SELECT ProductID AS id, ProductName as name FROM products WHERE ProductID = :product_id",
        {"product_id": product_id},
    ).fetchone()
    yield product


@contextmanager
def fetch_single_category(category_id: int):
    app.db_connection.row_factory = sqlite3.Row
    category = app.db_connection.execute(
        "SELECT CategoryID, CategoryName FROM categories WHERE CategoryID = :category_id",
        {"category_id": category_id},
    ).fetchone()
    yield category


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    categories = app.db_connection.execute(
        "SELECT CategoryID, CategoryName FROM categories ORDER BY CategoryID"
    ).fetchall()
    return {
        "categories": [
            {"id": c["CategoryID"], "name": c["CategoryName"]} for c in categories
        ]
    }


@app.post("/categories", status_code=201)
async def add_category(category: Category):
    cursor = app.db_connection.execute(
        "INSERT INTO categories (CategoryName) VALUES (?)", (category.name,)
    )
    app.db_connection.commit()
    new_category_id = cursor.lastrowid

    with fetch_single_category(new_category_id) as fetched_category:
        return {
            "id": fetched_category["CategoryID"],
            "name": fetched_category["CategoryName"],
        }


@app.put("/categories/{category_id}")
async def edit_category(category_id: int, category: Category):
    with fetch_single_category(category_id) as fetched_category:
        if not fetched_category:
            raise HTTPException(status_code=404, detail="Not found")

    cursor = app.db_connection.execute(
        "UPDATE categories SET CategoryName = ? WHERE CategoryID = ?",
        (category.name, category_id),
    )
    app.db_connection.commit()

    with fetch_single_category(category_id) as fetched_category:
        return {
            "id": fetched_category["CategoryID"],
            "name": fetched_category["CategoryName"],
        }


@app.delete("/categories/{category_id}")
async def delete_category(category_id: int):
    with fetch_single_category(category_id) as fetched_category:
        if not fetched_category:
            raise HTTPException(status_code=404, detail="Not found")

    cursor = app.db_connection.execute(
        "DELETE FROM categories WHERE CategoryID = ?", (category_id,)
    )
    app.db_connection.commit()
    return {"deleted": cursor.rowcount}


@app.get("/customers")
async def customers():
    sql_query = """
        SELECT
            CustomerID AS id,
            CompanyName AS name,
            (Address || ' ' || PostalCode || ' ' || City || ' ' || Country) AS full_address 
        FROM customers
        ORDER BY LOWER(CustomerID)
    """
    # Alternatywne rozwiazanie Z COALESCE (zamiast LOWER mozna zastosowac UPPER)
    #
    # sql_query = """
    #     SELECT
    #         CustomerID AS id,
    #         CompanyName AS name,
    #         (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) AS full_address
    #     FROM customers
    #     ORDER BY LOWER(CustomerID)
    # """
    if limit and offset:
        sql_query = f"{sql_query} LIMIT :limit OFFSET :offset"
    elif limit:
        sql_query = f"{sql_query} LIMIT :limit"

    app.db_connection.row_factory = sqlite3.Row
    customers = app.db_connection.execute(
        sql_query, {"limit": limit, "offset": offset}
    ).fetchall()
    return {"customers": customers}


@app.get("/employees")
async def employees(limit: int = None, offset: int = None, order: str = None):
    # SPRAWDZANIE CZY DOSTALISMY PARAM ORDER I CZY JEST ON W TABLICY DOSTEPNYCH PARAMSOW
    if order and order not in ["last_name", "first_name", "city"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    sql_query = """
        SELECT EmployeeID AS id, 
            LastName AS last_name, 
            FirstName AS first_name, 
            City AS city 
        FROM Employees
    """
    if order:
        # MALO SEKUIRNE ROZWIAZANIE
        sql_query = f"{sql_query} ORDER BY {order} ASC"
        # TROCHE BARDZIE SEKUIRNE ROZWIAZANIE Z UZYCIEM SLOWNIKA
        # sql_query f"{sql_query} {ALLOWED_ORDERS[order]}"
    if limit and offset:
        sql_query = f"{sql_query} LIMIT :limit OFFSET :offset"
    elif limit:
        sql_query = f"{sql_query} LIMIT :limit"

    app.db_connection.row_factory = sqlite3.Row
    employees = app.db_connection.execute(
        sql_query, {"limit": limit, "offset": offset}
    ).fetchall()
    return {"employees": employees}


@app.get("/products/{product_id}")
async def single_product(product_id: int):
    with fetch_single_product(product_id) as product:
        if not product:
            raise HTTPException(status_code=404, detail="Not found")
        return product


@app.get("/products/{product_id}/orders")
async def single_product_orders(product_id: int):
    with fetch_single_product(product_id) as product:
        if not product:
            raise HTTPException(status_code=404, detail="Not found")

    orders = app.db_connection.execute(
        """
        SELECT 
            orders.OrderID AS id, 
            customers.CompanyName AS customer, 
            orddet.Quantity AS quantity,
            ROUND(((orddet.Quantity * orddet.UnitPrice) - (orddet.Quantity * orddet.UnitPrice * orddet.Discount)), 2) AS total_price 
        FROM Orders
        JOIN customers ON orders.CustomerID = customers.CustomerID
        JOIN 'Order Details' AS orddet ON orders.OrderID = orddet.OrderID AND orddet.ProductID = :product_id 
        ORDER BY id    
        """,
        {"product_id": product_id},
    ).fetchall()
    return {"orders": orders}


@app.get("/products_extended")
async def products_categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        """
        SELECT 
            ProductID AS id, 
            ProductName AS name, 
            categories.CategoryName AS category, 
            suppliers.CompanyName AS supplier 
        FROM products
        JOIN categories ON products.CategoryID = categories.CategoryID
        JOIN suppliers ON products.SupplierID = suppliers.SupplierID
        """
    ).fetchall()
    return {"products_extended": data}
