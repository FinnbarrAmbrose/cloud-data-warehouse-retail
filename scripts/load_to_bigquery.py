"""
Load staged Olist CSVs into BigQuery staging dataset.

- Reads config/settings.yaml for project + dataset names
- Loads all CSVs from data/staging/olist/*.csv
- Table names are derived from file names (without .csv)
- Supports --dry-run to validate what would happen

Usage:
  python scripts/load_to_bigquery.py --dry-run
  python scripts/load_to_bigquery.py
"""

from __future__ import annotations

import argparse
import glob
import os
from dataclasses import dataclass
from typing import Dict, List

import yaml
from google.cloud import bigquery


@dataclass(frozen=True)
class Settings:
    project_id: str
    location: str
    staging_dataset: str


def load_settings(path: str = "config/settings.yaml") -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Expected structure:
    # gcp: { project_id: ..., location: ... }
    # bigquery: { staging_dataset: ... }
    return Settings(
        project_id=cfg["gcp"]["project_id"],
        location=cfg["gcp"]["location"],
        staging_dataset=cfg["bigquery"]["staging_dataset"],
    )


def discover_csvs(staging_dir: str = "data/staging/olist") -> List[str]:
    files = sorted(glob.glob(os.path.join(staging_dir, "*.csv")))
    return files


def ensure_dataset(client: bigquery.Client, dataset_id: str, location: str) -> None:
    dataset_ref = bigquery.Dataset(dataset_id)
    dataset_ref.location = location
    client.create_dataset(dataset_ref, exists_ok=True)


def load_csv_to_table(
    client: bigquery.Client,
    csv_path: str,
    table_fqdn: str,
    location: str,
    dry_run: bool,
) -> None:
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        allow_quoted_newlines=True,
    )

    if dry_run:
        print(f"[DRY-RUN] Would load: {csv_path} -> {table_fqdn}")
        return

    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(
            f,
            table_fqdn,
            job_config=job_config,
            location=location,
        )
    job.result()

    table = client.get_table(table_fqdn)
    print(f"[OK] Loaded {table.num_rows:,} rows into {table_fqdn}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Load staged Olist CSVs into BigQuery.")
    p.add_argument("--dry-run", action="store_true", help="Print actions without loading.")
    p.add_argument(
        "--staging-dir",
        default="data/staging/olist",
        help="Directory containing staged CSVs.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings()

    client = bigquery.Client(project=settings.project_id)

    dataset_fqdn = f"{settings.project_id}.{settings.staging_dataset}"
    print(f"Project: {settings.project_id}")
    print(f"Location: {settings.location}")
    print(f"Staging dataset: {dataset_fqdn}")

    # Ensure dataset exists
    if args.dry_run:
        print(f"[DRY-RUN] Would ensure dataset exists: {dataset_fqdn} (location={settings.location})")
    else:
        ensure_dataset(client, dataset_fqdn, settings.location)
        print(f"[OK] Dataset ready: {dataset_fqdn}")

    csv_files = discover_csvs(args.staging_dir)
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {args.staging_dir}")

    print(f"Found {len(csv_files)} staging CSVs.")
    for csv_path in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
        table_fqdn = f"{dataset_fqdn}.{table_name}"
        load_csv_to_table(
            client=client,
            csv_path=csv_path,
            table_fqdn=table_fqdn,
            location=settings.location,
            dry_run=args.dry_run,
        )

    print("Done.")


if __name__ == "__main__":
    main()
