from decimal import Decimal
from sqlalchemy.orm import Session
from app import models, schemas
import uuid

TAX_RATE = Decimal("0.05")  # 5% tax


def generate_reference_no() -> str:
    """Generate a unique PO reference like PO-A1B2C3D4"""
    return f"PO-{uuid.uuid4().hex[:8].upper()}"


def calculate_totals(items: list[schemas.POItemCreate], db: Session) -> tuple:
    """
    For each item:
      - Fetch current unit_price from DB
      - Calculate line_total = quantity * unit_price
    Then:
      - subtotal   = sum of all line_totals
      - tax_amount = subtotal * 5%
      - total      = subtotal + tax_amount

    Returns (subtotal, tax_amount, total_amount, enriched_items)
    """
    enriched = []
    subtotal = Decimal("0.00")

    for item in items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()

        if not product:
            raise ValueError(f"Product with id {item.product_id} not found")

        unit_price = Decimal(str(product.unit_price))
        line_total = unit_price * item.quantity
        subtotal  += line_total

        enriched.append({
            "product_id": item.product_id,
            "quantity":   item.quantity,
            "unit_price": unit_price,
            "line_total": line_total,
        })

    tax_amount   = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
    total_amount = (subtotal + tax_amount).quantize(Decimal("0.01"))
    subtotal     = subtotal.quantize(Decimal("0.01"))

    return subtotal, tax_amount, total_amount, enriched


def create_purchase_order(payload: schemas.PurchaseOrderCreate, db: Session):
    """Full PO creation flow with totals calculation"""

    # 1. Verify vendor exists
    vendor = db.query(models.Vendor).filter(
        models.Vendor.id == payload.vendor_id
    ).first()
    if not vendor:
        raise ValueError(f"Vendor with id {payload.vendor_id} not found")

    # 2. Calculate totals
    subtotal, tax_amount, total_amount, enriched_items = calculate_totals(
        payload.items, db
    )

    # 3. Create PO record
    po = models.PurchaseOrder(
        reference_no = generate_reference_no(),
        vendor_id    = payload.vendor_id,
        subtotal     = subtotal,
        tax_amount   = tax_amount,
        total_amount = total_amount,
        status       = "Draft",
    )
    db.add(po)
    db.flush()  # get po.id before committing

    # 4. Create line items
    for item_data in enriched_items:
        po_item = models.POItem(
            po_id      = po.id,
            **item_data
        )
        db.add(po_item)

    db.commit()
    db.refresh(po)
    return po