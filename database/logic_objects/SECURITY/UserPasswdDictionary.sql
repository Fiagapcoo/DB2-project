CREATE OR REPLACE FUNCTION HR.user_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
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
AFTER INSERT OR UPDATE ON HR.Users
FOR EACH ROW
EXECUTE FUNCTION HR.user_insert_trigger_func();