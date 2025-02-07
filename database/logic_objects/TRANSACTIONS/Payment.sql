CREATE OR REPLACE FUNCTION get_payment_method_totals()
RETURNS TABLE (payment_method VARCHAR, total_amount NUMERIC(10, 2)) AS $$
DECLARE
    payment_cursor CURSOR FOR
        SELECT PaymentMethod, SUM(Amount) AS total_amount
        FROM TRANSACTIONS.Payments
        GROUP BY PaymentMethod;
BEGIN
    OPEN payment_cursor;


    LOOP
        FETCH payment_cursor INTO payment_method, total_amount;
        EXIT WHEN NOT FOUND;
        RETURN NEXT;
    END LOOP;

    CLOSE payment_cursor;
END;
$$ LANGUAGE plpgsql;