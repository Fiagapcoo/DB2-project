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





CREATE OR REPLACE FUNCTION is_user_manager(p_userid INT) 
RETURNS BOOLEAN AS $$
DECLARE 
    manager_status BOOLEAN;
BEGIN
    SELECT ismanager INTO manager_status
    FROM hr.users
    WHERE userid = p_userid;

    RETURN manager_status;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION HR.get_userid_by_email(
    p_email VARCHAR(255)
)
RETURNS INT AS
$$
DECLARE
    v_UserID INT;
BEGIN

    SELECT UserID
    INTO v_UserID
    FROM HR.Users
    WHERE Email = p_email;


    RETURN v_UserID;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'No user found with email: %', p_email;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION HR.get_user_details_by_email(
    p_email VARCHAR(255)
)
RETURNS TABLE (
    UserID INT,
    Name VARCHAR(100),
    Email VARCHAR(255),
    HashedPassword VARCHAR(255)
) AS
$$
BEGIN
    RETURN QUERY
    SELECT u.UserID, u.Name, u.Email, u.HashedPassword
    FROM HR.Users u
    WHERE u.Email = p_email;
END;
$$
LANGUAGE plpgsql;