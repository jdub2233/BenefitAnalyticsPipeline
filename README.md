
# Benefits Analytics Pipeline

An end-to-end data engineering and business intelligence portfolio
project focused on employee benefits enrollment and cost analysis.

## Project Overview

This project demonstrates how employee benefits enrollment data can
be extracted, cleaned, transformed, stored, and analyzed using
modern data engineering and analytics technologies.

The project is being developed incrementally alongside a structured
technical learning curriculum.

It builds on professional experience developing enterprise SaaS
applications and working with employee benefits systems.

All employee data used in this project is entirely fictional.

## Project Goals

- Develop repeatable ETL pipelines using Python and pandas
- Clean, validate, and transform employee benefits enrollment data
- Store and query structured data using PostgreSQL
- Explore Microsoft Fabric Lakehouse and data pipelines
- Build interactive Power BI dashboards using DAX
- Integrate external data through REST APIs
- Apply software engineering practices such as version control,
  testing, and documentation

## Technology Stack

### Currently Implemented
- Python
- pandas
- Git and GitHub
- CSV data generation

### Planned
- PostgreSQL
- Microsoft Fabric
- Power BI
- DAX
- REST API integrations
- Automated ETL workflows

## Current Functionality

The project currently includes:

- A Python script that generates fictional employee enrollment data
- A CSV dataset containing 20 enrollment records
- Employee information, departments, benefit plan types, and costs
- A structured project directory organized around ETL development
- Git version control and a public GitHub repository

## Project Structure

```text
BenefitAnalyticsPipeline/
├── data/
│   ├── raw/
│   │   └── benefits_enrollments.csv
│   └── processed/
├── src/
│   ├── extract/
│   │   └── generate_sample_data.py
│   ├── transform/
│   └── load/
├── sql/
├── notebooks/
├── tests/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/jdub2233/BenefitAnalyticsPipeline.git
cd BenefitAnalyticsPipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Generate Sample Data

Run the dataset generator from the project root:

```bash
python src/extract/generate_sample_data.py
```

The script generates:

`data/raw/benefits_enrollments.csv`

This CSV contains 20 fictional employee benefits enrollment records.

## Development Roadmap

- [x] Initialize project and Git repository
- [x] Create synthetic employee enrollment dataset
- [x] Publish repository to GitHub
- [ ] Implement pandas data validation and transformations
- [ ] Create benefits cost analysis reports
- [ ] Design PostgreSQL schema and SQL queries
- [ ] Build ETL pipeline
- [ ] Explore Microsoft Fabric integration
- [ ] Develop Power BI dashboards and DAX measures
- [ ] Add automated tests and architecture documentation

## Data Privacy

All employee names, enrollment records, and benefit costs are
synthetic and created solely for demonstration purposes.

No real employee records or protected health information are used.

## Project Status

**In Development**

Started October 26, 2026.

This repository will be updated as new data engineering and
analytics capabilities are implemented.
```
