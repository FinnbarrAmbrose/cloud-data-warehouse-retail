import os
import pandas as pd

STG_DIR = "data/staging/olist"
OUT_MD = "docs/data_quality_checks.md"

def load(name: str) -> pd.DataFrame:
    fp = os.path.join(STG_DIR, name)
    return pd.read_csv(fp, low_memory=False)

def pk_check(df: pd.DataFrame, table: str, cols: list[str]) -> dict:
    total = len(df)
    null_keys = int(df[cols].isna().any(axis=1).sum())
    dup = int(df.duplicated(subset=cols).sum())
    distinct = int(df[cols].dropna().drop_duplicates().shape[0])
    return {
        "table": table,
        "pk": ", ".join(cols),
        "rows": total,
        "null_keys": null_keys,
        "dup_keys": dup,
        "distinct_keys": distinct,
    }

def fk_check(child: pd.DataFrame, parent: pd.DataFrame, child_table: str, parent_table: str, child_key: str, parent_key: str) -> dict:
    child_keys = child[child_key].dropna().astype(str)
    parent_keys = set(parent[parent_key].dropna().astype(str).unique())
    missing = int((~child_keys.isin(parent_keys)).sum())
    total = int(len(child_keys))
    return {
        "child_table": child_table,
        "parent_table": parent_table,
        "fk": f"{child_table}.{child_key} -> {parent_table}.{parent_key}",
        "child_nonnull_keys": total,
        "missing_in_parent": missing,
        "missing_rate": (missing / total) if total else 0.0,
    }

def main():
    os.makedirs("docs", exist_ok=True)

    customers = load("olist_customers_dataset.csv")
    orders = load("olist_orders_dataset.csv")
    order_items = load("olist_order_items_dataset.csv")
    payments = load("olist_order_payments_dataset.csv")
    reviews = load("olist_order_reviews_dataset.csv")
    products = load("olist_products_dataset.csv")
    sellers = load("olist_sellers_dataset.csv")

    pk_results = [
        pk_check(customers, "olist_customers_dataset.csv", ["customer_id"]),
        pk_check(orders, "olist_orders_dataset.csv", ["order_id"]),
        pk_check(order_items, "olist_order_items_dataset.csv", ["order_id", "order_item_id"]),
        pk_check(payments, "olist_order_payments_dataset.csv", ["order_id", "payment_sequential"]),
        pk_check(reviews, "olist_order_reviews_dataset.csv", ["review_id"]),
        pk_check(products, "olist_products_dataset.csv", ["product_id"]),
        pk_check(sellers, "olist_sellers_dataset.csv", ["seller_id"]),
    ]
    pk_df = pd.DataFrame(pk_results)

    fk_results = [
        fk_check(orders, customers, "olist_orders_dataset.csv", "olist_customers_dataset.csv", "customer_id", "customer_id"),
        fk_check(order_items, orders, "olist_order_items_dataset.csv", "olist_orders_dataset.csv", "order_id", "order_id"),
        fk_check(payments, orders, "olist_order_payments_dataset.csv", "olist_orders_dataset.csv", "order_id", "order_id"),
        fk_check(reviews, orders, "olist_order_reviews_dataset.csv", "olist_orders_dataset.csv", "order_id", "order_id"),
        fk_check(order_items, products, "olist_order_items_dataset.csv", "olist_products_dataset.csv", "product_id", "product_id"),
        fk_check(order_items, sellers, "olist_order_items_dataset.csv", "olist_sellers_dataset.csv", "seller_id", "seller_id"),
    ]
    fk_df = pd.DataFrame(fk_results)

    # Write markdown report (requires `tabulate`)
    lines = []
    lines.append("# Data Quality Checks — Stage 3")
    lines.append("")
    lines.append("## Primary key checks")
    lines.append("")
    lines.append(pk_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Foreign key checks")
    lines.append("")
    lines.append(fk_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Notes")
    lines.append("- Null cells in reviews and delivery timestamps are expected; downstream KPIs must filter appropriately.")
    lines.append("- Geolocation duplicates will be resolved via a ZIP-prefix aggregation in modelling/staging.")
    lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(pk_df.to_string(index=False))
    print("")
    print(fk_df.to_string(index=False))
    print(f"\nWrote: {OUT_MD}")

if __name__ == "__main__":
    main()
