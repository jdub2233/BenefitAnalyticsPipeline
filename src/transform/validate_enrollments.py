import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]

if len(sys.argv) > 1:
    csv_path = Path(sys.argv[1])
    if not csv_path.is_absolute():
        csv_path = BASE_DIR / csv_path
else:
    csv_path = BASE_DIR / "data" / "raw" / "benefits_enrollments.csv"

df = pd.read_csv(csv_path)

print("ALL ENROLLMENT DATA")
print("---------------------")
print(df)

print("BENEFITS DATA VALIDATION")
print("------------------------")
print(f"Total Records: {len(df)}")

missing_ids = df["employee_id"].isna().sum()
print(f"\nMissing Employee IDs: {missing_ids}")

records_with_missing_ids = df[df["employee_id"].isna()]
print("\nRecords with Missing Employee IDs:")
print(records_with_missing_ids)


duplicate_records = df.duplicated(
    subset=["employee_id", "plan_type"],
    keep=False
)

duplicate_count = duplicate_records.sum()

print(f"\nDuplicate Enrollment Records: {duplicate_count}")

records_with_duplicates = df[duplicate_records]
print("\nRecords with Duplicate Enrollment Records:")
print(records_with_duplicates)

negative_premiums = df["monthly_premium"] < 0

negative_premium_count = negative_premiums.sum()

print(f"\nNegative Monthly Premiums: {negative_premium_count}")

records_with_negative_premiums = df[negative_premiums]
print("\nRecords with Negative Monthly Premiums:")  
print(records_with_negative_premiums)

negative_employee_costs = df["employee_monthly_cost"] < 0
negative_employee_cost_count = negative_employee_costs.sum()
print(f"\nNegative Employee Monthly Costs: {negative_employee_cost_count}")
records_with_negative_employee_costs = df[negative_employee_costs]
print("\nRecords with Negative Employee Monthly Costs:")
print(records_with_negative_employee_costs)

valid_plan_types = ["Medical", "Dental", "Vision"]
invalid_plan_types = ~df["plan_type"].isin(valid_plan_types)
invalid_plan_count = invalid_plan_types.sum()
print(f"\nInvalid Plan Types: {invalid_plan_count}")
records_with_invalid_plans = df[invalid_plan_types]
print("\nRecords with Invalid Plan Types:")
print(records_with_invalid_plans)

invalid_records = (
    df["employee_id"].isna()
    | duplicate_records
    | negative_premiums
    | negative_employee_costs
    | invalid_plan_types
)

accepted_df = df[~invalid_records]
rejected_df = df[invalid_records]

print("\nENROLLMENT VALIDATION SUMMARY")
print("-----------------------------")
print(f"Total Records: {len(df)}")
print(f"Accepted Records: {len(accepted_df)}")
print(f"Rejected Records: {len(rejected_df)}")

