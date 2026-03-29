# PO Management System

A full-stack Purchase Order Management System built with FastAPI, PostgreSQL, and Vanilla JS — featuring Google OAuth, JWT authentication, and Gemini AI-powered product descriptions.

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3.11, FastAPI, SQLAlchemy    |
| Database   | PostgreSQL 15                       |
| Auth       | Google OAuth 2.0 + JWT              |
| AI         | Google Gemini 1.5 Flash (free tier) |
| Frontend   | HTML5, CSS3, Vanilla JS             |
| DevOps     | Docker, Docker Compose              |

---

## Project Structure

```
po-management/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py        # Env var loader (Pydantic Settings)
│   │   ├── database.py      # SQLAlchemy engine + session
│   │   ├── models.py        # ORM models (Vendor, Product, PurchaseOrder, POItem)
│   │   ├── schemas.py       # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   ├── auth.py      # Google OAuth + JWT
│   │   │   ├── vendors.py   # Vendor CRUD
│   │   │   ├── products.py  # Product CRUD + AI describe
│   │   │   └── orders.py    # Purchase Order CRUD + status update
│   │   └── services/
│   │       ├── po_logic.py  # Calculate Total business logic (5% tax)
│   │       └── gemini.py    # Gemini AI description generator
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                 # Environment variables (not committed)
├── frontend/
│   ├── index.html           # Login page
│   ├── dashboard.html       # PO dashboard with stats
│   ├── create_po.html       # Create PO form with dynamic rows
│   ├── css/style.css        # Shared dark theme styles
│   └── js/                  # (auth.js, po.js — utility scripts)
├── sql/
│   └── init.sql             # Schema + seed data (auto-runs on first Docker start)
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A Google Cloud account (for OAuth) — optional for dev mode
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com/app/apikey) — optional

---

### 1. Clone / Download the project

```bash
git clone https://github.com/your-username/po-management.git
cd po-management
```

---

### 2. Configure environment variables

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in:

```env
DATABASE_URL=postgresql://po_user:po_pass@db:5432/po_db

# Google OAuth (https://console.cloud.google.com → APIs & Services → Credentials)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# JWT
JWT_SECRET_KEY=any-random-string-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# Gemini AI (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-api-key

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5500
```

> **Dev mode:** You can leave Google and Gemini keys as dummy values to start — the app will run without them. Auth can be bypassed via the "Dev Mode" button on the login page. (Only I can Access).

---

### 3. Start the application

```bash
docker compose up --build
```

This will:
- Start a PostgreSQL 15 container and auto-run `sql/init.sql` (creates tables + seeds 3 vendors and 5 products)
- Build and start the FastAPI backend on port `8000`

---

### 4. Open the frontend

Open `frontend/index.html` with **VS Code Live Server** (right-click → Open with Live Server) or any static file server. It will run on `http://localhost:5500`.

- Click **⚡ Dev Mode** to skip auth and go straight to the dashboard
- Or click **Continue with Google** if you've configured OAuth

---

### 5. Verify the API

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Health check |
| `http://localhost:8000/docs` | Swagger UI — all endpoints |
| `http://localhost:8000/vendors/` | List seeded vendors |
| `http://localhost:8000/products/` | List seeded products |

---

## Database Design

### Schema Overview

```
vendors         products
   │                │
   │                │
   └──► purchase_orders ◄──┐
              │             │
              └──► po_items ┘
```

### Tables

**vendors** — Supplier information
```sql
id | name | contact | rating | created_at
```

**products** — Purchasable items with pricing
```sql
id | name | sku | unit_price | stock_level | category | created_at
```

**purchase_orders** — The PO header record
```sql
id | reference_no | vendor_id (FK) | subtotal | tax_amount | total_amount | status | created_at
```

**po_items** — Line items belonging to a PO
```sql
id | po_id (FK) | product_id (FK) | quantity | unit_price | line_total
```

### Design Decisions

**Why a separate `po_items` table?**
Proper normalization — a single PO can have multiple products. Storing items as a JSON column would make querying, filtering, and aggregation much harder.

**Why snapshot `unit_price` in `po_items`?**
Product prices can change over time. By copying the price at the moment of ordering, historical POs remain accurate even if a product's price is updated later.

**Why `ON DELETE RESTRICT` on vendor/product foreign keys?**
Prevents accidental deletion of a vendor or product that is referenced by existing orders, preserving data integrity.

**Why `ON DELETE CASCADE` on `po_items.po_id`?**
When a PO is deleted, its line items should be cleaned up automatically — they have no meaning without their parent order.

---

## Business Logic — Calculate Total

Located in `backend/app/services/po_logic.py`:

```
For each item in the PO:
  line_total = quantity × unit_price (fetched from DB at time of order)

subtotal   = Σ line_totals
tax_amount = subtotal × 5%
total      = subtotal + tax_amount
```

The tax calculation is enforced **on the backend** — the frontend displays a live preview but the authoritative calculation always happens server-side.

---

## API Endpoints

### Vendors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/vendors/` | List all vendors |
| GET | `/vendors/{id}` | Get single vendor |
| POST | `/vendors/` | Create vendor |
| PUT | `/vendors/{id}` | Update vendor |
| DELETE | `/vendors/{id}` | Delete vendor |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/` | List all products |
| GET | `/products/{id}` | Get single product |
| POST | `/products/` | Create product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| GET | `/products/{id}/describe` | AI-generate description via Gemini |

### Purchase Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders/` | List all orders |
| GET | `/orders/{id}` | Get single order |
| POST | `/orders/` | Create order (auto-calculates totals) |
| PATCH | `/orders/{id}/status` | Update order status |
| DELETE | `/orders/{id}` | Delete draft order |

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/login` | Redirect to Google OAuth |
| GET | `/auth/callback` | Handle OAuth callback, issue JWT |
| GET | `/auth/me?token=...` | Decode JWT, return user info |

---

## Gen AI Feature — Auto Description

Each product row in the Create PO form has a **Generate** button. Clicking it:

1. Calls `GET /products/{id}/describe` on the backend
2. Backend sends the product name + category to **Gemini 1.5 Flash**
3. Gemini returns a professional 2-sentence marketing description
4. Description appears inline below the product dropdown

If the Gemini API is unavailable or the key is missing, the endpoint falls back to a template description — the app never crashes.

---

## Stopping the application

```bash
docker compose down          # stop containers
docker compose down -v       # stop + delete database volume (fresh start)
```

---

## Setting up Google OAuth (optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → **APIs & Services** → **Credentials**
3. Create **OAuth 2.0 Client ID** (Web application)
4. Add Authorized redirect URI: `http://localhost:8000/auth/callback`
5. Copy Client ID and Secret into `backend/.env`

---

*Built for IV Innovations Private Limited assignment — ERP/MRP Module*