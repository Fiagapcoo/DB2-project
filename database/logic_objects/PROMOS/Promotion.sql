CREATE OR REPLACE PROCEDURE PROMOS.insert_promotion(
    p_Code VARCHAR(50),
    p_Description TEXT,
    p_DiscountAmount NUMERIC(10, 2),
    p_DiscountPercentage DECIMAL(5, 2),
    p_ValidUntil DATE,
    p_ProductID INT,
    p_CategoryID INT
)
AS $$
BEGIN
    -- Check if product exists (if specified)
    IF p_ProductID IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM DYNAMIC_CONTENT.Products
        WHERE ProductID = p_ProductID
    ) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', p_ProductID;
    END IF;

    -- Check if category exists (if specified)
    IF p_CategoryID IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = p_CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', p_CategoryID;
    END IF;

    -- Insert the new promotion
    INSERT INTO PROMOS.Promotions (
        Code,
        Description,
        DiscountAmount,
        DiscountPercentage,
        ValidUntil,
        ProductID,
        CategoryID
    ) VALUES (
        p_Code,
        p_Description,
        p_DiscountAmount,
        p_DiscountPercentage,
        p_ValidUntil,
        p_ProductID,
        p_CategoryID
    );
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE PROCEDURE PROMOS.update_promotion(
    p_PromoID INT,
    p_Code VARCHAR(50),
    p_Description TEXT,
    p_DiscountAmount NUMERIC(10, 2),
    p_DiscountPercentage DECIMAL(5, 2),
    p_ValidUntil DATE,
    p_ProductID INT,
    p_CategoryID INT
)
AS $$
BEGIN
    -- Check if product exists (if specified)
    IF p_ProductID IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM DYNAMIC_CONTENT.Products
        WHERE ProductID = p_ProductID
    ) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', p_ProductID;
    END IF;

    -- Check if category exists (if specified)
    IF p_CategoryID IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM STATIC_CONTENT.Categories
        WHERE CategoryID = p_CategoryID
    ) THEN
        RAISE EXCEPTION 'Category with ID % does not exist', p_CategoryID;
    END IF;

    -- Update the promotion
    UPDATE PROMOS.Promotions
    SET Code = p_Code,
        Description = p_Description,
        DiscountAmount = p_DiscountAmount,
        DiscountPercentage = p_DiscountPercentage,
        ValidUntil = p_ValidUntil,
        ProductID = p_ProductID,
        CategoryID = p_CategoryID
    WHERE PromoID = p_PromoID;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE PROMOS.delete_promotion(
    p_PromoID INT
)
AS $$
BEGIN
    DELETE FROM PROMOS.Promotions
    WHERE PromoID = p_PromoID;
END;
$$ LANGUAGE plpgsql;