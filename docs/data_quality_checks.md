# Data Quality Checks — Stage 3

## Primary key checks

| table                            | pk                           |   rows |   null_keys |   dup_keys |   distinct_keys |
|:---------------------------------|:-----------------------------|-------:|------------:|-----------:|----------------:|
| olist_customers_dataset.csv      | customer_id                  |  99441 |           0 |          0 |           99441 |
| olist_orders_dataset.csv         | order_id                     |  99441 |           0 |          0 |           99441 |
| olist_order_items_dataset.csv    | order_id, order_item_id      | 112650 |           0 |          0 |          112650 |
| olist_order_payments_dataset.csv | order_id, payment_sequential | 103886 |           0 |          0 |          103886 |
| olist_order_reviews_dataset.csv  | review_id                    |  99224 |           0 |        814 |           98410 |
| olist_products_dataset.csv       | product_id                   |  32951 |           0 |          0 |           32951 |
| olist_sellers_dataset.csv        | seller_id                    |   3095 |           0 |          0 |            3095 |

## Foreign key checks

| child_table                      | parent_table                | fk                                                                                |   child_nonnull_keys |   missing_in_parent |   missing_rate |
|:---------------------------------|:----------------------------|:----------------------------------------------------------------------------------|---------------------:|--------------------:|---------------:|
| olist_orders_dataset.csv         | olist_customers_dataset.csv | olist_orders_dataset.csv.customer_id -> olist_customers_dataset.csv.customer_id   |                99441 |                   0 |              0 |
| olist_order_items_dataset.csv    | olist_orders_dataset.csv    | olist_order_items_dataset.csv.order_id -> olist_orders_dataset.csv.order_id       |               112650 |                   0 |              0 |
| olist_order_payments_dataset.csv | olist_orders_dataset.csv    | olist_order_payments_dataset.csv.order_id -> olist_orders_dataset.csv.order_id    |               103886 |                   0 |              0 |
| olist_order_reviews_dataset.csv  | olist_orders_dataset.csv    | olist_order_reviews_dataset.csv.order_id -> olist_orders_dataset.csv.order_id     |                99224 |                   0 |              0 |
| olist_order_items_dataset.csv    | olist_products_dataset.csv  | olist_order_items_dataset.csv.product_id -> olist_products_dataset.csv.product_id |               112650 |                   0 |              0 |
| olist_order_items_dataset.csv    | olist_sellers_dataset.csv   | olist_order_items_dataset.csv.seller_id -> olist_sellers_dataset.csv.seller_id    |               112650 |                   0 |              0 |

## Notes
- Null cells in reviews and delivery timestamps are expected; downstream KPIs must filter appropriately.
- Geolocation duplicates will be resolved via a ZIP-prefix aggregation in modelling/staging.
