
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Data & Analytics Platform",
    description="RESTful API for structured data and analytics",
    version="1.0.0",
)


# 1. Define the data structure
class SalesRecord(BaseModel):
    product: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


# 2. Temporary in-memory storage
records: dict[int, SalesRecord] = {}
next_id = 1


@app.get("/")
def home():
    return {
        "message": "Data & Analytics Platform is running",
        "status": "healthy",
    }


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


# CREATE: Add a sales record
@app.post("/api/v1/records", status_code=status.HTTP_201_CREATED)
def create_record(record: SalesRecord):
    global next_id

    record_id = next_id
    records[record_id] = record
    next_id += 1

    return {
        "id": record_id,
        **record.model_dump(),
        "total_value": record.quantity * record.unit_price,
    }


# READ: Get all records with pagination
@app.get("/api/v1/records")
def get_records(limit: int = 10, offset: int = 0):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100",
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset cannot be negative",
        )

    items = list(records.items())
    selected = items[offset:offset + limit]

    return {
        "total": len(records),
        "limit": limit,
        "offset": offset,
        "data": [
            {
                "id": record_id,
                **record.model_dump(),
                "total_value": record.quantity * record.unit_price,
            }
            for record_id, record in selected
        ],
    }


# READ: Get one record by ID
@app.get("/api/v1/records/{record_id}")
def get_record(record_id: int):
    record = records.get(record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return {
        "id": record_id,
        **record.model_dump(),
        "total_value": record.quantity * record.unit_price,
    }


# UPDATE: Replace an existing record
@app.put("/api/v1/records/{record_id}")
def update_record(record_id: int, updated_record: SalesRecord):
    if record_id not in records:
        raise HTTPException(status_code=404, detail="Record not found")

    records[record_id] = updated_record

    return {
        "id": record_id,
        **updated_record.model_dump(),
        "total_value": updated_record.quantity * updated_record.unit_price,
    }


# DELETE: Remove a record
@app.delete("/api/v1/records/{record_id}")
def delete_record(record_id: int):
    if record_id not in records:
        raise HTTPException(status_code=404, detail="Record not found")

    del records[record_id]

    return {
        "message": "Record deleted successfully",
        "id": record_id,
    }
