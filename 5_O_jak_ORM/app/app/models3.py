# coding: utf-8
from sqlalchemy import CHAR, Column, Date, Float, Integer, LargeBinary, SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    CategoryID = Column(SmallInteger, primary_key=True, server_default=text("nextval('categories_categoryid_seq'::regclass)"))
    CategoryName = Column(String(15), nullable=False)
    Description = Column(Text)
    Picture = Column(LargeBinary)


class Customercustomerdemo(Base):
    __tablename__ = 'customercustomerdemo'

    CustomerID = Column(CHAR(6), primary_key=True, nullable=False)
    CustomerTypeID = Column(CHAR(6), primary_key=True, nullable=False)


class Customerdemographic(Base):
    __tablename__ = 'customerdemographics'

    CustomerTypeID = Column(SmallInteger, primary_key=True, server_default=text("nextval('customerdemographics_customertypeid_seq'::regclass)"))
    CustomerDesc = Column(Text)


class Customer(Base):
    __tablename__ = 'customers'

    CustomerID = Column(CHAR(6), primary_key=True)
    CompanyName = Column(String(40), nullable=False)
    ContactName = Column(String(30))
    ContactTitle = Column(String(30))
    Address = Column(String(60))
    City = Column(String(15))
    Region = Column(String(15))
    PostalCode = Column(String(10))
    Country = Column(String(15))
    Phone = Column(String(24))
    Fax = Column(String(24))


class Employee(Base):
    __tablename__ = 'employees'

    EmployeeID = Column(SmallInteger, primary_key=True, server_default=text("nextval('employees_employeeid_seq'::regclass)"))
    LastName = Column(String(20), nullable=False)
    FirstName = Column(String(10), nullable=False)
    Title = Column(String(30))
    TitleOfCourtesy = Column(String(25))
    BirthDate = Column(Date)
    HireDate = Column(Date)
    Address = Column(String(60))
    City = Column(String(15))
    Region = Column(String(15))
    PostalCode = Column(String(10))
    Country = Column(String(15))
    HomePhone = Column(String(24))
    Extension = Column(String(4))
    Photo = Column(LargeBinary)
    Notes = Column(Text)
    ReportsTo = Column(SmallInteger)
    PhotoPath = Column(String(255))


class Employeeterritory(Base):
    __tablename__ = 'employeeterritories'

    EmployeeID = Column(SmallInteger, primary_key=True, nullable=False)
    TerritoryID = Column(Integer, primary_key=True, nullable=False)


class OrderDetail(Base):
    __tablename__ = 'order_details'

    OrderID = Column(SmallInteger, primary_key=True, nullable=False)
    ProductID = Column(SmallInteger, primary_key=True, nullable=False)
    UnitPrice = Column(Float, nullable=False)
    Quantity = Column(SmallInteger, nullable=False)
    Discount = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    OrderID = Column(SmallInteger, primary_key=True, server_default=text("nextval('orders_orderid_seq'::regclass)"))
    CustomerID = Column(CHAR(6))
    EmployeeID = Column(SmallInteger)
    OrderDate = Column(Date)
    RequiredDate = Column(Date)
    ShippedDate = Column(Date)
    ShipVia = Column(SmallInteger)
    Freight = Column(Float)
    ShipName = Column(String(40))
    ShipAddress = Column(String(60))
    ShipCity = Column(String(15))
    ShipRegion = Column(String(15))
    ShipPostalCode = Column(String(10))
    ShipCountry = Column(String(15))


class Product(Base):
    __tablename__ = 'products'

    ProductID = Column(SmallInteger, primary_key=True, server_default=text("nextval('products_productid_seq'::regclass)"))
    ProductName = Column(String(40), nullable=False)
    SupplierID = Column(SmallInteger)
    CategoryID = Column(SmallInteger)
    QuantityPerUnit = Column(String(20))
    UnitPrice = Column(Float)
    UnitsInStock = Column(SmallInteger)
    UnitsOnOrder = Column(SmallInteger)
    ReorderLevel = Column(SmallInteger)
    Discontinued = Column(Integer, nullable=False)


class Region(Base):
    __tablename__ = 'region'

    RegionID = Column(SmallInteger, primary_key=True, server_default=text("nextval('region_regionid_seq'::regclass)"))
    RegionDescription = Column(CHAR(8), nullable=False)


class Shipper(Base):
    __tablename__ = 'shippers'

    ShipperID = Column(SmallInteger, primary_key=True, server_default=text("nextval('shippers_shipperid_seq'::regclass)"))
    CompanyName = Column(String(40), nullable=False)
    Phone = Column(String(24))


class ShippersTmp(Base):
    __tablename__ = 'shippers_tmp'

    ShipperID = Column(SmallInteger, primary_key=True, server_default=text("nextval('shippers_tmp_shipperid_seq'::regclass)"))
    CompanyName = Column(String(40), nullable=False)
    Phone = Column(String(24))


class Supplier(Base):
    __tablename__ = 'suppliers'

    SupplierID = Column(SmallInteger, primary_key=True, server_default=text("nextval('suppliers_supplierid_seq'::regclass)"))
    CompanyName = Column(String(40), nullable=False)
    ContactName = Column(String(30))
    ContactTitle = Column(String(30))
    Address = Column(String(60))
    City = Column(String(15))
    Region = Column(String(15))
    PostalCode = Column(String(10))
    Country = Column(String(15))
    Phone = Column(String(24))
    Fax = Column(String(24))
    HomePage = Column(Text)


class Territory(Base):
    __tablename__ = 'territories'

    TerritoryID = Column(Integer, primary_key=True, server_default=text("nextval('territories_territoryid_seq'::regclass)"))
    TerritoryDescription = Column(CHAR(64), nullable=False)
    RegionID = Column(SmallInteger, nullable=False)


t_usstates = Table(
    'usstates', metadata,
    Column('StateID', SmallInteger, nullable=False, server_default=text("nextval('usstates_stateid_seq'::regclass)")),
    Column('StateName', String(100)),
    Column('StateAbbr', String(2)),
    Column('StateRegion', String(50))
)
