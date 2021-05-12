CREATE SEQUENCE categories_CategoryID_seq OWNED BY categories."CategoryID";
SELECT setval('categories_CategoryID_seq', coalesce(max("CategoryID"), 0) + 1, false) FROM categories;
ALTER TABLE categories ALTER COLUMN "CategoryID" SET DEFAULT nextval('categories_CategoryID_seq');


CREATE SEQUENCE employees_EmployeeID_seq OWNED BY employees."EmployeeID";
SELECT setval('employees_EmployeeID_seq', coalesce(max("EmployeeID"), 0) + 1, false) FROM employees;
ALTER TABLE employees ALTER COLUMN "EmployeeID" SET DEFAULT nextval('employees_EmployeeID_seq');


ALTER TABLE customerdemographics ALTER COLUMN "CustomerTypeID" TYPE smallint USING "CustomerTypeID"::integer;
CREATE SEQUENCE customerdemographics_CustomerTypeID_seq OWNED BY customerdemographics."CustomerTypeID";
SELECT setval('customerdemographics_CustomerTypeID_seq', coalesce(max("CustomerTypeID"), 0) + 1, false) FROM customerdemographics;
ALTER TABLE customerdemographics ALTER COLUMN "CustomerTypeID" SET DEFAULT nextval('customerdemographics_CustomerTypeID_seq');



ALTER TABLE territories ALTER COLUMN "TerritoryID" TYPE int USING "TerritoryID"::integer ;
ALTER TABLE employeeterritories ALTER COLUMN "TerritoryID" TYPE int USING "TerritoryID"::integer ;
CREATE SEQUENCE territories_TerritoryID_seq OWNED BY territories."TerritoryID";
SELECT setval('territories_TerritoryID_seq', coalesce(max("TerritoryID"), 0) + 1, false) FROM territories;
ALTER TABLE territories ALTER COLUMN "TerritoryID" SET DEFAULT nextval('territories_TerritoryID_seq');


CREATE SEQUENCE orders_OrderID_seq OWNED BY orders."OrderID";
SELECT setval('orders_OrderID_seq', coalesce(max("OrderID"), 0) + 1, false) FROM orders;
ALTER TABLE orders ALTER COLUMN "OrderID" SET DEFAULT nextval('orders_OrderID_seq');


CREATE SEQUENCE products_ProductID_seq OWNED BY products."ProductID";
SELECT setval('products_ProductID_seq', coalesce(max("ProductID"), 0) + 1, false) FROM products;
ALTER TABLE products ALTER COLUMN "ProductID" SET DEFAULT nextval('products_ProductID_seq');


CREATE SEQUENCE region_RegionID_seq OWNED BY region."RegionID";
SELECT setval('region_RegionID_seq', coalesce(max("RegionID"), 0) + 1, false) FROM region;
ALTER TABLE region ALTER COLUMN "RegionID" SET DEFAULT nextval('region_RegionID_seq');


CREATE SEQUENCE shippers_ShipperID_seq OWNED BY shippers."ShipperID";
SELECT setval('shippers_ShipperID_seq', coalesce(max("ShipperID"), 0) + 1, false) FROM shippers;
ALTER TABLE shippers ALTER COLUMN "ShipperID" SET DEFAULT nextval('shippers_ShipperID_seq');


CREATE SEQUENCE shippers_tmp_ShipperID_seq OWNED BY shippers_tmp."ShipperID";
SELECT setval('shippers_tmp_ShipperID_seq', coalesce(max("ShipperID"), 0) + 1, false) FROM shippers_tmp;
ALTER TABLE shippers_tmp ALTER COLUMN "ShipperID" SET DEFAULT nextval('shippers_tmp_ShipperID_seq');



CREATE SEQUENCE suppliers_SupplierID_seq OWNED BY suppliers."SupplierID";
SELECT setval('suppliers_SupplierID_seq', coalesce(max("SupplierID"), 0) + 1, false) FROM suppliers;
ALTER TABLE suppliers ALTER COLUMN "SupplierID" SET DEFAULT nextval('suppliers_SupplierID_seq');


CREATE SEQUENCE usstates_StateID_seq OWNED BY usstates."StateID";
SELECT setval('usstates_StateID_seq', coalesce(max("StateID"), 0) + 1, false) FROM usstates;
ALTER TABLE usstates ALTER COLUMN "StateID" SET DEFAULT nextval('usstates_StateID_seq');

