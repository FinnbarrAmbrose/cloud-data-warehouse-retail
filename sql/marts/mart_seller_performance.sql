CREATE OR REPLACE TABLE `web-analytics-funnel.olist_warehouse_us.mart_seller_performance` AS
WITH seller_fact AS (
  SELECT
    seller_key,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    SUM(COALESCE(item_price, 0)) AS total_revenue,
    SUM(COALESCE(freight_value, 0)) AS total_freight,
    COUNTIF(order_status = 'delivered') AS delivered_items,
    COUNTIF(order_status = 'canceled')  AS cancelled_items
  FROM `web-analytics-funnel.olist_warehouse_us.fact_order_item`
  GROUP BY seller_key
)
SELECT
  s.seller_key,
  s.seller_zip_code_prefix AS zip_code_prefix,
  s.seller_city,
  s.seller_state,

  COALESCE(f.total_orders, 0) AS total_orders,
  COALESCE(f.total_items, 0) AS total_items,
  COALESCE(f.total_revenue, 0) AS total_revenue,
  COALESCE(f.total_freight, 0) AS total_freight,
  SAFE_DIVIDE(COALESCE(f.total_revenue, 0), NULLIF(COALESCE(f.total_orders, 0), 0)) AS avg_order_value,

  COALESCE(f.delivered_items, 0) AS delivered_items,
  COALESCE(f.cancelled_items, 0) AS cancelled_items,
  SAFE_DIVIDE(COALESCE(f.delivered_items, 0), NULLIF(COALESCE(f.total_items, 0), 0)) AS delivered_item_rate,
  SAFE_DIVIDE(COALESCE(f.cancelled_items, 0), NULLIF(COALESCE(f.total_items, 0), 0)) AS cancelled_item_rate

FROM `web-analytics-funnel.olist_warehouse_us.dim_seller` s
LEFT JOIN seller_fact f
USING (seller_key);
