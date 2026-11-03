# Benefits Analytics Pipeline

An end-to-end data engineering and business intelligence portfolio project focused on employee benefits enrollment and cost analysis.

**Project Status:** In Development

## Project Overview

Benefits Analytics Pipeline is an ongoing portfolio project demonstrating how fictional employee benefits enrollment data can be generated, validated, transformed, and analyzed using Python and pandas.

The project now includes a repeatable, two-stage pipeline that validates enrollment records before generating financial analytics. A single command runs validation followed by analytics, ensuring reports consume accepted records rather than the raw dataset.

The project builds on professional experience developing enterprise SaaS applications and working with employee benefits systems. Future development will incorporate PostgreSQL, more advanced ETL capabilities, Microsoft Fabric, and Power BI.

All employee data used in this project is entirely fictional.

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

- **Language:** Python
- **Data Processing:** pandas
- **Data Storage:** CSV files
- **Development Tools:** Visual Studio Code, Git, GitHub
- **Data Validation:** Null checks, duplicate detection, value checks, accepted/rejected record separation, and rejection reasons
- **Analytics:** pandas aggregations, `groupby`, and pivot tables
- **Pipeline Orchestration:** Python `subprocess` with sequential execution and failure propagation

### Planned

- PostgreSQL
- Microsoft Fabric Lakehouse and data pipelines
- Power BI and DAX
- REST API integrations
- Expanded ETL orchestration, logging, and error handling
- Automated testing with pytest

## Current Functionality

### Synthetic Data Generation

- Generates fictional employee benefits enrollment data
- Produces a CSV dataset containing 20 enrollment records
- Includes employee IDs, employee names, departments, benefit plan types, monthly premiums, and employee contributions
- Maintains a separate test dataset containing intentionally invalid records

### Data Validation

- Detects missing employee IDs
- Identifies duplicate enrollments based on employee ID and plan type
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

### Two-Stage Pipeline Runner

The `src/run_pipeline.py` entry point runs both processing stages in order:

1. **Validation:** Reads the normal raw enrollment dataset, applies validation rules, and exports accepted and rejected records.
2. **Analytics:** Reads the newly generated accepted records, calculates benefit cost statistics, and exports a departmental cost report.

The runner uses `subprocess.run(..., check=True)` so a nonzero exit status from validation stops the pipeline before analytics begins. Rejected enrollment records are handled as expected data-quality outcomes and do not, by themselves, cause the script to fail.

## Project Structure

```text
BenefitAnalyticsPipeline/
├── data/
│   ├── raw/
│   │   └── benefits_enrollments.csv
│   ├── test/
│   │   └── benefits_enrollments_invalid.csv
│   └── processed/                         # Generated outputs (not tracked)
│       ├── accepted_enrollments.csv
│       ├── rejected_enrollments.csv
│       └── department_benefits_costs.csv
├── src/
│   ├── extract/
│   │   └── generate_sample_data.py
│   ├── transform/
│   │   ├── analyze_benefits.py
│   │   └── validate_enrollments.py
│   ├── load/                              # Reserved for future database loading
│   └── run_pipeline.py
├── sql/                                   # Planned database scripts
├── notebooks/                             # Reserved for exploration
├── tests/                                 # Planned automated tests
├── docs/                                  # Planned architecture documentation
├── README.md
├── requirements.txt
└── .gitignore
```

The folders marked as planned or reserved represent the intended project organization and may be empty or absent from a fresh clone. Files under `data/processed/` are generated outputs, excluded from Git tracking, and recreated when the pipeline runs.

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

### Run the Complete Pipeline

**Recommended way to run the project:**

```bash
python src/run_pipeline.py
```

This single command:

1. Validates `data/raw/benefits_enrollments.csv`.
2. Writes accepted and rejected records to `data/processed/`.
3. Runs analytics using only `data/processed/accepted_enrollments.csv`.
4. Exports `data/processed/department_benefits_costs.csv`.
5. Checks that the analytics report total reconciles with the accepted enrollment data.

The runner stops if either script exits with an error. The current runner processes the **default raw dataset**; it does not yet accept a custom input-file argument.

**Expected results for the normal sample dataset:**

| Metric | Expected result |
|---|---:|
| Source records | 20 |
| Accepted records | 20 |
| Rejected records | 0 |
| Total employee monthly cost | $2,273.00 |
| Average monthly premium | $316.15 |

The pipeline should end with `PIPELINE COMPLETED SUCCESSFULLY`.

### Generate Sample Data

To regenerate the normal fictional enrollment dataset:

```bash
python src/extract/generate_sample_data.py
```

This creates `data/raw/benefits_enrollments.csv` with 20 fictional enrollment records. Run the complete pipeline afterward to refresh the processed outputs.

## Data Validation

### Validation Rules

| Validation rule | Description |
|---|---|
| Missing Employee ID | Reject records without an employee identifier |
| Duplicate Enrollment | Reject records sharing the same employee ID and benefit plan type |
| Negative Monthly Premium | Reject records with a monthly premium below zero |
| Negative Employee Cost | Reject records with a negative employee monthly contribution |
| Invalid Plan Type | Reject records containing unsupported benefit plan types |

Supported benefit plan types are **Medical**, **Dental**, and **Vision**.

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

### Validation Testing

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

This demonstrates that invalid records are excluded from downstream analytics. The test is currently run manually; automated regression tests are planned.

**Note:** Running the validator with the invalid test dataset overwrites the generated accepted/rejected CSVs, and the analytics script overwrites the generated cost report.

### Restore Normal Reports After Testing

Run:

```bash
python src/run_pipeline.py
```

This regenerates the processed outputs from the normal 20-record dataset and restores the expected $2,273.00 employee monthly cost total.

### Generated Outputs

The normal pipeline creates:

- `data/processed/accepted_enrollments.csv`
- `data/processed/rejected_enrollments.csv`
- `data/processed/department_benefits_costs.csv`

Generated CSV files are excluded from Git tracking and can be recreated at any time.

## Development Roadmap

### Phase 1: Project Foundation

- [x] Initialize project and Git repository
- [x] Create synthetic employee enrollment dataset
- [x] Publish repository to GitHub
- [x] Establish project directory structure

### Phase 2: Data Processing and Analytics

- [x] Implement pandas data validation and transformations
- [x] Create benefits cost analysis reports
- [x] Create intentionally invalid test data
- [x] Export accepted and rejected enrollment records
- [x] Implement rejection reason reporting
- [x] Support multiple rejection reasons per record
- [x] Add record-count reconciliation checks
- [x] Integrate validated enrollment data into analytics reports
- [x] Implement a two-stage pipeline runner
- [x] Verify integration using intentionally invalid enrollment data
- [x] Add financial reconciliation checks

### Phase 3: Database and ETL Development

- [ ] Design PostgreSQL database schema
- [ ] Develop SQL queries for benefits analytics
- [ ] Load validated enrollment data into PostgreSQL
- [ ] Extend the ETL workflow to include database loading

### Phase 4: Cloud and Business Intelligence

- [ ] Explore Microsoft Fabric Lakehouse integration
- [ ] Develop Microsoft Fabric data pipelines
- [ ] Build Power BI dashboards
- [ ] Create DAX measures for benefits analytics

### Phase 5: Integration and Software Engineering

- [ ] Integrate external data through REST APIs
- [ ] Add automated tests with pytest
- [ ] Add architecture documentation
- [ ] Improve error handling and logging

## Data Privacy

All employee names, enrollment records, and benefit costs are synthetic and created solely for demonstration purposes.

No real employee records or protected health information are used.

## Project Status

**In Development**

**Started:** October 26, 2026

**Latest Progress:** November 3, 2026

The project currently supports synthetic enrollment data generation, data-quality validation with rejection reporting, accepted-record-only financial analytics, CSV report generation, and a working two-stage pipeline executed with one command.

The next major development phase is PostgreSQL database design and loading validated enrollment data into relational tables. Future work will expand the ETL workflow and introduce Microsoft Fabric, Power BI, automated testing, and REST API integrations.

This repository will be updated as new data engineering and analytics capabilities are implemented.
