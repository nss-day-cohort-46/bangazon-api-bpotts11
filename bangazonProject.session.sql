SELECT *
FROM bangazonapi_order o
    JOIN bangazonapi_customer c ON o.customer_id = c.id
    JOIN bangazonapi_orderproduct op ON o.id = op.order_id
    JOIN bangazonapi_product p ON p.id = op.product_id