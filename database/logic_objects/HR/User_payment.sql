CREATE OR REPLACE FUNCTION HR.user_payment_insert_trigger_func()
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

    -- Check if billing address exists
    IF NOT EXISTS (
        SELECT 1
        FROM HR.User_address
        WHERE AddressID = NEW.Billing_AddressID
    ) THEN
        RAISE EXCEPTION 'Billing address with ID % does not exist', NEW.Billing_AddressID;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_payment_insert_trigger
BEFORE INSERT ON HR.User_payment
FOR EACH ROW
EXECUTE PROCEDURE HR.user_payment_insert_trigger_func();



CREATE OR REPLACE PROCEDURE HR.update_user_payment(
    p_PaymentMethodID INT,
    p_Payment_method VARCHAR(50),
    p_Provider VARCHAR(50),
    p_CardNumber VARCHAR(50),
    p_ExpiryDate DATE,
    p_Billing_AddressID INT
)
AS $$
BEGIN
    -- Check if billing address exists
    IF NOT EXISTS (
        SELECT 1
        FROM HR.User_address
        WHERE AddressID = p_Billing_AddressID
    ) THEN
        RAISE EXCEPTION 'Billing address with ID % does not exist', p_Billing_AddressID;
    END IF;

    UPDATE HR.User_payment
    SET Payment_method = p_Payment_method,
        Provider = p_Provider,
        CardNumber = p_CardNumber,
        ExpiryDate = p_ExpiryDate,
        Billing_AddressID = p_Billing_AddressID
    WHERE PaymentMethodID = p_PaymentMethodID;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE HR.delete_user_payment(
    p_PaymentMethodID INT
)
AS $$
BEGIN
    DELETE FROM HR.User_payment
    WHERE PaymentMethodID = p_PaymentMethodID;
END;
$$ LANGUAGE plpgsql;