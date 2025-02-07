CREATE OR REPLACE PROCEDURE HR.InsertUser(
    p_Name VARCHAR(100),
    p_Phone VARCHAR(20),
    p_Email VARCHAR(100),
    p_HashedPassword VARCHAR(255),
    p_IsManager BOOLEAN = FALSE
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO HR.Users (
        Name, 
        Phone, 
        Email, 
        HashedPassword,
        IsManager
    )
    VALUES (
        p_Name,
        p_Phone,
        p_Email,
        p_HashedPassword,
        p_IsManager
    );
END;
$$;


CREATE OR REPLACE FUNCTION HR.user_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert or update user password into the dictionary
    INSERT INTO SECURITY.User_Passwords_Dictionary (
        UserID,
        HashedPassword,
        CreatedAt
    ) VALUES (
        NEW.UserID,
        NEW.HashedPassword,
        CURRENT_TIMESTAMP
    )
    ON CONFLICT (UserID) DO UPDATE 
    SET HashedPassword = EXCLUDED.HashedPassword, 
        CreatedAt = CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER user_insert_trigger
AFTER INSERT OR UPDATE ON HR.Users
FOR EACH ROW
EXECUTE FUNCTION HR.user_insert_trigger_func();


CREATE OR REPLACE FUNCTION is_user_manager(p_userid INT) 
RETURNS BOOLEAN AS $$
DECLARE 
    manager_status BOOLEAN;
BEGIN
    SELECT ismanager INTO manager_status
    FROM hr.user
    WHERE userid = p_userid;

    RETURN manager_status;
END;
$$ LANGUAGE plpgsql;


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


CREATE OR REPLACE FUNCTION HR.can_user_login(p_email VARCHAR(65535), p_hashed_password VARCHAR(65535))
RETURNS BOOLEAN AS $$
DECLARE
    db_hashed_password VARCHAR(65535);
BEGIN
    SELECT HashedPassword INTO db_hashed_password
    FROM HR.Users
    WHERE Email = p_email;

    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;

    IF p_hashed_password = db_hashed_password THEN
        RETURN TRUE; 
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;
