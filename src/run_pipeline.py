from pathlib import Path
import subprocess
import sys

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Define the scripts to execute
VALIDATION_SCRIPT = PROJECT_ROOT / "src" / "transform" / "validate_enrollments.py"
ANALYTICS_SCRIPT = PROJECT_ROOT / "src" / "transform" / "analyze_benefits.py"

# PostgreSQL loading scripts
DEPARTMENTS_SCRIPT = PROJECT_ROOT / "src" / "load" / "load_departments.py"
EMPLOYEES_SCRIPT = PROJECT_ROOT / "src" / "load" / "load_employees.py"
BENEFIT_PLANS_SCRIPT = PROJECT_ROOT / "src" / "load" / "load_benefit_plans.py"
ENROLLMENTS_SCRIPT = PROJECT_ROOT / "src" / "load" / "load_enrollments.py"

def run_step(step_name, script_path):
    """Execute a pipeline step and stop if it fails."""
    try:
        subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            cwd=PROJECT_ROOT
        )
        print(f"\nSUCCESS: {step_name}")

    except subprocess.CalledProcessError as error:
        print(f"\nFAILED: {step_name}")
        print(f"Exit code: {error.returncode}")
        raise SystemExit(error.returncode)


print("===================================")
print("    BENEFITS ANALYTICS PIPELINE")
print("===================================")


# Step 1: Validate enrollment data
print("\nSTEP 1: Validating enrollment data...")

validation_command = [sys.executable, str(VALIDATION_SCRIPT)]

if len(sys.argv) > 1:
    validation_command.append(sys.argv[1])

subprocess.run(
    validation_command,
    check=True,
    cwd=PROJECT_ROOT
)

print("\nEnrollment validation completed successfully.")

# Step 2: Analyze accepted enrollment data
print("\nSTEP 2: Analyzing validated enrollment data...")

subprocess.run(
    [sys.executable, str(ANALYTICS_SCRIPT)],
    check=True,
    cwd=PROJECT_ROOT
)

print("\nBenefits analytics completed successfully.")

# Step 3: Load departments into PostgreSQL
print("\nSTEP 3: Loading departments into PostgreSQL...")

run_step("Load Departments", DEPARTMENTS_SCRIPT)

print("\nDepartment loading completed successfully.")

# Step 4: Load employees into PostgreSQL
print("\nSTEP 4: Loading employees into PostgreSQL...")

run_step("Load Employees", EMPLOYEES_SCRIPT)

print("\nEmployee loading completed successfully.")

# Step 5: Verify benefit plans in PostgreSQL
print("\nSTEP 5: Verifying benefit plans in PostgreSQL...")

run_step("Verify Benefit Plans", BENEFIT_PLANS_SCRIPT)

print("\nBenefit plan verification completed successfully.")

# Step 6: Load enrollments into PostgreSQL
"""print("\nSTEP 6: Loading enrollments into PostgreSQL...")

subprocess.run(
    [sys.executable, str(ENROLLMENTS_SCRIPT)],
    check=True,
    cwd=PROJECT_ROOT
)

print("\nEnrollment loading completed successfully.")"""


print("\n===================================")
print("    PIPELINE STAGES 1-5 COMPLETED SUCCESSFULLY")
print("===================================")

