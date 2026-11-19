import os
import subprocess
import sys
from pathlib import Path

import psycopg
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TEST_DB_NAME = "benefits_analytics_test"

TEST_CSV = (
    PROJECT_ROOT
    / "data"
    / "test"
    / "accepted_enrollments_integration.csv"
)


def connect_to_test_db():
    # Never allow this helper to connect to the working database.
    if os.environ.get("DB_NAME") != TEST_DB_NAME:
        raise RuntimeError(
            "Integration tests must use benefits_analytics_test."
        )

    if os.environ.get("INTEGRATION_TEST") != "1":
        raise RuntimeError(
            "INTEGRATION_TEST must be enabled."
        )

    password = os.environ.get("DB_PASSWORD")

    if not password:
        raise RuntimeError("DB_PASSWORD is not configured.")

    return psycopg.connect(
        host="localhost",
        dbname=TEST_DB_NAME,
        user="postgres",
        password=password,
    )


@pytest.fixture
def clean_test_enrollment():
    source_id = "TEST-ENR-9999-001"

    def delete_test_enrollment():
        with connect_to_test_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM enrollments
                    WHERE source_enrollment_id = %s
                    """,
                    (source_id,),
                )

    # Setup: remove the test enrollment before execution.
    delete_test_enrollment()

    try:
        yield
    finally:
        # Teardown: remove the test enrollment after execution.
        delete_test_enrollment()

def run_enrollment_loader():
    # Explicitly configure the isolated test environment.
    env = os.environ.copy()
    env["DB_NAME"] = TEST_DB_NAME
    env["INTEGRATION_TEST"] = "1"
    env["ENROLLMENTS_CSV"] = str(TEST_CSV)

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "src" / "load" / "load_enrollments.py"),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout


def test_enrollment_loader_is_idempotent(clean_test_enrollment):
    # Safety: integration tests must use the isolated database.
    assert os.environ.get("DB_NAME") == TEST_DB_NAME
    assert os.environ.get("INTEGRATION_TEST") == "1"

    # Verify the test input exists.
    assert TEST_CSV.exists()

    # First run: the enrollment should be inserted.
    first_output = run_enrollment_loader()

    assert "Records processed: 1" in first_output
    assert "New enrollments inserted: 1" in first_output
    assert "Existing enrollments skipped: 0" in first_output

    # Verify the actual record exists in PostgreSQL.
    with connect_to_test_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM enrollments
                WHERE source_enrollment_id = %s
                """,
                ("TEST-ENR-9999-001",),
            )

            enrollment_count = cursor.fetchone()[0]

    assert enrollment_count == 1


    # Second run: the existing enrollment should be skipped.
    second_output = run_enrollment_loader()

    assert "Records processed: 1" in second_output
    assert "New enrollments inserted: 0" in second_output
    assert "Existing enrollments skipped: 1" in second_output

    # Verify PostgreSQL still contains exactly one enrollment.
    with connect_to_test_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM enrollments
                WHERE source_enrollment_id = %s
                """,
                ("TEST-ENR-9999-001",),
            )

            enrollment_count_after = cursor.fetchone()[0]

    assert enrollment_count_after == 1
