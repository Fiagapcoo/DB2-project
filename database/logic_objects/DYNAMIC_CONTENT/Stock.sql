CREATE OR REPLACE FUNCTION DYNAMIC_CONTENT.stock_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if product exists
    IF NOT EXISTS (
        SELECT 1
        FROM DYNAMIC_CONTENT.Products
        WHERE ProductID = NEW.ProductID
    ) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', NEW.ProductID;
    END IF;

    -- Set the LastUpdated timestamp
    NEW.LastUpdated := CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER stock_insert_trigger
BEFORE INSERT ON DYNAMIC_CONTENT.Stock
FOR EACH ROW
EXECUTE PROCEDURE DYNAMIC_CONTENT.stock_insert_trigger_func();



CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.update_stock(
    p_StockID INT,
    p_Quantity INT
)
AS $$
BEGIN
    UPDATE DYNAMIC_CONTENT.Stock
    SET Quantity = p_Quantity,
        LastUpdated = CURRENT_TIMESTAMP
    WHERE StockID = p_StockID;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.delete_stock(
    p_StockID INT
)
AS $$
BEGIN
    DELETE FROM DYNAMIC_CONTENT.Stock
    WHERE StockID = p_StockID;
END;
$$ LANGUAGE plpgsql;
