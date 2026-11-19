# Benefits Analytics Pipeline

[![Python Unit Tests](https://github.com/jdub2233/BenefitAnalyticsPipeline/actions/workflows/python-tests.yml/badge.svg)](https://github.com/jdub2233/BenefitAnalyticsPipeline/actions/workflows/python-tests.yml)

An end-to-end data engineering and business intelligence portfolio project focused on employee benefits enrollment and cost analysis.

**Project Status:** Active Development


## Project Overview

Benefits Analytics Pipeline is an end-to-end data engineering and
business intelligence portfolio project that processes fictional
employee benefits enrollment data.

The project demonstrates a seven-stage ETL workflow using Python,
pandas, and PostgreSQL.

The pipeline:

1. Reads and validates enrollment records from CSV files.
2. Separates accepted and rejected records with rejection reasons.
3. Generates benefits cost analytics using pandas.
4. Loads departments, employees, benefit plans, and enrollments
   into PostgreSQL.
5. Prevents duplicate enrollment inserts during repeated loads.
6. Reconciles PostgreSQL enrollment records against the accepted CSV.
7. Reports pipeline success or failure.

The project includes seven automated pytest validation unit tests, one
PostgreSQL enrollment-loading integration test, and GitHub Actions
continuous integration (CI) for automatic unit testing.

An interactive Power BI dashboard provides enrollment and premium
analytics using the processed CSV data. Power BI is not yet
connected directly to PostgreSQL.

The project builds on professional experience developing enterprise
SaaS applications and working with employee benefits systems.

All employee data is entirely fictional.


## Project Goals

- Develop repeatable ETL workflows using Python and pandas
- Clean, validate, and transform employee benefits enrollment data
- Store and query structured data using PostgreSQL
- Explore Microsoft Fabric Lakehouse and data pipelines
- Build interactive Power BI dashboards using DAX
- Integrate external data through REST APIs
- Apply software engineering practices such as version control, testing, and documentation


## Technology Stack


### Currently Implemented

- **Language:** Python 3
- **Data Processing:** pandas
- **Relational Database:** PostgreSQL
- **Database Connectivity:** psycopg
- **Data Storage:** CSV files and PostgreSQL tables
- **Data Validation:** Missing values, duplicate detection,
  numeric validation, plan type validation, and date validation
- **Analytics:** pandas aggregations, groupby, and pivot tables
- **Pipeline Orchestration:** Python subprocess with sequential
  execution and failure propagation
- **Data Integrity:** PostgreSQL reconciliation against accepted
  CSV records and idempotent enrollment loading
- **Automated Testing:** pytest unit tests and PostgreSQL integration testing
- **Continuous Integration:** GitHub Actions (Python 3.13)
- **Business Intelligence:** Microsoft Power BI Desktop
- **Data Modeling and Calculations:** Power BI and DAX
- **Development Tools:** Visual Studio Code, Git, GitHub


### Planned

- Microsoft Fabric Lakehouse and OneLake integration
- Microsoft Fabric data pipelines
- REST API integrations
- Expanded automated testing and pipeline reliability
- Improved logging and error handling


## Current Functionality


### Synthetic Data Generation

- Generates fictional employee benefits enrollment data
- Generates synthetic enrollment records; the latest verified dataset contains 21 accepted enrollments
- Includes employee IDs, employee names, departments, benefit plan types, monthly premiums, and employee contributions
- Maintains a separate test dataset containing intentionally invalid records


### Data Validation

- Detects missing employee IDs
- Identifies duplicate enrollments using source_enrollment_id and rejects all records sharing a duplicate identifier
- Detects negative monthly benefit premiums
- Detects negative employee monthly contributions
- Identifies invalid benefit plan types
- Separates accepted and rejected enrollment records
- Assigns descriptive rejection reasons, including multiple reasons for a single record
- Exports accepted and rejected records to separate CSV files
- Verifies that accepted and rejected record counts reconcile with the input dataset


### Benefits Cost Analytics

- Reads **accepted enrollment records**, not the raw enrollment CSV
- Calculates average, minimum, and maximum monthly benefit premiums
- Calculates total employee monthly benefit contributions
- Analyzes benefit costs by department and plan type
- Counts enrollments by benefit plan type
- Generates pivot tables showing departmental, plan-type, and grand totals
- Displays financial reports with currency formatting
- Exports departmental benefits cost reports to CSV
- Verifies that calculated report totals reconcile with the accepted data


### Seven-Stage ETL Pipeline

The project uses `src/run_pipeline.py` to orchestrate seven
processing stages in sequence.

| Stage | Script | Responsibility |
|---|---|---|
| 1 | `validate_enrollments.py` | Validate raw enrollment records and separate accepted/rejected data |
| 2 | `analyze_benefits.py` | Generate benefits cost analytics using accepted records |
| 3 | `load_departments.py` | Load department records into PostgreSQL |
| 4 | `load_employees.py` | Load employee records into PostgreSQL |
| 5 | `load_benefit_plans.py` | Load benefit plan records into PostgreSQL |
| 6 | `load_enrollments.py` | Load validated enrollments into PostgreSQL |
| 7 | `reconcile_enrollments.py` | Compare PostgreSQL records against the accepted CSV |


#### Pipeline Execution

Run the complete pipeline from the project root:

```bash
python src/run_pipeline.py
```

The runner uses Python's `subprocess` module to execute each
stage sequentially.

If a stage exits with an error, the pipeline stops instead of
continuing with potentially incomplete or inconsistent data.

#### Data Quality and Integrity

The pipeline includes several safeguards:

- Invalid enrollment records are separated from accepted records.
- Downstream analytics use accepted enrollment data.
- PostgreSQL enrollment loading prevents duplicate inserts
  using `source_enrollment_id`.
- Repeated pipeline runs do not create duplicate enrollments.
- Reconciliation compares accepted CSV records with PostgreSQL.
- Missing records, duplicate identifiers, and field mismatches
  are reported as reconciliation failures.

This provides a repeatable ETL workflow with validation,
relational database loading, and post-load verification.


## Project Structure

```text
BenefitAnalyticsPipeline/
├── data/
│   ├── raw/
│   │   └── benefits_enrollments.csv
│   ├── test/
│   │   ├── benefits_enrollments_invalid.csv
│   │   └── accepted_enrollments_integration.csv
│   └── processed/
│       ├── accepted_enrollments.csv
│       ├── rejected_enrollments.csv
│       └── department_benefits_costs.csv
├── src/
│   ├── extract/
│   │   └── generate_sample_data.py
│   ├── transform/
│   │   ├── validate_enrollments.py
│   │   └── analyze_benefits.py
│   ├── load/
│   │   ├── load_departments.py
│   │   ├── load_employees.py
│   │   ├── load_benefit_plans.py
│   │   ├── load_enrollments.py
│   │   └── test_db_connection.py
│   ├── validation/
│   │   └── reconcile_enrollments.py
│   └── run_pipeline.py
├── tests/
│   ├── test_validate_enrollments.py
│   └── test_load_enrollments_integration.py
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── reports/
│   └── Benefits_Analytics_Dashboard.pbix
├── sql/
│   └── create_schema.sql
├── README.md
├── requirements.txt
├── pytest.ini
└── .gitignore
```

### Directory Responsibilities

- **data/raw/** — Original synthetic enrollment data.
- **data/test/** — Intentionally invalid enrollment records for testing.
- **data/processed/** — Generated accepted, rejected, and analytics CSV files.
- **src/extract/** — Synthetic data generation.
- **src/transform/** — pandas validation and analytics.
- **src/load/** — PostgreSQL database loading and connection testing scripts.
- **src/validation/** — Post-load database reconciliation.
- **tests/** — Automated pytest validation and PostgreSQL integration tests.
- **.github/workflows/** — GitHub Actions workflow for unit tests.
- **pytest.ini** — pytest test discovery and integration-test marker configuration.
- **reports/** — Power BI Desktop dashboard.
- **sql/** — PostgreSQL database schema creation script, including tables, primary keys, foreign keys, and constraints.

Generated files under `data/processed/` are excluded from Git tracking and recreated when the pipeline runs.
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip
- Git

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/jdub2233/BenefitAnalyticsPipeline.git
cd BenefitAnalyticsPipeline
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the virtual environment**

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

All commands below assume the virtual environment is activated and commands are run from the project root.



### PostgreSQL Configuration

The ETL pipeline requires PostgreSQL and a database named
`benefits_analytics`.

The repository includes a schema-only SQL script:

`sql/create_schema.sql`

This script creates the four required tables:

- `departments`
- `employees`
- `benefit_plans`
- `enrollments`

It also creates the primary keys, foreign keys, unique
constraints, and check constraints required by the pipeline.

#### 1. Create the Database

Connect to PostgreSQL using psql:

```powershell
psql -h localhost -U postgres -d postgres
```

Run:

```sql
CREATE DATABASE benefits_analytics;
```

Exit psql:

```text
\q
```

#### 2. Create the Database Schema

From the project root, run:

```powershell
psql -h localhost -U postgres -d benefits_analytics -v ON_ERROR_STOP=1 -f ".\sql\create_schema.sql"
```

This command creates the required database tables
and constraints.

**Important:** Run the schema script against a new,
empty database. Do not run it against an existing
database containing the project's tables.

#### 3. Configure the Database Password

The Python database loading scripts use the
`DB_PASSWORD` environment variable.

In Windows PowerShell:

```powershell
$env:DB_PASSWORD = Read-Host "Enter PostgreSQL password"
```

The environment variable applies to the current
PowerShell session.

Never commit database credentials to GitHub.

#### 4. Run the Pipeline

```powershell
python src/run_pipeline.py
```

The pipeline validates enrollment data, generates
analytics, loads PostgreSQL tables, and reconciles
database records against the accepted CSV.

### Schema Verification

The schema script was successfully restored into a
separate PostgreSQL 18.4 test database.

Verification confirmed:

- Four tables created successfully.
- 27 database constraints present.
- All four tables initially empty.
- No SQL errors during restoration.

The test database was used only to verify schema
reproducibility; the working database was not modified.


### Run the Complete Pipeline

**Recommended way to run the project:**

From the project root, with PostgreSQL running and
`DB_PASSWORD` configured:

```powershell
python src/run_pipeline.py
```

This command executes seven stages:

1. Validate raw enrollment records.
2. Generate benefits cost analytics from accepted records.
3. Load departments into PostgreSQL.
4. Load employees into PostgreSQL.
5. Load benefit plans into PostgreSQL.
6. Load accepted enrollments into PostgreSQL.
7. Reconcile PostgreSQL enrollments against the accepted CSV.

The runner stops if a processing stage fails.

Rejected enrollment records are expected data-quality
outcomes and do not automatically cause the pipeline to fail.

#### Latest Verified Results

The following results were verified during development
using the normal sample dataset:

| Metric | Result |
|---|---:|
| Accepted enrollment records | 21 |
| Rejected enrollment records | 0 |
| PostgreSQL reconciliation discrepancies | 0 |
| Automated validation tests passing | 7 of 7 |

The enrollment loading process is idempotent. Running
the same dataset again does not create duplicate
enrollment records.

#### Generated Outputs

The pipeline generates:

- `data/processed/accepted_enrollments.csv`
- `data/processed/rejected_enrollments.csv`
- `data/processed/department_benefits_costs.csv`

It also loads records into the PostgreSQL
`benefits_analytics` database.

The Power BI dashboard currently uses the accepted CSV
as its data source. Refresh the dashboard in Power BI
Desktop to display updated processed data.


### Generate Sample Data

To regenerate the normal fictional enrollment dataset:

```bash
python src/extract/generate_sample_data.py
```

This creates `data/raw/benefits_enrollments.csv` with 20 fictional enrollment records. Run the complete pipeline afterward to refresh the processed outputs.

## Data Validation


### Validation Rules

The pipeline applies seven data-quality validation rules
before records are accepted for downstream processing.

| Validation Rule | Description |
|---|---|
| Missing Employee ID | Reject records without a valid employee identifier |
| Duplicate Source Enrollment ID | Reject records sharing the same source enrollment identifier |
| Negative Monthly Premium | Reject records with a monthly premium below zero |
| Negative Employee Monthly Cost | Reject records with a negative employee contribution |
| Invalid Plan Type | Reject records containing unsupported benefit plan types |
| Invalid Effective Date | Reject records with invalid or missing effective dates |
| Missing Source Enrollment ID | Reject records without a valid source enrollment identifier |

Supported benefit plan types are **Medical**, **Dental**,
and **Vision**.

Duplicate detection uses `source_enrollment_id` rather than
employee ID and plan type.

When duplicate source enrollment IDs are detected, all
records sharing that identifier are rejected.

The validation logic is implemented in the reusable
`validate_enrollments(df)` function, which returns:

- `accepted_df`: Records passing all validation checks.
- `rejected_df`: Records failing one or more checks.

The validation script writes these DataFrames to separate
CSV files for downstream processing and investigation.


Records that fail one or more checks are separated from accepted records and assigned descriptive rejection reasons. When multiple rules fail, their reasons are combined in the `rejection_reason` field.

### Run Validation Independently

Validate the normal enrollment dataset:

```bash
python src/transform/validate_enrollments.py
```

Validate the intentionally invalid test dataset:

```bash
python src/transform/validate_enrollments.py data/test/benefits_enrollments_invalid.csv
```

The validation script accepts an optional CSV path. If omitted, it uses `data/raw/benefits_enrollments.csv`.

### Validation Output Files

**Accepted enrollments:** `data/processed/accepted_enrollments.csv`

Contains records that passed every implemented validation rule.

**Rejected enrollments:** `data/processed/rejected_enrollments.csv`

Contains records that failed at least one rule, including a `rejection_reason` column.

Example rejection reasons:

```text
Missing Employee ID
Duplicate Record
Negative Monthly Premium
Negative Employee Monthly Cost
Invalid Plan Type
Negative Monthly Premium; Invalid Plan Type
```

### Manual Validation Testing

The synthetic test dataset is stored at `data/test/benefits_enrollments_invalid.csv`. It includes missing employee identifiers, duplicate enrollments, negative premiums, negative employee costs, invalid plan types, and a record with multiple failures.

| Validation result | Record count |
|---|---:|
| Total records | 21 |
| Accepted records | 15 |
| Rejected records | 6 |

The validation script includes a record-count reconciliation assertion:

```python
assert len(df) == len(accepted_df) + len(rejected_df)
```

This confirms that each input record is accounted for in either the accepted or rejected output.


## Automated Testing and Continuous Integration

The project uses pytest to verify enrollment validation rules and
PostgreSQL enrollment loading. The two types of tests are separated
so routine unit testing does not require a running database.

### Unit Tests

`tests/test_validate_enrollments.py` contains seven tests using
in-memory pandas DataFrames and the production
`validate_enrollments(df)` function.

| Test Scenario | Expected Behavior |
|---|---|
| Missing employee ID | Reject enrollment |
| Negative monthly premium | Reject enrollment |
| Duplicate source enrollment ID | Reject all duplicate records |
| Invalid plan type | Reject enrollment |
| Invalid effective date | Reject enrollment |
| Missing or whitespace-only source enrollment ID | Reject enrollment |
| Negative employee monthly cost | Reject enrollment |

Run the default test suite from the project root:

```powershell
python -m pytest tests/ -v
```

The `pytest.ini` configuration excludes tests marked `integration`
by default. The latest verified default run reported **7 passed,
1 deselected**.

### PostgreSQL Integration Test

`tests/test_load_enrollments_integration.py` verifies that the
enrollment loader is idempotent: the first load inserts a fixture
enrollment and a repeated load does not create a duplicate.

The test uses an isolated `benefits_analytics_test` database and
`data/test/accepted_enrollments_integration.csv`. It requires a
running PostgreSQL instance, the project schema, the fixture's
referenced employee and benefit plan, and a database password.

For a new test database, create the database and restore the schema
using the instructions in **PostgreSQL Configuration**, substituting
`benefits_analytics_test` for `benefits_analytics`. Seed the referenced
employee, department, and benefit plan before running the test.

In Windows PowerShell, configure the environment for the isolated
test database:

```powershell
$env:DB_NAME = "benefits_analytics_test"
$env:INTEGRATION_TEST = "1"
$env:ENROLLMENTS_CSV = "data/test/accepted_enrollments_integration.csv"
$env:DB_PASSWORD = Read-Host "Enter PostgreSQL password"
```

Run only the integration test:

```powershell
python -m pytest tests/ -v -m integration
```

To run both unit and integration tests together (with the same
test database configuration):

```powershell
python -m pytest tests/ -v -m ""
```

The loader includes a safety guard that prevents integration-test
mode from targeting a database other than `benefits_analytics_test`.
Never run the integration test against the normal project database.

### GitHub Actions CI

The workflow at `.github/workflows/python-tests.yml` runs on pushes
to `main` and pull requests targeting `main`. It checks out the
repository, configures Python 3.13, installs `requirements.txt`,
and executes:

```bash
python -m pytest tests/ -v
```

CI deliberately runs only the seven unit tests. The PostgreSQL
integration test remains a separate, explicit local test and does
not require database credentials in GitHub Actions.

**Latest verified CI run (November 19, 2026):** GitHub Actions
workflow #2 succeeded after upgrading to `actions/checkout@v6`
and `actions/setup-python@v6`. The previous Node.js 20 deprecation
warning was not displayed on the new run summary.

[View GitHub Actions workflow runs](https://github.com/jdub2233/BenefitAnalyticsPipeline/actions/workflows/python-tests.yml)


## PostgreSQL Integration

The pipeline loads validated employee benefits data into
a PostgreSQL database named `benefits_analytics`.

### Database Tables

The database contains four primary tables:

| Table | Purpose |
|---|---|
| `departments` | Stores department information |
| `employees` | Stores employee information and department relationships |
| `benefit_plans` | Stores available benefit plans |
| `enrollments` | Stores employee benefit enrollments and associated costs |

### Database Loading

The pipeline uses Python and psycopg to connect to PostgreSQL.

Four loading scripts execute in sequence:

1. `src/load/load_departments.py`
2. `src/load/load_employees.py`
3. `src/load/load_benefit_plans.py`
4. `src/load/load_enrollments.py`

The loading order ensures that supporting records are
available before enrollment records are inserted.

### Idempotent Enrollment Loading

The enrollment loader uses `source_enrollment_id` as a
unique source identifier.

PostgreSQL's `ON CONFLICT` handling prevents the same
enrollment from being inserted multiple times.

This allows the enrollment loading step to be rerun
without creating duplicate enrollment records.

### Post-Load Reconciliation

After database loading, the pipeline executes:

`src/validation/reconcile_enrollments.py`

This script compares the accepted enrollment CSV against
the records stored in PostgreSQL.

Reconciliation checks include:

- Enrollment identifiers missing from PostgreSQL.
- Enrollment identifiers missing from the accepted CSV.
- Duplicate or null source enrollment identifiers.
- Differences in employee IDs.
- Differences in monthly premium amounts.
- Differences in employee monthly costs.
- Differences in effective dates.

Records are matched using `source_enrollment_id`.

If reconciliation detects a discrepancy, the script
reports the problem and fails the pipeline.

### Latest Verified Results

The latest successful pipeline execution verified:

| Reconciliation Metric | Result |
|---|---:|
| Accepted enrollment records | 21 |
| PostgreSQL enrollment records matched | 21 |
| Missing enrollment records | 0 |
| Field-level discrepancies | 0 |

The reconciliation process was also tested by deliberately
introducing a premium mismatch and confirming that the
pipeline detected the discrepancy.


## Benefits Analytics

### Run Analytics Independently

First run validation so the accepted-enrollment file exists and reflects the intended input:

```bash
python src/transform/validate_enrollments.py
python src/transform/analyze_benefits.py
```

The analytics script:

1. Reads `data/processed/accepted_enrollments.csv`.
2. Calculates premium and employee cost statistics.
3. Analyzes accepted enrollments by department and plan type.
4. Counts enrollments by benefit plan type.
5. Generates a pivot table containing departmental and plan-type totals.
6. Exports a CSV report.
7. Verifies that the report total matches the accepted data.

The generated report is saved to `data/processed/department_benefits_costs.csv`.

**Important:** Running analytics by itself reads the most recently generated accepted CSV, which may be stale. Prefer `python src/run_pipeline.py` for the normal workflow because it regenerates validated records immediately before analytics.

## End-to-End Integration Test


> **Historical testing note:** This section documents an earlier
> CSV validation and analytics integration test performed before
> PostgreSQL loading and reconciliation were added.
>
> The results below reflect the original 20-record sample dataset
> and its intentionally invalid test dataset. They are retained
> as evidence of earlier development and should not be interpreted
> as the latest pipeline results.
>
> The current seven-stage ETL pipeline has been verified with
> 21 accepted enrollments, zero PostgreSQL reconciliation
> discrepancies, and seven passing automated validation tests.


The pipeline was tested against both the normal dataset and the intentionally invalid dataset.

### Test Invalid Enrollment Data

Run validation using the test dataset, then analyze the accepted records:

```bash
python src/transform/validate_enrollments.py data/test/benefits_enrollments_invalid.csv
python src/transform/analyze_benefits.py
```

**Verified results:**

| Metric | Normal dataset | Invalid-data test |
|---|---:|---:|
| Input records | 20 | 21 |
| Records analyzed | 20 | 15 |
| Rejected records | 0 | 6 |
| Average monthly premium | $316.15 | $287.87 |
| Total employee monthly cost | $2,273.00 | $1,553.00 |
| Financial reconciliation | Passed | Passed |

This demonstrates that invalid records are excluded from downstream analytics. This historical CSV integration test was performed manually. Automated pytest tests now cover the seven core validation rules, and a separate PostgreSQL integration test verifies idempotent enrollment loading.

**Note:** Running the validator with the invalid test dataset overwrites the generated accepted/rejected CSVs, and the analytics script overwrites the generated cost report.

### Restore Normal Reports After Testing

Run:

```bash
python src/run_pipeline.py
```

This executes the current seven-stage pipeline using the
default raw enrollment dataset.

It regenerates the accepted and rejected enrollment CSV
files, updates the analytics reports, loads validated
records into PostgreSQL, and performs post-load
reconciliation.

The latest verified run processed 21 accepted enrollments
with zero PostgreSQL reconciliation discrepancies.

Results may change if the source dataset is modified.


### Generated Outputs

The normal pipeline creates:

- `data/processed/accepted_enrollments.csv`
- `data/processed/rejected_enrollments.csv`
- `data/processed/department_benefits_costs.csv`

Generated CSV files are excluded from Git tracking and can be recreated at any time.


## Power BI Dashboard

The project includes an interactive Power BI Desktop dashboard
for analyzing employee benefits enrollment data and costs.

### Dashboard File

`reports/Benefits_Analytics_Dashboard.pbix`

### Data Source

The dashboard currently imports validated enrollment data from:

`data/processed/accepted_enrollments.csv`

This ensures that reporting uses records that passed the
Python validation process.

Power BI is not yet connected directly to PostgreSQL.

After running the ETL pipeline, refresh the dataset in
Power BI Desktop to display updated enrollment data.

### Dashboard KPIs

The dashboard includes three primary KPI cards:

| KPI | Latest Verified Value |
|---|---:|
| Total Enrollments | 21 |
| Total Monthly Premiums | $6,408.00 |
| Average Monthly Premium | $305.14 |

These values represent the sample dataset used during
development and may change when the data is regenerated.

### Dashboard Visualizations

The dashboard includes:

- Monthly benefits premiums by department.
- Monthly benefits premiums by plan type.
- Department slicer for interactive filtering.
- Plan type slicer for interactive filtering.
- KPI cards that respond to report filters.

### DAX Calculations

The dashboard uses DAX to calculate benefits metrics.

For example, the average monthly premium measure:

```dax
Average Monthly Premium =
DIVIDE(
    SUM(accepted_enrollments[monthly_premium]),
    COUNTROWS(accepted_enrollments),
    0
)
```

This calculates the average monthly premium while
handling division by zero.

### Future Enhancements

Planned improvements include:

- Connecting Power BI directly to PostgreSQL.
- Exploring Microsoft Fabric Lakehouse integration.
- Building Fabric data pipelines.
- Expanding dashboard analytics and reporting.


## Development Roadmap

### Phase 1: Project Foundation — Complete

- [x] Initialize Git repository and project structure
- [x] Generate synthetic employee benefits enrollment data
- [x] Create intentionally invalid test data
- [x] Publish project to GitHub

### Phase 2: Python Data Processing — Complete

- [x] Implement pandas data validation
- [x] Separate accepted and rejected enrollment records
- [x] Add descriptive rejection reasons
- [x] Implement seven enrollment validation rules
- [x] Generate benefits cost analytics
- [x] Create departmental and plan-type pivot tables
- [x] Export processed CSV reports

### Phase 3: PostgreSQL and ETL — Complete

- [x] Create PostgreSQL relational database schema
- [x] Implement department loading
- [x] Implement employee loading
- [x] Implement benefit plan loading
- [x] Implement enrollment loading
- [x] Prevent duplicate enrollment inserts
- [x] Implement seven-stage ETL orchestration
- [x] Add PostgreSQL-to-CSV reconciliation
- [x] Verify repeatable pipeline execution
- [x] Export PostgreSQL schema to a version-controlled SQL script
- [x] Verify schema restoration in a separate test database


### Phase 4: Power BI — Initial Dashboard Complete

- [x] Import validated enrollment data into Power BI
- [x] Create enrollment and premium KPI cards
- [x] Create department and plan-type visualizations
- [x] Add interactive slicers
- [x] Implement DAX measures
- [ ] Connect Power BI directly to PostgreSQL

### Phase 5: Testing and Reliability — In Progress

- [x] Refactor validation logic into a reusable function
- [x] Add seven automated pytest validation tests
- [x] Verify PostgreSQL reconciliation
- [x] Test detection of database discrepancies
- [x] Add PostgreSQL enrollment-loading integration test
- [ ] Improve logging and error handling
- [x] Separate unit and integration tests using pytest markers
- [x] Add GitHub Actions CI for unit tests
- [x] Upgrade GitHub Actions to Node.js 24-compatible versions
- [ ] Finalize project documentation

### Phase 6: Microsoft Fabric — Planned

- [ ] Explore Microsoft Fabric Lakehouse
- [ ] Load project data into a Fabric Lakehouse
- [ ] Build Microsoft Fabric data pipelines
- [ ] Explore Fabric SQL analytics endpoints
- [ ] Integrate Fabric data with Power BI

### Phase 7: Additional Integrations — Planned

- [ ] Explore REST API data ingestion
- [ ] Expand analytics capabilities
- [ ] Complete portfolio presentation and documentation


## Data Privacy

All employee names, enrollment records, and benefit costs are synthetic and created solely for demonstration purposes.

No real employee records or protected health information are used.


## Project Status

**Status:** Active Development

**Started:** October 26, 2026

**Latest Verified Progress:** November 19, 2026

### Current Capabilities

The project includes a working seven-stage ETL pipeline
with Python, pandas, PostgreSQL, automated validation and database
integration tests, GitHub Actions CI, database reconciliation, and
an interactive Power BI dashboard.

The latest verified execution processed 21 accepted
enrollment records with zero reconciliation discrepancies.

All seven automated pytest validation tests passed in GitHub Actions;
the separate PostgreSQL integration test also passed locally.

### Current Development Focus

- Pipeline reliability and documentation
- Broader pipeline reliability testing and improved logging
- Microsoft Fabric integration
- Future Power BI connectivity improvements

All project data is synthetic and intended for learning
and portfolio demonstration.
