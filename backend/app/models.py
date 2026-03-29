from sqlalchemy import (
    Column, Integer, String, Numeric, ForeignKey,
    DateTime, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    contact    = Column(String(255), nullable=False)
    rating     = Column(Numeric(2, 1))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One vendor → many purchase orders
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")


class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False)
    sku         = Column(String(100), unique=True, nullable=False)
    unit_price  = Column(Numeric(10, 2), nullable=False)
    stock_level = Column(Integer, default=0)
    category    = Column(String(100))
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    # One product → many PO line items
    po_items = relationship("POItem", back_populates="product")


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id           = Column(Integer, primary_key=True, index=True)
    reference_no = Column(String(50), unique=True, nullable=False)
    vendor_id    = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    subtotal     = Column(Numeric(10, 2), default=0)
    tax_amount   = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), default=0)
    status       = Column(String(50), default="Draft")
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    vendor = relationship("Vendor", back_populates="purchase_orders")
    items  = relationship("POItem", back_populates="purchase_order", cascade="all, delete-orphan")


class POItem(Base):
    __tablename__ = "po_items"

    id         = Column(Integer, primary_key=True, index=True)
    po_id      = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)  # price snapshot
    line_total = Column(Numeric(10, 2), nullable=False)  # quantity * unit_price

    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    product        = relationship("Product", back_populates="po_items")