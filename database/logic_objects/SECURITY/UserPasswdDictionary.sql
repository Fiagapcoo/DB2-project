CREATE OR REPLACE FUNCTION SECURITY.user_password_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure password is not a common dictionary password
    IF EXISTS (
        SELECT 1 
        FROM SECURITY.Password_Blacklist 
        WHERE HashedPassword = NEW.HashedPassword
    ) THEN
        RAISE EXCEPTION 'Password is on the blacklist and cannot be used.';
    END IF;

    -- Log the new password
    INSERT INTO SECURITY.User_Passwords_Dictionary (
        UserID, 
        HashedPassword,
        CreatedAt
    ) VALUES (
        NEW.UserID,
        NEW.HashedPassword,
        NEW.CreatedAt
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_password_insert_trigger
BEFORE INSERT ON SECURITY.User_Passwords_Dictionary
FOR EACH ROW
EXECUTE PROCEDURE SECURITY.user_password_insert_trigger_func();



CREATE OR REPLACE PROCEDURE SECURITY.update_user_password(
    p_UserID INT,
    p_NewPassword VARCHAR(255)
)
AS $$
BEGIN
    -- Ensure password is not a common dictionary password
    IF EXISTS (
        SELECT 1 
        FROM SECURITY.Password_Blacklist
        WHERE HashedPassword = SHA256(p_NewPassword)
    ) THEN
        RAISE EXCEPTION 'Password is on the blacklist and cannot be used.';
    END IF;

    -- Update the user's password
    UPDATE SECURITY.User_Passwords_Dictionary
    SET HashedPassword = SHA256(p_NewPassword),
        CreatedAt = CURRENT_TIMESTAMP
    WHERE UserID = p_UserID
    ORDER BY CreatedAt DESC
    LIMIT 1;

    -- Log the password change
    INSERT INTO SECURITY.User_Passwords_Dictionary (
        UserID,
        HashedPassword,
        CreatedAt
    ) VALUES (
        p_UserID,
        SHA256(p_NewPassword),
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE SECURITY.delete_user_password(
    p_PasswordID INT
)
AS $$
BEGIN
    DELETE FROM SECURITY.User_Passwords_Dictionary
    WHERE PasswordID = p_PasswordID;
END;
$$ LANGUAGE plpgsql;


-- CALL SECURITY.update_user_password(__VALUE1__, 'VALUE2__');

-- CALL SECURITY.delete_user_password(__VALUE__);