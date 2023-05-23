BEGIN;

UPDATE eshop_order
SET user_id = 63,
    product_id = 17,
    quantity = 1000,
    ordered = 1,
    ordered_date = '2023-05-10 18:33:23.046468',
    commentaire = 'Commentaire lors d''une transaction'
WHERE id = 49;

COMMIT;
