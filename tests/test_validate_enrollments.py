import pandas as pd

from src.transform.validate_enrollments import validate_enrollments


def test_missing_employee_id():
    # Arrange: Create one valid and one invalid enrollment
    df = pd.DataFrame({
        "employee_id": [101, None],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Dental"],
        "monthly_premium": [500, 100],
        "employee_monthly_cost": [150, 30],
        "source_enrollment_id": ["ENR-101", "ENR-102"],
        "effective_date": ["2026-01-01", "2026-01-01"]
    })

    # Act: Execute your actual validation function
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert: Verify the expected results
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Missing Employee ID" in rejected_df.iloc[0]["rejection_reason"]


def test_negative_monthly_premium():
    # Arrange: Create one valid and one invalid enrollment
    df = pd.DataFrame({
        "employee_id": [101, 102],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Dental"],
        "monthly_premium": [500, -100],
        "employee_monthly_cost": [150, 30],
        "source_enrollment_id": ["ENR-101", "ENR-102"],
        "effective_date": ["2026-01-01", "2026-01-01"]
    })

    # Act: Execute the actual validation function
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert: Verify the negative premium was rejected
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Negative Monthly Premium" in rejected_df.iloc[0]["rejection_reason"]


def test_duplicate_enrollment_ids():
    # Arrange: Two duplicate enrollments and one valid enrollment
    df = pd.DataFrame({
        "employee_id": [101, 102, 103],
        "employee_name": ["John", "Sarah", "Mike"],
        "department": ["Engineering", "HR", "Sales"],
        "plan_type": ["Medical", "Dental", "Vision"],
        "monthly_premium": [500, 100, 50],
        "employee_monthly_cost": [150, 30, 10],
        "source_enrollment_id": ["ENR-101", "ENR-101", "ENR-103"],
        "effective_date": ["2026-01-01"] * 3
    })

    # Act
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert
    assert len(accepted_df) == 1
    assert len(rejected_df) == 2

    assert accepted_df.iloc[0]["employee_name"] == "Mike"

    assert all(
        rejected_df["rejection_reason"].str.contains("Duplicate Record")
    )


def test_invalid_plan_type():
    # Arrange: One valid enrollment and one invalid plan
    df = pd.DataFrame({
        "employee_id": [101, 102],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Life"],
        "monthly_premium": [500, 100],
        "employee_monthly_cost": [150, 30],
        "source_enrollment_id": ["ENR-101", "ENR-102"],
        "effective_date": ["2026-01-01", "2026-01-01"]
    })

    # Act: Execute the production validation function
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert: Verify the invalid plan was rejected
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1

    assert accepted_df.iloc[0]["employee_name"] == "John"
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Invalid Plan Type" in rejected_df.iloc[0]["rejection_reason"]


def test_invalid_effective_date():
    # Arrange: One valid date and one invalid date
    df = pd.DataFrame({
        "employee_id": [101, 102],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Dental"],
        "monthly_premium": [500, 100],
        "employee_monthly_cost": [150, 30],
        "source_enrollment_id": ["ENR-101", "ENR-102"],
        "effective_date": ["2026-01-01", "not-a-date"]
    })

    # Act
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1

    assert accepted_df.iloc[0]["employee_name"] == "John"
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Invalid Effective Date" in rejected_df.iloc[0]["rejection_reason"]


def test_missing_source_enrollment_id():
    # Arrange: One valid enrollment and one with a blank source ID
    df = pd.DataFrame({
        "employee_id": [101, 102],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Dental"],
        "monthly_premium": [500, 100],
        "employee_monthly_cost": [150, 30],
        "source_enrollment_id": ["ENR-101", "   "],
        "effective_date": ["2026-01-01", "2026-01-01"]
    })

    # Act
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1

    assert accepted_df.iloc[0]["employee_name"] == "John"
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Missing Source Enrollment ID" in rejected_df.iloc[0]["rejection_reason"]


def test_negative_employee_monthly_cost():
    # Arrange: One valid enrollment and one negative employee cost
    df = pd.DataFrame({
        "employee_id": [101, 102],
        "employee_name": ["John", "Sarah"],
        "department": ["Engineering", "HR"],
        "plan_type": ["Medical", "Dental"],
        "monthly_premium": [500, 100],
        "employee_monthly_cost": [150, -30],
        "source_enrollment_id": ["ENR-101", "ENR-102"],
        "effective_date": ["2026-01-01", "2026-01-01"]
    })

    # Act: Call the actual validation function
    accepted_df, rejected_df = validate_enrollments(df)

    # Assert: Verify the negative cost was rejected
    assert len(accepted_df) == 1
    assert len(rejected_df) == 1

    assert accepted_df.iloc[0]["employee_name"] == "John"
    assert rejected_df.iloc[0]["employee_name"] == "Sarah"
    assert "Negative Employee Monthly Cost" in rejected_df.iloc[0]["rejection_reason"]
