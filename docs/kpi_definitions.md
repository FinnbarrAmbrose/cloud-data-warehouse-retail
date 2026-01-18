# KPI Definitions — Olist Retail Analytics Warehouse

## Sales KPIs (mart_sales_daily)
- **Total Revenue**: Sum of item_price across all order items on the day.
- **Total Orders**: Count of distinct order_id on the day.
- **Total Items**: Count of order line items (rows in fact_order_item) on the day.
- **Average Order Value (AOV)**: Total Revenue / Total Orders.
- **Delivery Rate**: Delivered Orders / Total Orders.
- **Cancelled Orders**: Count of orders with status = 'canceled'.

## Customer KPIs (mart_customer_performance)
- **Total Orders**: Distinct orders by customer.
- **Total Items**: Total order items purchased by customer.
- **Total Revenue**: Sum of item_price for all customer purchases.
- **AOV (Customer)**: Total Revenue / Total Orders.
- **First Order Timestamp**: Earliest purchase timestamp observed for the customer.
- **Last Order Timestamp**: Latest purchase timestamp observed for the customer.

## Seller KPIs (mart_seller_performance)
- **Total Revenue**: Sum of item_price sold by seller.
- **Delivered Item Rate**: Delivered items / Total items for seller.
- **Cancelled Item Rate**: Cancelled items / Total items for seller.

## Product KPIs (mart_product_performance)
- **Total Units Sold**: Total order items per product.
- **Total Revenue**: Sum of item_price per product.
- **Average Item Price**: Average item_price per product.
