import os
import pandas as pd

RAW_DIR = "data/raw/olist"
STG_DIR = "data/staging/olist"
os.makedirs(STG_DIR, exist_ok=True)

FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]

DATE_COLS = {
    "olist_orders_dataset.csv": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_order_items_dataset.csv": ["shipping_limit_date"],
    "olist_order_reviews_dataset.csv": ["review_creation_date", "review_answer_timestamp"],
}

NUMERIC_COLS = {
    "olist_order_items_dataset.csv": ["order_item_id", "price", "freight_value"],
    "olist_order_payments_dataset.csv": ["payment_sequential", "payment_installments", "payment_value"],
    "olist_order_reviews_dataset.csv": ["review_score"],
    "olist_products_dataset.csv": [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "olist_customers_dataset.csv": ["customer_zip_code_prefix"],
    "olist_sellers_dataset.csv": ["seller_zip_code_prefix"],
    "olist_geolocation_dataset.csv": ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"],
}

def read_csv(fp: str) -> pd.DataFrame:
    return pd.read_csv(fp, low_memory=False)

def coerce_dates(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def profile(df: pd.DataFrame, name: str) -> dict:
    return {
        "table": name,
        "rows": int(len(df)),
        "cols": int(df.shape[1]),
        "null_cells": int(df.isna().sum().sum()),
        "dup_rows": int(df.duplicated().sum()),
    }

def main():
    profiles = []

    for f in FILES:
        fp = os.path.join(RAW_DIR, f)
        if not os.path.exists(fp):
            raise FileNotFoundError(f"Missing raw file: {fp}")

        df = read_csv(fp)
        df = coerce_dates(df, DATE_COLS.get(f, []))
        df = coerce_numeric(df, NUMERIC_COLS.get(f, []))

        # Trim whitespace on string-like columns
        for c in df.columns:
            if df[c].dtype == "object":
                df[c] = df[c].astype("string").str.strip()

        out_fp = os.path.join(STG_DIR, f)
        df.to_csv(out_fp, index=False)

        profiles.append(profile(df, f))

    prof_df = pd.DataFrame(profiles).sort_values("table")
    print(prof_df.to_string(index=False))

    os.makedirs("docs", exist_ok=True)
    prof_df.to_csv("docs/data_quality_summary_stage3.csv", index=False)
    print("\nWrote: docs/data_quality_summary_stage3.csv")
    print(f"Wrote staged CSVs to: {STG_DIR}")

if __name__ == "__main__":
    main()
