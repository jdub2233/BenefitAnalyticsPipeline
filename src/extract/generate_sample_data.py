from pathlib import Path
import pandas as pd

# Locate the root of the portfolio project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Where the generated CSV will be saved
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "benefits_enrollments.csv"

# Fictional employee benefits enrollment records
employees = [
    (1001, "Alex Morgan", "Engineering", "Medical", 550, 175, "ENR-1001-2026"),
    (1002, "Taylor Reed", "Finance", "Dental", 85, 30, "ENR-1002-2026"),
    (1003, "Jordan Lee", "HR", "Medical", 625, 225, "ENR-1003-2026"),
    (1004, "Casey Brooks", "Sales", "Vision", 45, 15, "ENR-1004-2026"),
    (1005, "Morgan Hayes", "Engineering", "Medical", 700, 275, "ENR-1005-2026"),
    (1006, "Riley Parker", "Finance", "Medical", 575, 200, "ENR-1006-2026"),
    (1007, "Jamie Carter", "HR", "Dental", 95, 35, "ENR-1007-2026"),
    (1008, "Avery Collins", "Sales", "Medical", 650, 250, "ENR-1008-2026"),
    (1009, "Cameron Price", "Engineering", "Dental", 90, 32, "ENR-1009-2026"),
    (1010, "Quinn Foster", "Finance", "Vision", 50, 18, "ENR-1010-2026"),
    (1011, "Drew Bennett", "HR", "Medical", 525, 150, "ENR-1011-2026"),
    (1012, "Skyler James", "Sales", "Dental", 100, 40, "ENR-1012-2026"),
    (1013, "Peyton Ross", "Engineering", "Vision", 55, 20, "ENR-1013-2026"),
    (1014, "Harper Stone", "Finance", "Medical", 600, 215, "ENR-1014-2026"),
    (1015, "Reese Walker", "HR", "Vision", 40, 12, "ENR-1015-2026"),
    (1016, "Blake Turner", "Sales", "Medical", 725, 300, "ENR-1016-2026"),
    (1017, "Emerson Gray", "Engineering", "Dental", 80, 28, "ENR-1017-2026"),
    (1018, "Rowan Scott", "Finance", "Dental", 105, 42, "ENR-1018-2026"),
    (1019, "Finley Adams", "HR", "Medical", 580, 195, "ENR-1019-2026"),
    (1020, "Dakota Ellis", "Sales", "Vision", 48, 16, "ENR-1020-2026"),
    (1001, "Alex Morgan", "Engineering", "Dental", 85, 30, "ENR-1001-DENTAL-2026"),
]

columns = [
    "employee_id",
    "employee_name",
    "department",
    "plan_type",
    "monthly_premium",
    "employee_monthly_cost",
    "source_enrollment_id",
]

# Convert the employee records into a pandas DataFrame
df = pd.DataFrame(employees, columns=columns)

# Coverage start date for the 2026 enrollment period
df["effective_date"] = "2026-01-01"

# Ensure the destination folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Export the DataFrame to CSV
df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(df)} enrollment records.")
print(f"Saved to: {OUTPUT_FILE}")
print(df.head())
