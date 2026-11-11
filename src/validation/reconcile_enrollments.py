
from pathlib import Path
import pandas as pd
import os
import psycopg

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Locate the accepted enrollment data
CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "accepted_enrollments.csv"
)

# Verify that the CSV exists
if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Accepted enrollment file not found: {CSV_PATH}"
    )

# Load accepted enrollment records
csv_enrollments = pd.read_csv(CSV_PATH)

print("CSV ENROLLMENT RECONCILIATION")
print("-----------------------------")
print(f"CSV records loaded: {len(csv_enrollments)}")
print(csv_enrollments.head())


# Retrieve the PostgreSQL password
DB_PASSWORD = os.environ.get("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError(
        "DB_PASSWORD environment variable is not set."
    )

# Query PostgreSQL enrollment records
with psycopg.connect(
    host="localhost",
    dbname="benefits_analytics",
    user="postgres",
    password=DB_PASSWORD
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                source_enrollment_id,
                employee_id,
                monthly_premium,
                employee_monthly_cost,
                effective_date
            FROM enrollments
            ORDER BY source_enrollment_id;
        """)

        db_rows = cursor.fetchall()

# Convert PostgreSQL results into a DataFrame
db_enrollments = pd.DataFrame(
    db_rows,
    columns=[
        "source_enrollment_id",
        "employee_id",
        "monthly_premium",
        "employee_monthly_cost",
        "effective_date"
    ]
)

print("\nPOSTGRESQL ENROLLMENT RECONCILIATION")
print("-----------------------------------")
print(f"PostgreSQL records loaded: {len(db_enrollments)}")
print(db_enrollments.head())


# Fields shared by the CSV and PostgreSQL
compare_columns = [
    "employee_id",
    "monthly_premium",
    "employee_monthly_cost",
    "effective_date"
]

# Normalize values for consistent comparison
for df in [csv_enrollments, db_enrollments]:
    df["monthly_premium"] = pd.to_numeric(
        df["monthly_premium"]
    )
    df["employee_monthly_cost"] = pd.to_numeric(
        df["employee_monthly_cost"]
    )
    df["effective_date"] = pd.to_datetime(
        df["effective_date"]
    )

# Validate source enrollment identifiers before comparison
for dataset_name, df in [
    ("CSV", csv_enrollments),
    ("PostgreSQL", db_enrollments)
]:
    missing_ids = df["source_enrollment_id"].isna().sum()
    duplicate_ids = df["source_enrollment_id"].duplicated().sum()

    if missing_ids > 0 or duplicate_ids > 0:
        print(f"\n{dataset_name} IDENTIFIER VALIDATION FAILED")
        print(f"Missing source IDs: {missing_ids}")
        print(f"Duplicate source IDs: {duplicate_ids}")
        raise SystemExit(1)

print("\nSource enrollment ID validation passed.")

# Use the source enrollment ID as the record identifier
csv_data = csv_enrollments.set_index(
    "source_enrollment_id"
)[compare_columns].sort_index()

db_data = db_enrollments.set_index(
    "source_enrollment_id"
)[compare_columns].sort_index()

# Identify records missing from either dataset
missing_from_db = csv_data.index.difference(db_data.index)
missing_from_csv = db_data.index.difference(csv_data.index)

print("\nRECONCILIATION RESULTS")
print("----------------------")
print(f"Missing from PostgreSQL: {len(missing_from_db)}")
print(f"Missing from CSV: {len(missing_from_csv)}")

# Compare only records present in both datasets
common_ids = csv_data.index.intersection(db_data.index)

differences = csv_data.loc[common_ids].compare(
    db_data.loc[common_ids]
)

print(f"Records with field differences: "
      f"{len(differences)}")

if differences.empty and len(missing_from_db) == 0 and len(missing_from_csv) == 0:
    print("RECONCILIATION PASSED")
else:
    print("RECONCILIATION FAILED")
    print(differences)
    raise SystemExit(1)

