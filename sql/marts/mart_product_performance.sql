CREATE OR REPLACE TABLE `web-analytics-funnel.olist_warehouse_us.mart_product_performance` AS
WITH product_fact AS (
  SELECT
    product_key,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_units_sold,
    SUM(COALESCE(item_price, 0)) AS total_revenue,
    SUM(COALESCE(freight_value, 0)) AS total_freight,
    AVG(COALESCE(item_price, 0)) AS avg_item_price
  FROM `web-analytics-funnel.olist_warehouse_us.fact_order_item`
  GROUP BY product_key
)
SELECT
  p.product_key,
  p.product_category_name,
  p.product_weight_g,
  p.product_length_cm,
  p.product_height_cm,
  p.product_width_cm,

  COALESCE(f.total_orders, 0) AS total_orders,
  COALESCE(f.total_units_sold, 0) AS total_units_sold,
  COALESCE(f.total_revenue, 0) AS total_revenue,
  COALESCE(f.total_freight, 0) AS total_freight,
  COALESCE(f.avg_item_price, 0) AS avg_item_price

FROM `web-analytics-funnel.olist_warehouse_us.dim_product` p
LEFT JOIN product_fact f
USING (product_key);
