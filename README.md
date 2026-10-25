# High-Performance RESTful Data & Analytics Platform

A Python-based REST API for managing sales records and generating analytical insights using FastAPI, SQLAlchemy, and SQLite. Includes automated API tests and Locust-based performance testing.

## Features

- **REST API:** Create, retrieve, update, and delete sales records.
- **Database persistence:** Store records in SQLite using SQLAlchemy ORM.
- **Analytics endpoints:** Generate revenue summaries, category-level analytics, and top-product reports using SQL aggregation.
- **Input validation:** Validate request data and reject invalid quantities or prices.
- **Automated testing:** Test API operations, validation, and analytics using Pytest.
- **Performance testing:** Simulate concurrent users and measure API response times with Locust.

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
| GET | `/api/v1/records` | List sales records |
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

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

## Automated Tests

Run the test suite from the project root:

```bash
python -m pytest -v
```

**Current result:** 9 tests passed in the local test run.

## Performance Testing

Start the API in one terminal, then run Locust in another:

```bash
locust -f locustfile.py --host http://127.0.0.1:8000
```

Open `http://localhost:8089`, configure the number of simulated users and spawn rate, and start the test.

### Initial Local Benchmark

Observed during a local run with 10 simulated users:

| Metric | Result |
|---|---:|
| Total requests | 274 |
| Failed requests | 0 |
| Average response time | 6.69 ms |
| 95th-percentile response time | 11 ms |
| Maximum response time | 82 ms |
| Observed throughput | 5.4 requests/second |

These measurements represent one local test run and are not a production capacity guarantee. Results depend on the test duration, machine, data volume, and environment.

## Project Structure

```text
Data-analytics-platform/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── analytics.py
├── tests/
│   └── test_api.py
├── locustfile.py
├── requirements.txt
└── README.md
```

## Future Improvements

- Add database indexes and benchmark query performance.
- Add pagination, filtering, and sorting for record retrieval.
- Introduce authentication and authorization.
- Add structured logging and centralized error handling.
- Deploy the API and run tests in a production-like environment.

## Author

GitHub: [harshitmehta341-crypto](https://github.com/harshitmehta341-crypto)
