CREATE OR REPLACE FUNCTION HR.user_address_insert_trigger_func()
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

CREATE TRIGGER user_address_insert_trigger
BEFORE INSERT ON HR.User_address
FOR EACH ROW
EXECUTE PROCEDURE HR.user_address_insert_trigger_func();



CREATE OR REPLACE PROCEDURE HR.update_user_address(
    p_AddressID INT,
    p_Address_line1 VARCHAR(255),
    p_Address_line2 VARCHAR(255),
    p_City VARCHAR(100),
    p_Postal_code VARCHAR(20),
    p_Country VARCHAR(50),
    p_Phone_number VARCHAR(20)
)
AS $$
BEGIN
    UPDATE HR.User_address
    SET Address_line1 = p_Address_line1,
        Address_line2 = p_Address_line2,
        City = p_City,
        Postal_code = p_Postal_code,
        Country = p_Country,
        Phone_number = p_Phone_number
    WHERE AddressID = p_AddressID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE HR.delete_user_address(
    p_AddressID INT
)
AS $$
BEGIN
    DELETE FROM HR.User_address
    WHERE AddressID = p_AddressID;
END;
$$ LANGUAGE plpgsql;