CREATE OR REPLACE FUNCTION DYNAMIC_CONTENT.cart_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if user exists
    IF NOT EXISTS (
        SELECT 1
        FROM HR.Users
        WHERE UserID = NEW.UserID
    ) THEN
        RAISE EXCEPTION 'User with ID % does not exist', NEW.UserID;
    END IF;

    -- Check if product exists
    IF NOT EXISTS (
        SELECT 1
        FROM DYNAMIC_CONTENT.Products
        WHERE ProductID = NEW.ProductID
    ) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', NEW.ProductID;
    END IF;

    -- Set the CreatedAt timestamp
    NEW.CreatedAt := CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER cart_insert_trigger
BEFORE INSERT ON DYNAMIC_CONTENT.Cart
FOR EACH ROW
EXECUTE PROCEDURE DYNAMIC_CONTENT.cart_insert_trigger_func();


CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.update_cart_item(
    p_CartID INT,
    p_Quantity INT
)
AS $$
BEGIN
    UPDATE DYNAMIC_CONTENT.Cart
    SET Quantity = p_Quantity
    WHERE CartID = p_CartID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE DYNAMIC_CONTENT.delete_cart_item(
    p_CartID INT
)
AS $$
BEGIN
    DELETE FROM DYNAMIC_CONTENT.Cart
    WHERE CartID = p_CartID;
END;
$$ LANGUAGE plpgsql;