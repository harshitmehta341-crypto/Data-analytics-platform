
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SalesRecord

router = APIRouter(
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)


@router.get("/summary")
def analytics_summary(db: Session = Depends(get_db)):
    total_records = db.query(func.count(SalesRecord.id)).scalar() or 0

    total_revenue = (
        db.query(
            func.sum(SalesRecord.quantity * SalesRecord.unit_price)
        ).scalar()
        or 0
    )

    average_record_value = (
        db.query(
            func.avg(SalesRecord.quantity * SalesRecord.unit_price)
        ).scalar()
        or 0
    )

    return {
        "total_records": total_records,
        "total_revenue": round(float(total_revenue), 2),
        "average_record_value": round(float(average_record_value), 2),
    }


@router.get("/categories")
def category_analytics(db: Session = Depends(get_db)):
    results = (
        db.query(
            SalesRecord.category,
            func.count(SalesRecord.id).label("record_count"),
            func.sum(
                SalesRecord.quantity * SalesRecord.unit_price
            ).label("revenue"),
        )
        .group_by(SalesRecord.category)
        .order_by(
            func.sum(
                SalesRecord.quantity * SalesRecord.unit_price
            ).desc()
        )
        .all()
    )

    return {
        "categories": [
            {
                "category": row.category,
                "record_count": row.record_count,
                "revenue": round(float(row.revenue or 0), 2),
            }
            for row in results
        ]
    }


@router.get("/top-products")
def top_products(
    limit: int = Query(default=5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            SalesRecord.product,
            func.sum(
                SalesRecord.quantity * SalesRecord.unit_price
            ).label("revenue"),
        )
        .group_by(SalesRecord.product)
        .order_by(
            func.sum(
                SalesRecord.quantity * SalesRecord.unit_price
            ).desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "products": [
            {
                "product": row.product,
                "revenue": round(float(row.revenue or 0), 2),
            }
            for row in results
        ]
    }
