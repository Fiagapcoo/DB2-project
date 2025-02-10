CREATE OR REPLACE FUNCTION create_stock_on_product_insert()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO dynamic_content.stock (productid, quantity)
    VALUES (NEW.productid, 1);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER product_insert_trigger
AFTER INSERT ON dynamic_content.products
FOR EACH ROW
EXECUTE FUNCTION create_stock_on_product_insert();