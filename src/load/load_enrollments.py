from pathlib import Path
import pandas as pd
import os
import psycopg

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Locate the validated enrollment data
INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "accepted_enrollments.csv"
)

# Ensure the validated data exists
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "Validated enrollment data not found. "
        "Run the pipeline validation step first."
    )

# Load accepted enrollment records
enrollments = pd.read_csv(INPUT_FILE)

print("ENROLLMENTS READY FOR DATABASE LOAD")
print("-----------------------------------")
print(enrollments.head())

print(f"\nTotal accepted enrollments: {len(enrollments)}")

# Connect to PostgreSQL
DB_PASSWORD = os.environ.get("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable is not set.")

with psycopg.connect(
    host="localhost",
    dbname="benefits_analytics",
    user="postgres",
    password=DB_PASSWORD
) as conn:

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT plan_id, plan_type
            FROM benefit_plans
            ORDER BY plan_id;
        """)

        plan_rows = cursor.fetchall()

# Convert PostgreSQL results into a DataFrame
plans = pd.DataFrame(
    plan_rows,
    columns=["plan_id", "plan_type"]
)

print("\nBENEFIT PLANS FROM POSTGRESQL")
print("-----------------------------")
print(plans.to_string(index=False))

# Map each enrollment to its PostgreSQL benefit plan ID
enrollments_with_plan_ids = enrollments.merge(
    plans,
    on="plan_type",
    how="left",
    validate="many_to_one"
)

print("\nENROLLMENTS WITH POSTGRESQL PLAN IDS")
print("------------------------------------")

print(
    enrollments_with_plan_ids[
        ["employee_id", "plan_type", "plan_id"]
    ].to_string(index=False)
)

# Ensure every enrollment matched a PostgreSQL benefit plan
unmatched_plans = enrollments_with_plan_ids[
    enrollments_with_plan_ids["plan_id"].isna()
]

if not unmatched_plans.empty:
    raise ValueError(
        "Some enrollments could not be mapped to PostgreSQL plans:\n"
        f"{unmatched_plans[['employee_id', 'plan_type']]}"
    )

assert len(enrollments_with_plan_ids) == len(enrollments), (
    "Enrollment count changed during plan mapping."
)

print("\nAll enrollments successfully mapped to benefit plans.")

# Retrieve existing employee IDs from PostgreSQL
with psycopg.connect(
    host="localhost",
    dbname="benefits_analytics",
    user="postgres",
    password=DB_PASSWORD
) as conn:

    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT employee_id
            FROM employees
            ORDER BY employee_id;
        """)

        employee_rows = cursor.fetchall()

# Convert results to a set for efficient lookup
db_employee_ids = {row[0] for row in employee_rows}

# Identify employee IDs in the CSV that are missing from PostgreSQL
csv_employee_ids = set(enrollments_with_plan_ids["employee_id"])

missing_employee_ids = csv_employee_ids - db_employee_ids

if missing_employee_ids:
    raise ValueError(
        f"Employees missing from PostgreSQL: {missing_employee_ids}"
    )

print("\nAll enrollment employee IDs exist in PostgreSQL.")
print(f"Verified {len(csv_employee_ids)} unique employee IDs.")


# Prepare enrollment records for PostgreSQL
enrollments_to_load = enrollments_with_plan_ids[
    [
        "employee_id",
        "plan_id",
        "monthly_premium",
        "employee_monthly_cost"
    ]
].copy()

print("\nENROLLMENTS PREPARED FOR POSTGRESQL")
print("-----------------------------------")
print(enrollments_to_load.head())

print(f"\nTotal records ready to load: {len(enrollments_to_load)}")

# Insert validated enrollments into PostgreSQL
records_to_insert = list(
    enrollments_to_load.itertuples(index=False, name=None)
)

print(f"\nRecords prepared for insertion: {len(records_to_insert)}")
print(f"First record: {records_to_insert[0]}")

insert_sql = """
    INSERT INTO enrollments (
        employee_id,
        plan_id,
        monthly_premium,
        employee_monthly_cost
    )
    VALUES (%s, %s, %s, %s);
"""
# Connect to PostgreSQL and insert enrollments
with psycopg.connect(
    host="localhost",
    dbname="benefits_analytics",
    user="postgres",
    password=DB_PASSWORD
) as conn:

    with conn.cursor() as cursor:

        # Prevent accidental duplicate loads
        cursor.execute("SELECT COUNT(*) FROM enrollments;")
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            raise ValueError(
                f"Enrollment table already contains {existing_count} records. "
                "Load cancelled to prevent duplicates."
            )

        # Insert all validated enrollment records
        cursor.executemany(insert_sql, records_to_insert)

        # Verify the number of records inserted
        cursor.execute("SELECT COUNT(*) FROM enrollments;")
        inserted_count = cursor.fetchone()[0]

        if inserted_count != len(records_to_insert):
            raise ValueError(
                f"Expected {len(records_to_insert)} records, "
                f"but found {inserted_count}."
            )

    # Transaction commits automatically when the connection block succeeds

print(f"\nSuccessfully loaded {inserted_count} enrollments into PostgreSQL.")
