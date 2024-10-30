/*==============================================================*/
/* SGBD:      POSTGRESSQL                                       */
/* Created on:     29/10/2024 04:03:37                          */
/*==============================================================*/
-- Create the database
CREATE DATABASE DB2_Pratic;
-- Connect to the database
\c DB2_Pratic;

CREATE OR REPLACE PROCEDURE remove_all_tables()
AS $$
DECLARE
    table_record RECORD;
    schema_record RECORD;
BEGIN
    FOR schema_record IN SELECT schema_name FROM information_schema.schemata
    LOOP
        FOR table_record IN SELECT table_name FROM information_schema.tables WHERE table_schema = schema_record.schema_name
        LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || schema_record.schema_name || '.' || table_record.table_name || ' CASCADE';
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Call the procedure to remove all tables
CALL remove_all_tables();

-- schema drops
DROP SCHEMA IF EXISTS SECURITY CASCADE;
DROP SCHEMA IF EXISTS HR CASCADE;
-- DROP SCHEMA IF EXISTS CONTROL CASCADE; --mongoDB
DROP SCHEMA IF EXISTS STATIC_CONTENT CASCADE;
DROP SCHEMA IF EXISTS DYNAMIC_CONTENT CASCADE;
DROP SCHEMA IF EXISTS TRANSACTIONS CASCADE;
-- DROP SCHEMA IF EXISTS PROMOS CASCADE;

 /** 
  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |     ______   | || |  ____  ____  | || |  _________   | || | ____    ____ | || |      __      | || |    _______   | |
| |   /  ___  |  | || |   .' ___  |  | || | |_   ||   _| | || | |_   ___  |  | || ||_   \  /   _|| || |     /  \     | || |   /  ___  |  | |
| |  |  (__ \_|  | || |  / .'   \_|  | || |   | |__| |   | || |   | |_  \_|  | || |  |   \/   |  | || |    / /\ \    | || |  |  (__ \_|  | |
| |   '.___`-.   | || |  | |         | || |   |  __  |   | || |   |  _|  _   | || |  | |\  /| |  | || |   / ____ \   | || |   '.___`-.   | |
| |  |`\____) |  | || |  \ `.___.'\  | || |  _| |  | |_  | || |  _| |___/ |  | || | _| |_\/_| |_ | || | _/ /    \ \_ | || |  |`\____) |  | |
| |  |_______.'  | || |   `._____.'  | || | |____||____| | || | |_________|  | || ||_____||_____|| || ||____|  |____|| || |  |_______.'  | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
 **/

-- Create the schemas
CREATE SCHEMA SECURITY;
CREATE SCHEMA HR;
CREATE SCHEMA CONTROL;
CREATE SCHEMA STATIC_CONTENT;
CREATE SCHEMA DYNAMIC_CONTENT;
CREATE SCHEMA TRANSACTIONS;
CREATE SCHEMA PROMOS;



-- */
/*
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.   
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |  
| |     ______   | || |  _______     | || |  _________   | || |      __      | || |  _________   | || |  _________   | |  
| |   .' ___  |  | || | |_   __ \    | || | |_   ___  |  | || |     /  \     | || | |  _   _  |  | || | |_   ___  |  | |  
| |  / .'   \_|  | || |   | |__) |   | || |   | |_  \_|  | || |    / /\ \    | || | |_/ | | \_|  | || |   | |_  \_|  | |  
| |  | |         | || |   |  __ /    | || |   |  _|  _   | || |   / ____ \   | || |     | |      | || |   |  _|  _   | |  
| |  \ `.___.'\  | || |  _| |  \ \_  | || |  _| |___/ |  | || | _/ /    \ \_ | || |    _| |_     | || |  _| |___/ |  | |  
| |   `._____.'  | || | |____| |___| | || | |_________|  | || ||____|  |____|| || |   |_____|    | || | |_________|  | |  
| |              | || |              | || |              | || |              | || |              | || |              | |  
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |  
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'   
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.   
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |  
| |  _________   | || |      __      | || |   ______     | || |   _____      | || |  _________   | || |    _______   | |  
| | |  _   _  |  | || |     /  \     | || |  |_   _ \    | || |  |_   _|     | || | |_   ___  |  | || |   /  ___  |  | |  
| | |_/ | | \_|  | || |    / /\ \    | || |    | |_) |   | || |    | |       | || |   | |_  \_|  | || |  |  (__ \_|  | |  
| |     | |      | || |   / ____ \   | || |    |  __'.   | || |    | |   _   | || |   |  _|  _   | || |   '.___`-.   | |  
| |    _| |_     | || | _/ /    \ \_ | || |   _| |__) |  | || |   _| |__/ |  | || |  _| |___/ |  | || |  |`\____) |  | |  
| |   |_____|    | || ||____|  |____|| || |  |_______/   | || |  |________|  | || | |_________|  | || |  |_______.'  | |  
| |              | || |              | || |              | || |              | || |              | || |              | |  
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |  
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
*/



-- SECURITY
CREATE TABLE SECURITY.User_Passwords_Dictionary (
    PasswordID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    HashedPassword VARCHAR(255),
    CreatedAt TIMESTAMP
);

-- HR
CREATE TABLE HR.Users (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Phone VARCHAR(20),
    Email VARCHAR(100) UNIQUE,
    HashedPassword VARCHAR(255),
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
    CONSTRAINT fk_user_address_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID)
);

CREATE TABLE HR.User_payment (
    PaymentMethodID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Payment_method VARCHAR(50),
    Provider VARCHAR(50),
    CardNumber VARCHAR(50),
    ExpiryDate DATE,
    Billing_AddressID INT,
    CONSTRAINT fk_user_payment_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID),
    CONSTRAINT fk_user_payment_addressid FOREIGN KEY (Billing_AddressID) REFERENCES HR.User_address(AddressID)
);

-- CONTROL - MONGODB
-- CREATE TABLE CONTROL.audit_log (
--     LogID SERIAL PRIMARY KEY,
--     RecordID INT NOT NULL,
--     Modified_by INT NOT NULL,
--     Field_Changed VARCHAR(100),
--     Old_value TEXT,
--     New_value TEXT,
--     Edit_type VARCHAR(50),
--     CONSTRAINT fk_audit_log_userid FOREIGN KEY (Modified_by) REFERENCES HR.Users(UserID)
-- );

-- STATIC_CONTENT
CREATE TABLE STATIC_CONTENT.Categories (
    CategoryID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT
);

CREATE TABLE STATIC_CONTENT.sub_categories (
    SubCategoryID SERIAL PRIMARY KEY,
    CategoryID INT NOT NULL,
    Name VARCHAR(100),
    Description TEXT,
    CONSTRAINT fk_subcategories_categoryid FOREIGN KEY (CategoryID) REFERENCES STATIC_CONTENT.Categories(CategoryID)
);

-- DYNAMIC_CONTENT
CREATE TABLE DYNAMIC_CONTENT.Products (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    BasePrice NUMERIC(10, 2),
    DiscountedPrice NUMERIC(10, 2),
    SKU VARCHAR(50) UNIQUE,
    ModelID INT,
    ProductSerialNumber VARCHAR(50),
    CategoryID INT
);

CREATE TABLE DYNAMIC_CONTENT.Stock (
    StockID SERIAL PRIMARY KEY,
    ProductID INT NOT NULL,
    Quantity INT,
    LastUpdated TIMESTAMP,
    CONSTRAINT fk_stock_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID)
);

-- CREATE TABLE DYNAMIC_CONTENT.Cart (
--     CartID SERIAL PRIMARY KEY,
--     UserID INT NOT NULL,
--     ProductID INT NOT NULL,
--     Quantity INT,
--     CreatedAt TIMESTAMP,
--     CONSTRAINT fk_cart_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID),
--     CONSTRAINT fk_cart_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID)
-- );

-- TRANSACTIONS
CREATE TABLE TRANSACTIONS.Orders (
    OrderID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    TransactionCode VARCHAR(50),
    Status VARCHAR(50),
    CartContentJSON JSON,
    CONSTRAINT fk_orders_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID)
);

CREATE TABLE TRANSACTIONS.Payments (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INT NOT NULL,
    UserID INT NOT NULL,
    PaymentMethod VARCHAR(50),
    PaymentStatus VARCHAR(50),
    Amount NUMERIC(10, 2),
    PaymentDate TIMESTAMP,
    CONSTRAINT fk_payments_orderid FOREIGN KEY (OrderID) REFERENCES TRANSACTIONS.Orders(OrderID),
    CONSTRAINT fk_payments_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID)
);

-- CREATE TABLE TRANSACTIONS.Reservations (
--     ReservationID SERIAL PRIMARY KEY,
--     UserID INT NOT NULL,
--     ReservationCode VARCHAR(50),
--     ProductID INT NOT NULL,
--     ReservationStatus VARCHAR(50),
--     CONSTRAINT fk_reservations_userid FOREIGN KEY (UserID) REFERENCES HR.Users(UserID),
--     CONSTRAINT fk_reservations_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID)
-- );

-- -- PROMOS
-- CREATE TABLE PROMOS.Promotions (
--     PromoID SERIAL PRIMARY KEY,
--     Code VARCHAR(50) UNIQUE,
--     Description TEXT,
--     DiscountAmount NUMERIC(10, 2),
--     DiscountPercentage DECIMAL(5, 2),
--     ValidUntil DATE,
--     ProductID INT,
--     CategoryID INT,
--     CONSTRAINT fk_promos_productid FOREIGN KEY (ProductID) REFERENCES DYNAMIC_CONTENT.Products(ProductID),
--     CONSTRAINT fk_promos_categoryid FOREIGN KEY (CategoryID) REFERENCES STATIC_CONTENT.Categories(CategoryID)
-- );
