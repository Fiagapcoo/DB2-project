CREATE OR REPLACE FUNCTION TRANSACTIONS.insert_order(
    p_UserID INT,
    p_TransactionCode VARCHAR(50),
    p_CartContentJSON JSON
)
RETURNS INT AS
$$
DECLARE
    v_OrderID INT;
BEGIN

    INSERT INTO TRANSACTIONS.Orders (UserID, TransactionCode, Status, CartContentJSON)
    VALUES (p_UserID, p_TransactionCode, 'Pending', p_CartContentJSON)
    RETURNING OrderID INTO v_OrderID;


    RETURN v_OrderID;
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'TransactionCode must be unique';
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'UserID does not exist in HR.Users';
END;
$$
LANGUAGE plpgsql;