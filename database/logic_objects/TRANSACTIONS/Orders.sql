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



CREATE OR REPLACE FUNCTION get_order_status_data()
RETURNS TABLE (order_status VARCHAR, order_count BIGINT) AS $$
DECLARE
    status_cursor CURSOR FOR
        SELECT o.Status, COUNT(*) AS count
        FROM TRANSACTIONS.Orders o
        WHERE o.Status IN ('Completed', 'Pending')
        GROUP BY o.Status;
BEGIN
    OPEN status_cursor;
    
    LOOP
        FETCH status_cursor INTO order_status, order_count;
        EXIT WHEN NOT FOUND;
        RETURN NEXT;
    END LOOP;

    CLOSE status_cursor;
END;
$$ LANGUAGE plpgsql;