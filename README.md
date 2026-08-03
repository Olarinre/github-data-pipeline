# GitHub Data Pipeline

A production-inspired ETL (Extract, Transform, Load) pipeline built with Python that collects repository data from the GitHub REST API, validates and transforms it, and loads it into a PostgreSQL database.

This project demonstrates core data engineering concepts including API integration, data validation, logging, idempotent database loading (upserts), scheduling, and pipeline orchestration.

---

## 🚀 Features

* Extracts repository data from the GitHub REST API
* Stores raw API responses as JSON
* Cleans and transforms data using Pandas
* Performs data quality validation before loading
* Loads data into PostgreSQL
* Uses PostgreSQL upserts to prevent duplicate records
* Logs pipeline execution and runtime metrics
* Records pipeline execution metadata
* Supports automated execution using APScheduler

---

## 🛠️ Tech Stack

* Python 3.12+
* PostgreSQL
* SQLAlchemy
* Pandas
* Requests
* APScheduler
* Tenacity
* Docker *(Coming Soon)*

---

## 📁 Project Structure

```text
github-data-pipeline/
│
├── app/
│   ├── etl/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── metadata.py
│   │   └── pipeline.py
│   │
│   ├── quality/
│   │   └── validator.py
│   │
│   ├── models.py
│   ├── database.py
│   ├── config.py
│   ├── logger.py
│   └── scheduler.py
│
├── data/
│   └── raw/
│
├── logs/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📊 ETL Workflow

```text
                 GitHub REST API
                        │
                        ▼
                Extract Repository Data
                        │
                        ▼
               Save Raw JSON Response
                        │
                        ▼
               Transform & Clean Data
                        │
                        ▼
              Data Quality Validation
                        │
                        ▼
         PostgreSQL (Upsert on Conflict)
                        │
                        ▼
          Pipeline Metadata & Logging
```

---

## ✅ Data Quality Checks

Before loading data into PostgreSQL, the pipeline validates:

* Required columns exist
* Required fields are not null
* Duplicate repositories are detected
* Numeric fields contain valid values
* Empty datasets are rejected

---

## 🗄️ Database Schema

### `repositories`

Stores repository information including:

* Repository name
* Owner
* Programming language
* Star count
* Fork count
* Open issues
* Repository creation date
* Last update date
* Pipeline execution timestamp

### `pipeline_runs`

Stores metadata for every pipeline execution:

* Pipeline name
* Start time
* End time
* Execution duration
* Status (Success / Failed)
* Rows extracted
* Rows loaded
* Error message (if applicable)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/github-data-pipeline.git

cd github-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=github_pipeline
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

GITHUB_TOKEN=your_github_personal_access_token
```

---

## ▶️ Running the Pipeline

Create the database tables:

```bash
python -m app.create_tables
```

Run the ETL pipeline:

```bash
python -m app.etl.pipeline
```

Run the scheduler:

```bash
python -m app.scheduler
```

---

## 📈 Current Capabilities

* ✅ GitHub API Extraction
* ✅ Data Transformation
* ✅ Data Validation
* ✅ PostgreSQL Loading
* ✅ Upsert Support
* ✅ Pipeline Logging
* ✅ Pipeline Orchestration
* ✅ Pipeline Metadata Tracking
* ✅ Scheduled Execution

---

## 🚧 Planned Improvements

* Docker Compose support
* FastAPI service
* Unit & Integration Tests
* GitHub Actions CI/CD
* Data Quality Reports
* Incremental Data Processing
* Monitoring Dashboard
* Apache Airflow orchestration

---

## 📚 Learning Objectives

This project was built to strengthen practical skills in:

* ETL Pipeline Development
* Data Engineering Best Practices
* PostgreSQL
* SQLAlchemy
* REST API Integration
* Pipeline Automation
* Data Validation
* Logging & Monitoring

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository, open an issue, or submit a pull request.

---

## 📄 License

This project is available for learning, educational, and portfolio purposes.
