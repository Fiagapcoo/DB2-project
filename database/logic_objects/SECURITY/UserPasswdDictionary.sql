CREATE OR REPLACE FUNCTION HR.user_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Inserir uma nova entrada sempre que um usuário for inserido ou sua senha for atualizada
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

-- Create the trigger
CREATE TRIGGER user_insert_trigger
AFTER INSERT OR UPDATE ON HR.Users
FOR EACH ROW
EXECUTE FUNCTION HR.user_insert_trigger_func();