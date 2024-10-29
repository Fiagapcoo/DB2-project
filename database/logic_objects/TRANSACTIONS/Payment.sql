CREATE OR REPLACE FUNCTION TRANSACTIONS.payment_insert_trigger_func()
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

    -- Check if order exists
    IF NOT EXISTS (
        SELECT 1
        FROM TRANSACTIONS.Orders
        WHERE OrderID = NEW.OrderID
    ) THEN
        RAISE EXCEPTION 'Order with ID % does not exist', NEW.OrderID;
    END IF;

    -- Set the PaymentDate timestamp
    NEW.PaymentDate := CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER payment_insert_trigger
BEFORE INSERT ON TRANSACTIONS.Payments
FOR EACH ROW
EXECUTE PROCEDURE TRANSACTIONS.payment_insert_trigger_func();



CREATE OR REPLACE PROCEDURE TRANSACTIONS.update_payment(
    p_PaymentID INT,
    p_PaymentStatus VARCHAR(50),
    p_Amount NUMERIC(10, 2)
)
AS $$
BEGIN
    UPDATE TRANSACTIONS.Payments
    SET PaymentStatus = p_PaymentStatus,
        Amount = p_Amount
    WHERE PaymentID = p_PaymentID;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE TRANSACTIONS.delete_payment(
    p_PaymentID INT
)
AS $$
BEGIN
    DELETE FROM TRANSACTIONS.Payments
    WHERE PaymentID = p_PaymentID;
END;
$$ LANGUAGE plpgsql;