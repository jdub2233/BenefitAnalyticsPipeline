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

# Read validated enrollment records
benefits = pd.read_csv(INPUT_FILE)

# Select employee information
employees = benefits[
    ["employee_id", "employee_name", "department"]
].drop_duplicates(subset=["employee_id"])

print("EMPLOYEES FROM VALIDATED DATA")
print("-----------------------------")
print(employees)

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
            "SELECT department_id, department_name FROM departments"
        )

        department_rows = cursor.fetchall()

    departments = pd.DataFrame(
        department_rows,
        columns=["department_id", "department_name"]
    )

print("\nDEPARTMENTS FROM POSTGRESQL")
print("---------------------------")
print(departments)

# -----------------------------------------
# MAP EMPLOYEES TO DEPARTMENT IDS
# -----------------------------------------

employees_with_departments = employees.merge(
    departments,
    left_on="department",
    right_on="department_name",
    how="left",
    validate="many_to_one"
)

print("\nEMPLOYEES WITH DEPARTMENT IDS")
print("-----------------------------")

print(
    employees_with_departments[
        ["employee_id", "employee_name", "department_id"]
    ].to_string(index=False)
)

# Check for employees without a matching department
missing_departments = employees_with_departments[
    employees_with_departments["department_id"].isna()
]

if not missing_departments.empty:
    raise ValueError(
        "Some employees could not be matched to a department:\n"
        + missing_departments.to_string(index=False)
    )

print("\nAll employees successfully mapped to departments.")


# -----------------------------------------
# LOAD EMPLOYEES INTO POSTGRESQL
# -----------------------------------------

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="benefits_analytics",
    user="postgres",
    password=db_password
) as conn:

    with conn.cursor() as cursor:

        for employee in employees_with_departments.itertuples(index=False):

            cursor.execute(
                """
                INSERT INTO employees (
                    employee_id,
                    employee_name,
                    department_id
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (employee_id)
                DO UPDATE SET
                    employee_name = EXCLUDED.employee_name,
                    department_id = EXCLUDED.department_id;
                """,
                (
                    int(employee.employee_id),
                    employee.employee_name,
                    int(employee.department_id)
                )
            )

print("\nEmployees loaded into PostgreSQL successfully.")


