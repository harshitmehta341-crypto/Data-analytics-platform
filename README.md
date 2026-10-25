
![API Tests](https://github.com/harshitmehta341-crypto/Data-analytics-platform/actions/workflows/tests.yml/badge.svg)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/harshitmehta341-crypto/Data-analytics-platform)
# High-Performance RESTful Data & Analytics Platform

A Python-based REST API for managing sales records and generating analytical insights using FastAPI, SQLAlchemy, and SQLite. Includes automated API tests, pagination, SQL-based analytics, and performance benchmarking.

## Features

- **REST API:** Create, retrieve, update, and delete sales records.
- **Database persistence:** Store records in SQLite using SQLAlchemy ORM.
- **Analytics endpoints:** Generate revenue summaries, category-level analytics, and top-product reports using SQL aggregation.
- **Input validation:** Validate request data and reject invalid quantities or prices.
- **Pagination:** Retrieve records using limit and offset parameters with input validation.
- **Database indexing:** Index record IDs and categories to support data retrieval and category analytics.
- **Automated testing:** Test CRUD operations, pagination, input validation, and analytics using Pytest.
- **Load testing:** Simulate concurrent users and measure API response times with Locust.
- **Query benchmarking:** Compare analytics query execution times using a separate SQLite benchmark database.

## Tech Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Testing:** Pytest, FastAPI TestClient
- **Load Testing:** Locust
- **API Documentation:** OpenAPI / Swagger UI

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Check API health |
| POST | `/api/v1/records` | Create a sales record |
| GET | `/api/v1/records` | List records with pagination |
| GET | `/api/v1/records/{record_id}` | Retrieve one record |
| PUT | `/api/v1/records/{record_id}` | Update a record |
| DELETE | `/api/v1/records/{record_id}` | Delete a record |
| GET | `/api/v1/analytics/summary` | View overall analytics |
| GET | `/api/v1/analytics/categories` | Analyze sales by category |
| GET | `/api/v1/analytics/top-products` | Rank products by revenue |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/harshitmehta341-crypto/Data-analytics-platform.git
cd Data-analytics-platform
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

API base URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

## Automated Tests

Run the test suite from the project root:

```bash
python -m pytest -v
```

**Latest observed result:** 12 tests passed.

## Performance Testing with Locust

Start the API in one terminal, then run Locust in another:

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

Open `http://localhost:8089`, configure the number of simulated users and spawn rate, and start the test.

### Initial Local API Load Test

Observed during one local run with 10 simulated users:

| Metric | Result |
|---|---:|
| Total requests | 274 |
| Failed requests | 0 |
| Average response time | 6.69 ms |
| 95th-percentile response time | 11 ms |
| Maximum response time | 82 ms |
| Observed throughput | 5.4 requests/second |

These measurements represent one local test run, not a production capacity guarantee. Results depend on the machine, workload, data volume, and environment.

## Analytics Query Benchmark

Run the benchmark script from the project root:

```bash
python scripts/benchmark_analytics.py
```

The script creates a temporary SQLite database with 50,000 synthetic sales records and compares the average execution time of category and product aggregation queries with and without the corresponding index. It runs each query 10 times after a warm-up query.

### Initial Observed Results

| Query | Without index | With index | Observed change |
|---|---:|---:|---:|
| Category analytics | 27.568 ms | 17.502 ms | 36.5% faster |
| Top products | 13.043 ms | 13.889 ms | 6.5% slower |

In this run, the category index reduced the measured execution time, while the product index did not improve it. The results are preliminary and specific to one local run on synthetic data. Repeated controlled measurements on representative workloads are needed to establish reliable performance differences.

The benchmark uses a temporary database and does not modify the application's `data.db` file.

## Project Structure

```text
Data-analytics-platform/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── analytics.py
├── scripts/
│   └── benchmark_analytics.py
├── tests/
│   └── test_api.py
├── locustfile.py
├── requirements.txt
└── README.md
```

## Future Improvements

- Add authentication and authorization.
- Introduce structured logging and centralized error handling.
- Evaluate query performance on larger, representative datasets.
- Add database migrations and production database support.
- Add CI/CD and deploy the API to a cloud environment.
- Run repeatable load tests with documented workload and environment settings.

## Author

GitHub: [harshitmehta341-crypto](https://github.com/harshitmehta341-crypto)
