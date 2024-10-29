CREATE OR REPLACE FUNCTION STATIC_CONTENT.subcategory_insert_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if category exists
    IF NOT EXISTS (
        SELECT 1 
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = NEW.CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', NEW.CategoryID;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER subcategory_insert_trigger
BEFORE INSERT ON STATIC_CONTENT.sub_categories
FOR EACH ROW
EXECUTE PROCEDURE STATIC_CONTENT.subcategory_insert_trigger_func();


CREATE OR REPLACE PROCEDURE STATIC_CONTENT.update_subcategory(
    p_SubCategoryID INT,
    p_CategoryID INT,
    p_Name VARCHAR(100),
    p_Description TEXT
)
AS $$
BEGIN
    -- Check if category exists
    IF NOT EXISTS (
        SELECT 1
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = p_CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', p_CategoryID;
    END IF;

    UPDATE STATIC_CONTENT.sub_categories
    SET CategoryID = p_CategoryID,
        Name = p_Name,
        Description = p_Description
    WHERE SubCategoryID = p_SubCategoryID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE STATIC_CONTENT.delete_subcategory(
    p_SubCategoryID INT
)
AS $$
BEGIN
    DELETE FROM STATIC_CONTENT.sub_categories
    WHERE SubCategoryID = p_SubCategoryID;
END;
$$ LANGUAGE plpgsql;