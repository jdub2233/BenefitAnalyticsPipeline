import pandas as pd

def test_missing_employee_id():
    # Arrange: Create sample enrollment data
    df = pd.DataFrame({
        "employee_id": [101, None, 103],
        "employee_name": ["John", "Sarah", "Mike"]
    })

    # Act: Identify missing employee IDs
    missing_ids = df["employee_id"].isna()

    # Assert: Verify that exactly one record is missing an ID
    assert missing_ids.sum() == 1
