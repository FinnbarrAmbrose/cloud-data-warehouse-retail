CREATE OR REPLACE TABLE `web-analytics-funnel.olist_warehouse_us.dim_customer` AS
SELECT
  customer_id AS customer_key,              -- PK grain
  customer_unique_id,                       -- attribute (natural person/customer)
  customer_zip_code_prefix AS zip_code_prefix,
  customer_city,
  customer_state
FROM `web-analytics-funnel.olist_staging.olist_customers_dataset`;
