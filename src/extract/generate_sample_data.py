from pathlib import Path
import pandas as pd

# Locate the root of the portfolio project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Where the generated CSV will be saved
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "benefits_enrollments.csv"

# Fictional employee benefits enrollment records
employees = [
    (1001, "Alex Morgan", "Engineering", "Medical", 550, 175),
    (1002, "Taylor Reed", "Finance", "Dental", 85, 30),
    (1003, "Jordan Lee", "HR", "Medical", 625, 225),
    (1004, "Casey Brooks", "Sales", "Vision", 45, 15),
    (1005, "Morgan Hayes", "Engineering", "Medical", 700, 275),
    (1006, "Riley Parker", "Finance", "Medical", 575, 200),
    (1007, "Jamie Carter", "HR", "Dental", 95, 35),
    (1008, "Avery Collins", "Sales", "Medical", 650, 250),
    (1009, "Cameron Price", "Engineering", "Dental", 90, 32),
    (1010, "Quinn Foster", "Finance", "Vision", 50, 18),
    (1011, "Drew Bennett", "HR", "Medical", 525, 150),
    (1012, "Skyler James", "Sales", "Dental", 100, 40),
    (1013, "Peyton Ross", "Engineering", "Vision", 55, 20),
    (1014, "Harper Stone", "Finance", "Medical", 600, 215),
    (1015, "Reese Walker", "HR", "Vision", 40, 12),
    (1016, "Blake Turner", "Sales", "Medical", 725, 300),
    (1017, "Emerson Gray", "Engineering", "Dental", 80, 28),
    (1018, "Rowan Scott", "Finance", "Dental", 105, 42),
    (1019, "Finley Adams", "HR", "Medical", 580, 195),
    (1020, "Dakota Ellis", "Sales", "Vision", 48, 16),
]

columns = [
    "employee_id",
    "employee_name",
    "department",
    "plan_type",
    "monthly_premium",
    "employee_monthly_cost",
]

# Convert the employee records into a pandas DataFrame
df = pd.DataFrame(employees, columns=columns)

# Ensure the destination folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Export the DataFrame to CSV
df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(df)} enrollment records.")
print(f"Saved to: {OUTPUT_FILE}")
print(df.head())
