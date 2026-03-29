from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


# ── Vendor ────────────────────────────────────────────────
class VendorBase(BaseModel):
    name:    str
    contact: str
    rating:  Optional[Decimal] = Field(None, ge=0, le=5)

class VendorCreate(VendorBase):
    pass

class VendorOut(VendorBase):
    id:         int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Product ───────────────────────────────────────────────
class ProductBase(BaseModel):
    name:        str
    sku:         str
    unit_price:  Decimal = Field(..., ge=0)
    stock_level: int     = Field(0, ge=0)
    category:    Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id:         int
    created_at: datetime

    class Config:
        from_attributes = True


# ── PO Item ───────────────────────────────────────────────
class POItemCreate(BaseModel):
    product_id: int
    quantity:   int = Field(..., gt=0)

class POItemOut(BaseModel):
    id:         int
    product_id: int
    quantity:   int
    unit_price: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True


# ── Purchase Order ────────────────────────────────────────
class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    items:     List[POItemCreate] = Field(..., min_length=1)

class PurchaseOrderStatusUpdate(BaseModel):
    status: str  # Draft | Confirmed | Received | Cancelled

class PurchaseOrderOut(BaseModel):
    id:           int
    reference_no: str
    vendor_id:    int
    vendor:       VendorOut
    subtotal:     Decimal
    tax_amount:   Decimal
    total_amount: Decimal
    status:       str
    items:        List[POItemOut]
    created_at:   datetime

    class Config:
        from_attributes = True


# ── Auth ──────────────────────────────────────────────────
class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "bearer"

class UserInfo(BaseModel):
    email: str
    name:  str
    picture: Optional[str] = None