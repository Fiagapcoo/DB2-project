-- PROCEDURE para remover todas as tabelas em schemas do usuário
CREATE OR REPLACE PROCEDURE remove_all_tables()
AS $$
DECLARE
    table_record RECORD;
    schema_record RECORD;
BEGIN
    FOR schema_record IN 
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1')
    LOOP
        FOR table_record IN 
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = schema_record.schema_name
        LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(schema_record.schema_name) || '.' || quote_ident(table_record.table_name) || ' CASCADE';
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Chamar a procedure para remover todas as tabelas
CALL remove_all_tables();

-- Remover schemas, se existirem
DROP SCHEMA IF EXISTS SECURITY CASCADE;
DROP SCHEMA IF EXISTS HR CASCADE;
DROP SCHEMA IF EXISTS CONTROL CASCADE;  -- MongoDB pode não precisar
DROP SCHEMA IF EXISTS STATIC_CONTENT CASCADE;
DROP SCHEMA IF EXISTS DYNAMIC_CONTENT CASCADE;
DROP SCHEMA IF EXISTS TRANSACTIONS CASCADE;
DROP SCHEMA IF EXISTS PROMOS CASCADE;

-- Criar os schemas
CREATE SCHEMA SECURITY;
CREATE SCHEMA HR;
CREATE SCHEMA CONTROL;
CREATE SCHEMA STATIC_CONTENT;
CREATE SCHEMA DYNAMIC_CONTENT;
CREATE SCHEMA TRANSACTIONS;
CREATE SCHEMA PROMOS;

-- Criar tabelas

-- SECURITY
CREATE TABLE SECURITY.User_Passwords_Dictionary (
    PasswordID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    HashedPassword VARCHAR(255),
    CreatedAt TIMESTAMP DEFAULT now()
);

-- HR
CREATE TABLE HR.Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(255) UNIQUE NOT NULL,
    HashedPassword VARCHAR(255) NOT NULL,
    ProfilePic VARCHAR(255),
    IsManager BOOLEAN DEFAULT FALSE
);

CREATE TABLE HR.User_address (
    AddressID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Address_line1 VARCHAR(255),
    Address_line2 VARCHAR(255),
    City VARCHAR(100),
    Postal_code VARCHAR(20),
    Country VARCHAR(50),
    Phone_number VARCHAR(20),
    CONSTRAINT fk_user_address_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID) ON DELETE CASCADE
);

CREATE TABLE HR.User_payment (
    PaymentMethodID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Payment_method VARCHAR(50),
    Provider VARCHAR(50),
    CardNumber VARCHAR(50),
    ExpiryDate DATE,
    Billing_AddressID INT,
    CONSTRAINT fk_user_payment_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_user_payment_addressid FOREIGN KEY (Billing_AddressID) REFERENCES HR.User_address(AddressID) ON DELETE SET NULL
);

-- STATIC_CONTENT
CREATE TABLE STATIC_CONTENT.Categories (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    preview_img VARCHAR(255) NOT NULL
);

CREATE TABLE STATIC_CONTENT.Sub_Categories (
    SubCategoryID SERIAL PRIMARY KEY,
    CategoryID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    CONSTRAINT fk_subcategories_categoryid FOREIGN KEY (CategoryID) REFERENCES STATIC_CONTENT.Categories(CategoryID) ON DELETE CASCADE
);

-- DYNAMIC_CONTENT
CREATE TABLE DYNAMIC_CONTENT.Products (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    BasePrice NUMERIC(10, 2) NOT NULL CHECK (BasePrice >= 0),
    DiscountedPrice NUMERIC(10, 2) CHECK (DiscountedPrice >= 0),
    SKU VARCHAR(50) UNIQUE,
    ModelID INT,
    ProductSerialNumber VARCHAR(50),
    CategoryID INT,
    ProductType VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    CONSTRAINT fk_products_categoryid FOREIGN KEY (CategoryID) REFERENCES STATIC_CONTENT.Categories(CategoryID) ON DELETE SET NULL
);

CREATE TABLE DYNAMIC_CONTENT.Stock (
    StockID SERIAL PRIMARY KEY,
    ProductID INT NOT NULL,
    Quantity INT CHECK (Quantity >= 0),
    LastUpdated TIMESTAMP DEFAULT now(),
    CONSTRAINT fk_stock_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID) ON DELETE CASCADE
);

-- TRANSACTIONS
CREATE TABLE TRANSACTIONS.Orders (
    OrderID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    TransactionCode VARCHAR(50) UNIQUE NOT NULL,
    Status VARCHAR(50) NOT NULL,
    CartContentJSON JSON NOT NULL,
    CONSTRAINT fk_orders_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID) ON DELETE CASCADE
);

CREATE TABLE TRANSACTIONS.Payments (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INT NOT NULL,
    UserID INT NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    PaymentStatus VARCHAR(50) NOT NULL,
    Amount NUMERIC(10, 2) NOT NULL CHECK (Amount >= 0),
    PaymentDate TIMESTAMP DEFAULT now(),
    CONSTRAINT fk_payments_orderid FOREIGN KEY (OrderID) REFERENCES TRANSACTIONS.Orders(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_payments_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID) ON DELETE CASCADE
);

-- PROMOS
CREATE TABLE PROMOS.Promotions (
    PromoID SERIAL PRIMARY KEY,
    Code VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT,
    DiscountAmount NUMERIC(10, 2) CHECK (DiscountAmount >= 0),
    DiscountPercentage DECIMAL(5, 2) CHECK (DiscountPercentage BETWEEN 0 AND 100),
    ValidUntil DATE,
    ProductID INT,
    CategoryID INT,
    CONSTRAINT fk_promos_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID) ON DELETE SET NULL,
    CONSTRAINT fk_promos_categoryid FOREIGN KEY (CategoryID) REFERENCES STATIC_CONTENT.Categories(CategoryID) ON DELETE SET NULL
);
