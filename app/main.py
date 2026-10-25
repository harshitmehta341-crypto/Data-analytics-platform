
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import SalesRecord as SalesRecordDB

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Data & Analytics Platform",
    description="RESTful API for structured data and analytics",
    version="1.0.0",
)


class SalesRecordInput(BaseModel):
    product: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


def serialize_record(record: SalesRecordDB):
    return {
        "id": record.id,
        "product": record.product,
        "category": record.category,
        "quantity": record.quantity,
        "unit_price": record.unit_price,
        "total_value": record.quantity * record.unit_price,
    }


@app.get("/")
def home():
    return {
        "message": "Data & Analytics Platform is running",
        "status": "healthy",
    }


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/records", status_code=status.HTTP_201_CREATED)
def create_record(
    record: SalesRecordInput,
    db: Session = Depends(get_db),
):
    db_record = SalesRecordDB(**record.model_dump())

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return serialize_record(db_record)


@app.get("/api/v1/records")
def get_records(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
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

    total = db.query(SalesRecordDB).count()

    records = (
        db.query(SalesRecordDB)
        .order_by(SalesRecordDB.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": [serialize_record(r) for r in records],
    }


@app.get("/api/v1/records/{record_id}")
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    record = db.get(SalesRecordDB, record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return serialize_record(record)


@app.put("/api/v1/records/{record_id}")
def update_record(
    record_id: int,
    updated_record: SalesRecordInput,
    db: Session = Depends(get_db),
):
    record = db.get(SalesRecordDB, record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    for key, value in updated_record.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return serialize_record(record)


@app.delete("/api/v1/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    record = db.get(SalesRecordDB, record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {
        "message": "Record deleted successfully",
        "id": record_id,
    }
