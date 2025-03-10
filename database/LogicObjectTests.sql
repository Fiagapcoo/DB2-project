-- Views
SELECT * FROM dynamic_content.instrument_products_with_stock
SELECT * FROM dynamic_content.latest_products_by_brand;
SELECT * FROM dynamic_content.product_price_range;
SELECT * FROM static_content.categories_with_instruments;
--Procedures
CALL HR.InsertUser('Nome Completo', '911111111', 'email@example.com', 'sUpErSeCrEtPaSsWoRd123=', FALSE)
-- Functions
SELECT CONTROL.insert_codigo_recuperacao(1, 123)
SELECT CONTROL.delete_codigos_recuperacao(1)
SELECT is_user_manager(1)
SELECT * FROM HR.get_user_details_by_email('email@example.com');
SELECT HR.get_userid_by_email('email@example.com');
SELECT TRANSACTIONS.insert_order(1, 'TX653', '{"items": [{"product_id": 23, "quantity": 1}]}');
-- Triggers
-- Não  é possivel demonstrar triggers num script SQL já que são autmáticamente executados pela base de dados

--Cursors
SELECT * FROM get_order_status_data();
select * from get_payment_method_totals();