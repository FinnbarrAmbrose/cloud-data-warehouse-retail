# Data Quality — Stage 3 (Staging)

## Objective
Create a trusted staging layer with consistent types, documented null handling, and validated join keys.

## Dataset
Olist Brazilian E-commerce (raw CSVs in `data/raw/olist/`).

## Standardisation rules (Stage 3)
- Date columns parsed to datetime (invalid values coerced to null).
- Numeric columns coerced to numeric (invalid values coerced to null).
- String columns trimmed of leading/trailing whitespace.
- No business logic transformations applied yet (modelling happens later).

## Checks executed (Stage 3)
- Row counts per table
- Column counts per table
- Total null cell count per table
- Duplicate row count per table

## Outputs
- `data/staging/olist/*.csv`
- `docs/data_quality_summary_stage3.csv`

## Issues found + fixes
(To be completed after running the staging script.)
