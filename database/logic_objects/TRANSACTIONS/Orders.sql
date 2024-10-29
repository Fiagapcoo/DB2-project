CREATE OR REPLACE FUNCTION TRANSACTIONS.order_insert_trigger_func()
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

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_insert_trigger
BEFORE INSERT ON TRANSACTIONS.Orders
FOR EACH ROW
EXECUTE PROCEDURE TRANSACTIONS.order_insert_trigger_func();


CREATE OR REPLACE PROCEDURE TRANSACTIONS.update_order(
    p_OrderID INT,
    p_Status VARCHAR(50),
    p_CartContentJSON JSON
)
AS $$
BEGIN
    UPDATE TRANSACTIONS.Orders
    SET Status = p_Status,
        CartContentJSON = p_CartContentJSON
    WHERE OrderID = p_OrderID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE TRANSACTIONS.delete_order(
    p_OrderID INT
)
AS $$
BEGIN
    DELETE FROM TRANSACTIONS.Orders
    WHERE OrderID = p_OrderID;
END;
$$ LANGUAGE plpgsql;