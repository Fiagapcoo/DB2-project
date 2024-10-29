CREATE OR REPLACE FUNCTION TRANSACTIONS.reservation_insert_trigger_func()
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

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER reservation_insert_trigger
BEFORE INSERT ON TRANSACTIONS.Reservations
FOR EACH ROW
EXECUTE PROCEDURE TRANSACTIONS.reservation_insert_trigger_func();

CREATE OR REPLACE PROCEDURE TRANSACTIONS.update_reservation(
    p_ReservationID INT,
    p_ReservationStatus VARCHAR(50)
)
AS $$
BEGIN
    UPDATE TRANSACTIONS.Reservations
    SET ReservationStatus = p_ReservationStatus
    WHERE ReservationID = p_ReservationID;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE TRANSACTIONS.delete_reservation(
    p_ReservationID INT
)
AS $$
BEGIN
    DELETE FROM TRANSACTIONS.Reservations
    WHERE ReservationID = p_ReservationID;
END;
$$ LANGUAGE plpgsql;