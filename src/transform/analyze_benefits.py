
from pathlib import Path
import pandas as pd

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Locate the original enrollment dataset
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "benefits_enrollments.csv"

# Load the CSV into a pandas DataFrame
benefits = pd.read_csv(INPUT_FILE)

print("====================================")
print("      BENEFITS ANALYTICS REPORT     ")
print("====================================")

print(f"\nTotal Enrollment Records: {len(benefits)}")
print("\nSample Enrollment Data:")
print(benefits.head())

# -----------------------------------------
# EXERCISE 1 - SUMMARY STATISTICS
# -----------------------------------------

print("\n=== Summary Statistics ===")
average_monthly_premium = benefits["monthly_premium"].mean()
print(f"Average Monthly Premium: ${average_monthly_premium:.2f}")

total_employee_monthly_cost = benefits["employee_monthly_cost"].sum()
print(f"Total Employee Monthly Cost: ${total_employee_monthly_cost:.2f}")

highest_monthly_premium = benefits["monthly_premium"].max()
print(f"Highest Monthly Premium: ${highest_monthly_premium:.2f}")

lowest_monthly_premium = benefits["monthly_premium"].min()
print(f"Lowest Monthly Premium: ${lowest_monthly_premium:.2f}")


# -----------------------------------------
# EXERCISE 2 - DEPARTMENT ANALYSIS
# -----------------------------------------


print("\n=== Department Analysis ===")
dept_avg_premium = benefits.groupby("department")["monthly_premium"].mean()
print("Average Monthly Premium by Department:")
print(dept_avg_premium)

dept_total_cost = benefits.groupby("department")["employee_monthly_cost"].sum()
print("\nTotal Employee Monthly Cost by Department:")
print(dept_total_cost)


# -----------------------------------------
# EXERCISE 3 - PLAN TYPE ANALYSIS
# -----------------------------------------

print("\n=== Plan Type Analysis ===")
plan_counts = benefits.groupby("plan_type").size()
print("Number of Enrollments by Plan Type:")
print(plan_counts)

plan_avg_premium = benefits.groupby("plan_type")["monthly_premium"].mean()
print("\nAverage Monthly Premium by Plan Type:")
for plan_type, average in plan_avg_premium.items():
    print(f"{plan_type}: ${average:,.2f}")


# -----------------------------------------
# EXERCISE 4 - PIVOT TABLE
# -----------------------------------------

report = benefits.pivot_table(
    index="department",
    columns="plan_type",
    values="employee_monthly_cost",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="Total"
)
formatted_report = report.map(lambda value: f"${value:,.2f}")
print("\n=== BENEFITS COST PIVOT TABLE ===")
print(formatted_report.to_string())

OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "department_benefits_costs.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

report.to_csv(OUTPUT_FILE, index=True)

print(f"\nReport exported to: {OUTPUT_FILE}")

# -----------------------------------------
# RECONCILIATION CHECK
# -----------------------------------------

source_total = benefits["employee_monthly_cost"].sum()
report_total = report.loc["Total", "Total"]

assert source_total == report_total, (
    f"Reconciliation failed: source={source_total}, report={report_total}"
)

print(f"Cost reconciliation passed: ${report_total:,.2f}")