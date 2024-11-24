-- 2. Check mutable view


-- Success: Update one record
UPDATE VIEW_LONG_PRODUCTION_PRODUCTS
SET TITLE = 'Updated Device'
WHERE ID = 3;


-- Success: Insert new record
INSERT INTO VIEW_LONG_PRODUCTION_PRODUCTS (TITLE, AVERAGE_PRODUCTION_TIME)
VALUES ('New Product', 12);


-- Failure: Insert a new record even if the average production time < 10
INSERT INTO VIEW_LONG_PRODUCTION_PRODUCTS (TITLE, AVERAGE_PRODUCTION_TIME)
VALUES ('New Product', 2);
