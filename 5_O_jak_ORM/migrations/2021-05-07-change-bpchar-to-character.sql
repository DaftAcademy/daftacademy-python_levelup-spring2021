ALTER TABLE customercustomerdemo
ALTER COLUMN "CustomerID" TYPE character(6),
ALTER COLUMN "CustomerTypeID" TYPE character(6);

ALTER TABLE customerdemographics
ALTER COLUMN "CustomerTypeID" TYPE character(6);

ALTER TABLE customers
ALTER COLUMN "CustomerID" TYPE character(6);

ALTER TABLE orders
ALTER COLUMN "CustomerID" TYPE character(6);

ALTER TABLE region
ALTER COLUMN "RegionDescription" TYPE character(8);

ALTER TABLE territories
ALTER COLUMN "TerritoryDescription" TYPE character(64);
