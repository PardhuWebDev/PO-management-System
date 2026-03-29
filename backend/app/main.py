from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routers import vendors, products, orders, auth, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PO Management System",
    description="Purchase Order Management with Vendors, Products, and Gen AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/auth",     tags=["Auth"])
app.include_router(vendors.router,  prefix="/vendors",  tags=["Vendors"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router,   prefix="/orders",   tags=["Purchase Orders"])
app.include_router(logs.router,     prefix="/logs",     tags=["AI Logs (MongoDB)"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "PO Management API is running"}
