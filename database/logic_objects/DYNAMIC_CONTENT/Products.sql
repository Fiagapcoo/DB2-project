CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.insert_product(
    p_Name VARCHAR(100),
    p_Description TEXT,
    p_BasePrice NUMERIC(10, 2),
    p_DiscountedPrice NUMERIC(10, 2),
    p_SKU VARCHAR(50),
    p_ModelID INT,
    p_ProductSerialNumber VARCHAR(50),
    p_CategoryID INT
)
AS $$
BEGIN
    -- Check if category exists
    IF NOT EXISTS (
        SELECT 1
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = p_CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', p_CategoryID;
    END IF;

    -- Insert the new product
    INSERT INTO DYNAMIC_CONTENT.Products (
        Name,
        Description,
        BasePrice,
        DiscountedPrice,
        SKU,
        ModelID,
        ProductSerialNumber,
        CategoryID
    ) VALUES (
        p_Name,
        p_Description,
        p_BasePrice,
        p_DiscountedPrice,
        p_SKU,
        p_ModelID,
        p_ProductSerialNumber,
        p_CategoryID
    );
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.update_product(
    p_ProductID INT,
    p_Name VARCHAR(100),
    p_Description TEXT,
    p_BasePrice NUMERIC(10, 2),
    p_DiscountedPrice NUMERIC(10, 2),
    p_SKU VARCHAR(50),
    p_ModelID INT,
    p_ProductSerialNumber VARCHAR(50),
    p_CategoryID INT
)
AS $$
BEGIN
    -- Check if category exists
    IF NOT EXISTS (
        SELECT 1
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = p_CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', p_CategoryID;
    END IF;

    -- Update the product
    UPDATE DYNAMIC_CONTENT.Products
    SET Name = p_Name,
        Description = p_Description,
        BasePrice = p_BasePrice,
        DiscountedPrice = p_DiscountedPrice,
        SKU = p_SKU,
        ModelID = p_ModelID,
        ProductSerialNumber = p_ProductSerialNumber,
        CategoryID = p_CategoryID
    WHERE ProductID = p_ProductID;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.delete_product(
    p_ProductID INT
)
AS $$
BEGIN
    DELETE FROM DYNAMIC_CONTENT.Products
    WHERE ProductID = p_ProductID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_stock_on_product_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert a new stock entry with quantity 1 for the new product
    INSERT INTO dynamic_content.stock (productid, quantity)
    VALUES (NEW.productid, 1);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER product_insert_trigger
AFTER INSERT ON dynamic_content.products
FOR EACH ROW
EXECUTE FUNCTION create_stock_on_product_insert();