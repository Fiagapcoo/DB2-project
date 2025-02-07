CREATE OR REPLACE VIEW static_content.categories_with_instruments AS
SELECT 
    c.*
FROM 
    static_content.categories c
WHERE 
    EXISTS (
        SELECT 1 
        FROM dynamic_content.products p 
        WHERE p.categoryid = c.categoryid 
        AND p.producttype = 'instrument'
    );