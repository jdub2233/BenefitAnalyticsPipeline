from pathlib import Path
import pandas as pd
import os
import psycopg

# Identify project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Locate validated enrollment data
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "accepted_enrollments.csv"
)

# Load accepted enrollment records
benefits = pd.read_csv(INPUT_FILE)

# Extract unique department names
departments = (
    benefits["department"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

print("DEPARTMENTS READY FOR DATABASE LOAD")
print("-----------------------------------")

for department in departments:
    print(department)

print(f"\nTotal unique departments: {len(departments)}")


# -----------------------------------------
# LOAD DEPARTMENTS INTO POSTGRESQL
# -----------------------------------------

db_password = os.environ.get("DB_PASSWORD")

if not db_password:
    raise RuntimeError(
        "DB_PASSWORD environment variable is not set."
    )

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="benefits_analytics",
    user="postgres",
    password=db_password
) as conn:

    with conn.cursor() as cursor:

        for department in departments:
            cursor.execute(
                """
                INSERT INTO departments (department_name)
                VALUES (%s)
                ON CONFLICT (department_name) DO NOTHING;
                """,
                (department,)
            )

    # The connection context commits on successful exit.

print("\nDepartments loaded into PostgreSQL successfully.")

