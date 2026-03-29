from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app import models, schemas
from app.database import get_db
from app.services.po_logic import create_purchase_order

router = APIRouter()

VALID_STATUSES = {"Draft", "Confirmed", "Received", "Cancelled"}


@router.get("/", response_model=List[schemas.PurchaseOrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    return (
        db.query(models.PurchaseOrder)
        .options(
            joinedload(models.PurchaseOrder.vendor),
            joinedload(models.PurchaseOrder.items)
        )
        .all()
    )


@router.get("/{order_id}", response_model=schemas.PurchaseOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(models.PurchaseOrder)
        .options(
            joinedload(models.PurchaseOrder.vendor),
            joinedload(models.PurchaseOrder.items)
        )
        .filter(models.PurchaseOrder.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return order


@router.post("/", response_model=schemas.PurchaseOrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    try:
        order = create_purchase_order(payload, db)
        # reload with relationships
        return get_order(order.id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/status", response_model=schemas.PurchaseOrderOut)
def update_order_status(
    order_id: int,
    payload: schemas.PurchaseOrderStatusUpdate,
    db: Session = Depends(get_db)
):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {VALID_STATUSES}"
        )

    order = db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.id == order_id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    try:
        order.status = payload.status
        db.commit()
        db.refresh(order)
        return get_order(order_id, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.PurchaseOrder).filter(
        models.PurchaseOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    if order.status == "Confirmed":
        raise HTTPException(status_code=400, detail="Cannot delete a Confirmed order")
    try:
        db.delete(order)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))