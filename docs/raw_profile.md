# Raw Profile — Olist Dataset

## Files, row counts, and columns

### olist_customers_dataset.csv
- Rows: 99441
- Columns (5): customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state

### olist_geolocation_dataset.csv
- Rows: 1000163
- Columns (5): geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state

### olist_order_items_dataset.csv
- Rows: 112650
- Columns (7): order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value

### olist_order_payments_dataset.csv
- Rows: 103886
- Columns (5): order_id, payment_sequential, payment_type, payment_installments, payment_value

### olist_order_reviews_dataset.csv
- Rows: 99224
- Columns (7): review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp

### olist_orders_dataset.csv
- Rows: 99441
- Columns (8): order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date

### olist_products_dataset.csv
- Rows: 32951
- Columns (9): product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm

### olist_sellers_dataset.csv
- Rows: 3095
- Columns (4): seller_id, seller_zip_code_prefix, seller_city, seller_state

### product_category_name_translation.csv
- Rows: 71
- Columns (2): product_category_name, product_category_name_english
