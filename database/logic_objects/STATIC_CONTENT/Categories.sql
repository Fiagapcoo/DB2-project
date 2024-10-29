CREATE OR REPLACE PROCEDURE STATIC_CONTENT.insert_category(
    p_Name VARCHAR(100),
    p_Description TEXT
)
AS $$
BEGIN
    INSERT INTO STATIC_CONTENT.Categories (
        Name,
        Description
    ) VALUES (
        p_Name,
        p_Description
    );
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE STATIC_CONTENT.update_category(
    p_CategoryID INT,
    p_Name VARCHAR(100),
    p_Description TEXT
)
AS $$
BEGIN
    UPDATE STATIC_CONTENT.Categories
    SET Name = p_Name,
        Description = p_Description
    WHERE CategoryID = p_CategoryID;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE STATIC_CONTENT.delete_category(
    p_CategoryID INT
)
AS $$
BEGIN
    DELETE FROM STATIC_CONTENT.Categories
    WHERE CategoryID = p_CategoryID;
END;
$$ LANGUAGE plpgsql;