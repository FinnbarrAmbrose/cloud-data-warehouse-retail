CREATE OR REPLACE TABLE `web-analytics-funnel.olist_warehouse_us.mart_customer_performance` AS
WITH customer_fact AS (
  SELECT
    customer_key,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    SUM(COALESCE(item_price, 0)) AS total_revenue,
    SUM(COALESCE(freight_value, 0)) AS total_freight,
    MIN(order_purchase_timestamp) AS first_order_ts,
    MAX(order_purchase_timestamp) AS last_order_ts
  FROM `web-analytics-funnel.olist_warehouse_us.fact_order_item`
  GROUP BY customer_key
)
SELECT
  c.customer_key,
  c.customer_unique_id,
  c.zip_code_prefix,
  c.customer_city,
  c.customer_state,

  COALESCE(f.total_orders, 0) AS total_orders,
  COALESCE(f.total_items, 0) AS total_items,
  COALESCE(f.total_revenue, 0) AS total_revenue,
  COALESCE(f.total_freight, 0) AS total_freight,
  SAFE_DIVIDE(COALESCE(f.total_revenue, 0), NULLIF(COALESCE(f.total_orders, 0), 0)) AS avg_order_value,

  f.first_order_ts,
  f.last_order_ts
FROM `web-analytics-funnel.olist_warehouse_us.dim_customer` c
LEFT JOIN customer_fact f
USING (customer_key);
