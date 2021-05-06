import sqlite3

from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from typing import List


app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/products")
async def products():
    products = app.db_connection.execute("SELECT ProductName FROM Products").fetchall()
    return {
        "products": products,
        "products_counter": len(products)
    }


@app.get("/suppliers/{supplier_id}")
async def single_supplier(supplier_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = :supplier_id",
        {'supplier_id': supplier_id}).fetchone()

    return data


@app.get("/employee_with_region")
async def employee_with_region():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT Employees.LastName, Employees.FirstName, Territories.TerritoryDescription 
        FROM Employees JOIN EmployeeTerritories ON Employees.EmployeeID = EmployeeTerritories.EmployeeID
        JOIN Territories ON EmployeeTerritories.TerritoryID = Territories.TerritoryID;
     ''').fetchall()
    return [{"employee": f"{x['FirstName']} {x['LastName']}", "region": x["TerritoryDescription"]} for x in data]


@app.get("/customers")
async def customers():
    app.db_connection.row_factory = lambda cursor, x: x[0]
    artists = app.db_connection.execute("SELECT CompanyName FROM Customers").fetchall()
    return artists


class Customer(BaseModel):
    company_name: str


@app.post("/customers/add")
async def customers_add(customer: Customer):
    cursor = app.db_connection.execute(
        f"INSERT INTO Customers (CompanyName) VALUES ('{customer.company_name}')"
    )
    app.db_connection.commit()
    return {
        "CustomerID": cursor.lastrowid,
        "CompanyName": customer.company_name
    }


class Shipper(BaseModel):
    company_name: str


@app.patch("/shippers/edit/{shipper_id}")
async def artists_add(shipper_id: int, shipper: Shipper):
    cursor = app.db_connection.execute(
        "UPDATE Shippers SET CompanyName = ? WHERE ShipperID = ?", (
            shipper.company_name, shipper_id)
    )
    app.db_connection.commit()

    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        """SELECT ShipperID AS shipper_id, CompanyName AS company_name
         FROM Shippers WHERE ShipperID = ?""",
        (shipper_id, )).fetchone()

    return data


@app.get("/orders")
async def orders():
    app.db_connection.row_factory = sqlite3.Row
    orders = app.db_connection.execute("SELECT * FROM Orders").fetchall()
    return {
        "orders_counter": len(orders),
        "orders": orders,
    }


@app.delete("/orders/delete/{order_id}")
async def order_delete(order_id: int):
    cursor = app.db_connection.execute(
        "DELETE FROM Orders WHERE OrderID = ?", (order_id, )
    )
    app.db_connection.commit()
    return {"deleted": cursor.rowcount}


@app.get("/region_count")
async def root():
    app.db_connection.row_factory = lambda cursor, x: x[0]
    regions = app.db_connection.execute(
        "SELECT RegionDescription FROM Regions ORDER BY RegionDescription DESC").fetchall()
    count = app.db_connection.execute('SELECT COUNT(*) FROM Regions').fetchone()

    return {
        "regions": regions,
        "regions_counter": count
    }
