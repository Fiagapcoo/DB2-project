CREATE OR REPLACE VIEW dynamic_content.instrument_products_with_stock AS
SELECT 
    p.*, 
    s.stockid, 
    s.quantity, 
    s.lastupdated
FROM 
    dynamic_content.products p
JOIN 
    dynamic_content.stock s 
ON 
    s.productid = p.productid
WHERE 
    p.producttype = 'instrument';


CREATE OR REPLACE VIEW dynamic_content.latest_products_by_brand AS
SELECT DISTINCT ON (b.brandid)
    b.brandid,
    b.brandname
FROM 
    dynamic_content.products p
JOIN 
    dynamic_content.brands b ON p.brandid = b.brandid
ORDER BY 
    b.brandid, p.productid DESC;

CREATE OR REPLACE VIEW dynamic_content.product_price_range AS
SELECT 
    MIN(COALESCE(discountedprice, baseprice)) AS min_price,
    MAX(COALESCE(discountedprice, baseprice)) AS max_price
FROM (
    SELECT discountedprice, baseprice 
    FROM dynamic_content.products 
    ORDER BY productid DESC 
    LIMIT 20
) AS subquery;