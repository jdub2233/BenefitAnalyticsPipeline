from pathlib import Path
import subprocess
import sys

# Identify the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Define the scripts to execute
VALIDATION_SCRIPT = PROJECT_ROOT / "src" / "transform" / "validate_enrollments.py"
ANALYTICS_SCRIPT = PROJECT_ROOT / "src" / "transform" / "analyze_benefits.py"


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


print("\n===================================")
print("    PIPELINE COMPLETED SUCCESSFULLY")
print("===================================")

