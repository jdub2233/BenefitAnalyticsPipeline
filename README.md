# Benefits Analytics Pipeline

An end-to-end data engineering and business intelligence portfolio project focused on employee benefits enrollment and cost analysis.

**Project Status:** In Development

## Project Overview

Benefits Analytics Pipeline is an ongoing portfolio project demonstrating how employee benefits enrollment data can be extracted, validated, transformed, and analyzed using Python and pandas.

The project is being developed incrementally alongside a structured technical learning curriculum, with future plans to incorporate PostgreSQL, automated ETL pipelines, Microsoft Fabric, and Power BI.

It builds on professional experience developing enterprise SaaS applications and working with employee benefits systems.

All employee data used in this project is entirely fictional.

## Project Goals

- Develop repeatable ETL pipelines using Python and pandas
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
- **Data Validation:** pandas filtering, duplicate detection, null checks, and validation rules
- **Analytics:** pandas aggregations, groupby operations, and pivot tables

### Planned

- PostgreSQL
- Microsoft Fabric Lakehouse and data pipelines
- Power BI
- DAX
- REST API integrations
- Automated ETL workflows
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
- Assigns descriptive rejection reasons to rejected records
- Supports multiple rejection reasons for a single record
- Exports accepted and rejected records to separate CSV files
- Verifies that accepted and rejected record counts reconcile with the source dataset

### Benefits Cost Analytics

- Calculates average, minimum, and maximum monthly benefit premiums
- Calculates total employee monthly benefit contributions
- Analyzes benefit costs by department and plan type
- Counts enrollments by benefit plan type
- Generates pivot tables showing departmental, plan-type, and grand totals
- Displays financial reports with currency formatting
- Exports departmental benefits cost reports to CSV
- Verifies that calculated report totals reconcile with the source data

**Current limitation:** Data validation and benefits cost analytics operate as separate scripts. The analytics script currently reads the original enrollment dataset rather than the accepted records produced by validation. Integrating these operations is the next development milestone.

## Project Structure

```text
BenefitAnalyticsPipeline/
├── data/
│   ├── raw/
│   │   └── benefits_enrollments.csv
│   ├── test/
│   │   └── benefits_enrollments_invalid.csv
│   └── processed/
│       ├── accepted_enrollments.csv
│       ├── rejected_enrollments.csv
│       └── department_benefits_costs.csv
├── src/
│   ├── extract/
│   │   └── generate_sample_data.py
│   ├── transform/
│   │   ├── analyze_benefits.py
│   │   └── validate_enrollments.py
│   └── load/
├── sql/
├── notebooks/
├── tests/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

Files under `data/processed/` are generated outputs and may not be present in a fresh clone of the repository. They are recreated by running the appropriate scripts.

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

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

All commands below assume that the virtual environment is activated and that you are running them from the project root directory.

### Generate Sample Data

Run the dataset generator:

```bash
python src/extract/generate_sample_data.py
```

The script generates:

`data/raw/benefits_enrollments.csv`

This dataset contains 20 fictional employee benefits enrollment records.

### Data Validation Pipeline

The project includes a pandas-based data validation script that identifies invalid employee benefit enrollment records before downstream processing.

#### Validation Rules

| Validation Rule | Description |
|---|---|
| Missing Employee ID | Reject records without an employee identifier |
| Duplicate Enrollment | Reject records sharing the same employee ID and benefit plan type |
| Negative Monthly Premium | Reject records with a monthly premium below zero |
| Negative Employee Cost | Reject records with a negative employee monthly contribution |
| Invalid Plan Type | Reject records containing unsupported benefit plan types |

Supported benefit plan types are:

- Medical
- Dental
- Vision

Records that fail validation are separated from accepted records and assigned descriptive rejection reasons.

If a record violates multiple validation rules, its rejection reasons are combined into a single field.

#### Running the Validation Pipeline

**Validate the normal enrollment dataset:**

```bash
python src/transform/validate_enrollments.py
```

**Validate the intentionally invalid test dataset:**

```bash
python src/transform/validate_enrollments.py data/test/benefits_enrollments_invalid.csv
```

The script accepts an optional CSV file path. If no path is provided, it uses the default dataset in `data/raw/`.

#### Output Files

The validation pipeline generates two files:

**Accepted Enrollments**

`data/processed/accepted_enrollments.csv`

Contains enrollment records that passed all validation checks.

**Rejected Enrollments**

`data/processed/rejected_enrollments.csv`

Contains enrollment records that failed one or more validation checks.

Rejected records include a `rejection_reason` column explaining why each record was rejected.

Example rejection reasons:

```text
Missing Employee ID
Duplicate Record
Negative Monthly Premium
Negative Employee Monthly Cost
Invalid Plan Type
Negative Monthly Premium; Invalid Plan Type
```

#### Validation Testing

A separate synthetic test dataset is maintained at:

`data/test/benefits_enrollments_invalid.csv`

This dataset intentionally contains invalid records to verify the validation logic.

The current test dataset contains 21 enrollment records.

| Validation Result | Record Count |
|---|---:|
| Total Records | 21 |
| Accepted Records | 15 |
| Rejected Records | 6 |

The test dataset includes examples of missing employee identifiers, duplicate enrollments, negative costs, invalid benefit plan types, and records with multiple validation failures.

The script includes a reconciliation assertion to ensure that every input record is accounted for:

```python
assert len(df) == len(accepted_df) + len(rejected_df)
```

This prevents records from being unintentionally lost during the validation process.

### Generate Benefits Analytics Report

After generating the sample enrollment data, run:

```bash
python src/transform/analyze_benefits.py
```

The script performs the following operations:

1. Reads the fictional employee enrollment dataset
2. Calculates premium and employee cost statistics
3. Analyzes enrollment data by department and plan type
4. Counts enrollments by benefit plan type
5. Generates a pivot table containing departmental and plan-type totals
6. Exports a CSV report
7. Verifies that the report total matches the source data

The generated report is saved to:

`data/processed/department_benefits_costs.csv`

Generated reports are excluded from Git because they can be recreated by running the scripts.

**Note:** The analytics script currently processes the original enrollment dataset. Integrating validated enrollment records into the reporting workflow is planned for the next development milestone.

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
- [x] Add record count reconciliation checks
- [ ] Integrate validated enrollment data into analytics reports

### Phase 3: Database and ETL Development

- [ ] Design PostgreSQL database schema
- [ ] Develop SQL queries for benefits analytics
- [ ] Load validated enrollment data into PostgreSQL
- [ ] Build a repeatable ETL pipeline

### Phase 4: Cloud and Business Intelligence

- [ ] Explore Microsoft Fabric Lakehouse integration
- [ ] Develop Microsoft Fabric data pipelines
- [ ] Build Power BI dashboards
- [ ] Create DAX measures for benefits analytics

### Phase 5: Integration and Software Engineering

- [ ] Integrate external data through REST APIs
- [ ] Add automated tests
- [ ] Add architecture documentation
- [ ] Improve error handling and logging

## Data Privacy

All employee names, enrollment records, and benefit costs are synthetic and created solely for demonstration purposes.

No real employee records or protected health information are used.

## Project Status

**In Development**

**Started:** October 26, 2026

**Latest Progress:** October 30, 2026

The project currently supports synthetic enrollment data generation, pandas-based validation with rejection reporting, and departmental benefits cost analysis.

The next development milestone is to integrate the validation and analytics workflows so that benefits cost reports use accepted enrollment records rather than unvalidated source data.

Future development will introduce PostgreSQL, repeatable ETL pipelines, Microsoft Fabric, Power BI, and additional software engineering practices.

This repository will be updated as new data engineering and analytics capabilities are implemented.
