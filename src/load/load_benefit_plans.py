from pathlib import Path
import os

import pandas as pd
import psycopg

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "accepted_enrollments.csv"
)

# Read validated enrollment data
benefits = pd.read_csv(INPUT_FILE)

# Extract unique plan types
plan_types = (
    benefits["plan_type"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

print("PLAN TYPES FROM VALIDATED DATA")
print("------------------------------")
print(plan_types.to_string(index=False))

# Connect to PostgreSQL
db_password = os.environ.get("DB_PASSWORD")

if not db_password:
    raise RuntimeError("DB_PASSWORD environment variable is not set.")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="benefits_analytics",
    user="postgres",
    password=db_password
) as conn:

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT plan_id, plan_type FROM benefit_plans"
        )
        plan_rows = cursor.fetchall()

plans = pd.DataFrame(
    plan_rows,
    columns=["plan_id", "plan_type"]
)

print("\nBENEFIT PLANS FROM POSTGRESQL")
print("-----------------------------")
print(plans.to_string(index=False))


# Verify every CSV plan type exists in PostgreSQL
csv_plan_types = set(plan_types)
db_plan_types = set(plans["plan_type"])

missing_plans = csv_plan_types - db_plan_types

if missing_plans:
    raise ValueError(
        f"Plan types missing from PostgreSQL: {missing_plans}"
    )

print("\nAll validated plan types exist in PostgreSQL.")

