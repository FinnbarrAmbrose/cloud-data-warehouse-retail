import argparse
from pathlib import Path
from google.cloud import bigquery

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default="web-analytics-funnel")
    parser.add_argument("--sql", required=True, help="Path to .sql file")
    args = parser.parse_args()

    sql_path = Path(args.sql)
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    sql = sql_path.read_text(encoding="utf-8")
    client = bigquery.Client(project=args.project)

    print(f"Running SQL: {sql_path}")
    job = client.query(sql)
    job.result()
    print("Done.")

if __name__ == "__main__":
    main()
