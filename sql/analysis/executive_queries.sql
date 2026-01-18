-- 1) Monthly revenue trend
SELECT
  FORMAT_DATE('%Y-%m', order_date) AS month,
  SUM(total_revenue) AS revenue,
  SUM(total_orders) AS orders,
  SAFE_DIVIDE(SUM(total_revenue), NULLIF(SUM(total_orders),0)) AS aov
FROM `web-analytics-funnel.olist_warehouse_us.mart_sales_daily`
GROUP BY month
ORDER BY month;

-- 2) Top 10 sellers by revenue
SELECT seller_key, seller_state, total_revenue, total_orders, delivered_item_rate
FROM `web-analytics-funnel.olist_warehouse_us.mart_seller_performance`
ORDER BY total_revenue DESC
LIMIT 10;

-- 3) Top 10 products by revenue
SELECT product_key, product_category_name, total_revenue, total_units_sold
FROM `web-analytics-funnel.olist_warehouse_us.mart_product_performance`
ORDER BY total_revenue DESC
LIMIT 10;

-- 4) Customer distribution by state
SELECT customer_state, COUNT(*) AS customers
FROM `web-analytics-funnel.olist_warehouse_us.mart_customer_performance`
GROUP BY customer_state
ORDER BY customers DESC;

-- 5) Highest value customers
SELECT customer_key, customer_state, total_revenue, total_orders, avg_order_value
FROM `web-analytics-funnel.olist_warehouse_us.mart_customer_performance`
ORDER BY total_revenue DESC
LIMIT 10;

