CREATE OR REPLACE FUNCTION HR.user_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert new user password into the dictionary
    INSERT INTO SECURITY.User_Passwords_Dictionary (
        UserID,
        HashedPassword,
        CreatedAt
    ) VALUES (
        NEW.UserID,
        NEW.HashedPassword,
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_insert_trigger
AFTER INSERT ON HR.Users
FOR EACH ROW
EXECUTE PROCEDURE HR.user_insert_trigger_func();


CREATE OR REPLACE PROCEDURE HR.update_user(
    p_UserID INT,
    p_Name VARCHAR(100),
    p_Phone VARCHAR(20),
    p_Email VARCHAR(100),
    p_HashedPassword VARCHAR(255),
    p_ProfilePic VARCHAR(255),
    p_IsManager BOOLEAN
)
AS $$
BEGIN
    UPDATE HR.Users
    SET Name = p_Name,
        Phone = p_Phone,
        Email = p_Email,
        HashedPassword = p_HashedPassword,
        ProfilePic = p_ProfilePic,
        IsManager = p_IsManager
    WHERE UserID = p_UserID;

    -- Update the user's password in the dictionary
    UPDATE SECURITY.User_Passwords_Dictionary
    SET HashedPassword = p_HashedPassword,
        CreatedAt = CURRENT_TIMESTAMP
    WHERE UserID = p_UserID
    ORDER BY CreatedAt DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE HR.delete_user(
    p_UserID INT
)
AS $$
BEGIN
    -- Delete user's password entries from the dictionary
    DELETE FROM SECURITY.User_Passwords_Dictionary
    WHERE UserID = p_UserID;

    -- Delete the user
    DELETE FROM HR.Users
    WHERE UserID = p_UserID;
END;
$$ LANGUAGE plpgsql;