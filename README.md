# Telecom Billing Playwright Test Automation

## Project Overview

This project is a UI and API test automation framework for a simulated telecom billing system.

It is built as a learning and portfolio project, but its structure follows common patterns used in real test automation projects:

- API testing
- UI testing
- E2E testing
- Contract/schema testing
- Page Object Model
- API Client abstraction
- Shared Pytest fixtures
- GitHub Actions CI

The current application scope focuses on an invoice dashboard. Users can view invoices, search by customer or invoice ID, filter by invoice status, and mark an unpaid invoice as paid.

---

## Business Background

The application simulates a small part of a telecom Customer Care and Billing system.

In a real telecom billing environment, invoices are linked to customers, contracts, billing periods, payment status, and downstream financial processes. This project currently focuses on the invoice and payment-status part of that flow.

Current business entities include:

- Invoice
- Customer
- Contract
- Billing period
- Invoice status
- Payment status

Current invoice statuses:

- `Paid`
- `Unpaid`
- `Overdue`

---

## Tech Stack

| Area | Technology |
|---|---|
| Test Framework | Pytest |
| Browser Automation | Playwright for Python |
| API Testing | Playwright APIRequestContext |
| Backend Mock App | FastAPI |
| Frontend Mock App | HTML, CSS, JavaScript |
| CI/CD | GitHub Actions |
| Language | Python |

---

## Test Strategy

The test suite is split into four layers.

### 1. API Tests

API tests validate backend behavior directly.

They cover:

- Health check
- Listing invoices
- Searching invoices
- Filtering invoices by status
- Getting invoice details
- Marking an invoice as paid
- Handling unknown invoice IDs

### 2. UI Tests

UI tests validate user-facing behavior in the billing dashboard.

They cover:

- Dashboard loading
- Invoice table rendering
- Searching by customer name
- Searching by invoice ID
- Filtering by invoice status
- Marking an unpaid invoice as paid

### 3. E2E Tests

E2E tests validate a complete user flow across frontend and backend.

Current E2E flow:

```text
User marks an unpaid invoice as paid in the UI
        ↓
Frontend sends PATCH request to backend
        ↓
Backend updates invoice status
        ↓
UI shows updated status
        ↓
API verification confirms status is Paid
```

### 4. Contract Tests

Contract tests validate the API response structure.

They check:

- Required invoice fields
- Field data types
- Valid invoice status values
- Invoice list response structure

---

## Project Structure

```text
telecom-billing-playwright-tests/
│
├── app/
│   ├── frontend/
│   │   ├── index.html
│   │   └── app.js
│   │
│   └── backend/
│       ├── __init__.py
│       ├── main.py
│       └── data.py
│
├── api_clients/
│   ├── __init__.py
│   └── invoice_client.py
│
├── pages/
│   ├── __init__.py
│   └── billing_dashboard_page.py
│
├── tests/
│   ├── api/
│   │   └── test_invoice_api.py
│   │
│   ├── ui/
│   │   └── test_billing_dashboard_ui.py
│   │
│   ├── e2e/
│   │   └── test_invoice_payment_flow.py
│   │
│   └── contract/
│       └── test_invoice_schema.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Application Under Test

The mock application has two parts.

### Backend

The backend is a FastAPI application.

Default URL:

```text
http://localhost:8000
```

Main endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend availability |
| POST | `/api/test/reset` | Reset mock test data |
| GET | `/api/invoices` | List invoices |
| GET | `/api/invoices?query=Beta` | Search invoices |
| GET | `/api/invoices?status=Unpaid` | Filter invoices by status |
| GET | `/api/invoices/{invoice_id}` | Get invoice by ID |
| PATCH | `/api/invoices/{invoice_id}/pay` | Mark invoice as paid |

### Frontend

The frontend is a simple HTML/JavaScript dashboard.

Default URL:

```text
http://localhost:3000
```

The frontend calls the backend API and renders invoice data in a table.

---

## Setup

### 1. Create and activate virtual environment

On Windows Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browser

```bash
playwright install chromium
```

---

## Run the Application Locally

Open one terminal for the backend:

```bash
uvicorn app.backend.main:app --reload --port 8000
```

Open another terminal for the frontend:

```bash
python -m http.server 3000 --directory app/frontend
```

Then open the browser:

```text
http://localhost:3000
```

---

## Run Tests Locally

Make sure both backend and frontend are running before executing UI or E2E tests.

### Run all tests

```bash
pytest -v
```

### Run API tests

```bash
pytest -m api -v
```

### Run UI tests

```bash
pytest -m ui -v
```

### Run E2E tests

```bash
pytest -m e2e -v
```

### Run contract tests

```bash
pytest -m contract -v
```

### Run smoke tests

```bash
pytest -m smoke -v
```

---

## Test Markers

Markers are defined in `pytest.ini`.

| Marker | Meaning |
|---|---|
| `api` | API tests |
| `ui` | UI tests |
| `e2e` | End-to-end tests |
| `contract` | Contract/schema tests |
| `smoke` | Critical fast feedback tests |
| `regression` | Broader regression suite |
| `billing` | Billing and invoice related tests |
| `payment` | Payment and dunning related tests |

---

## Test Data Strategy

The backend uses in-memory mock data.

Before tests that depend on a known invoice state, the test suite calls:

```text
POST /api/test/reset
```

This resets the invoices to their initial state:

| Invoice | Customer | Amount | Status |
|---|---|---:|---|
| INV-1001 | Alice Mobile | 89.00 | Paid |
| INV-1002 | Beta Telecom | 249.00 | Unpaid |
| INV-1003 | Delta GmbH | 399.00 | Overdue |

This keeps tests independent and repeatable.

---

## Page Object Model

UI locators and common UI actions are encapsulated in:

```text
pages/billing_dashboard_page.py
```

Example responsibilities:

- Open dashboard
- Search invoice
- Filter by status
- Locate invoice rows
- Mark invoice as paid
- Verify invoice status
- Verify success message

This keeps UI test files focused on test intent instead of locator details.

---

## API Client Abstraction

API calls are encapsulated in:

```text
api_clients/invoice_client.py
```

Example responsibilities:

- Health check
- Reset test data
- List invoices
- Search invoices
- Filter invoices
- Get invoice by ID
- Mark invoice as paid

This keeps API tests readable and reduces duplicated endpoint paths.

---

## Shared Fixtures

Common fixtures are defined in:

```text
conftest.py
```

Current shared fixtures include:

- `frontend_base_url`
- `api_base_url`
- `api_context`
- `invoice_client`
- `reset_test_data`

---

## CI/CD

GitHub Actions is used to run the test suite automatically.

The workflow:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Installs Playwright Chromium
5. Starts the FastAPI backend
6. Starts the frontend static server
7. Waits until both services are available
8. Runs the Pytest suite
9. Uploads Playwright artifacts on failure

Workflow file:

```text
.github/workflows/ci.yml
```

---

## Current Test Coverage

### API

- Health check returns OK
- List invoices returns default invoices
- Search invoice by customer name
- Filter invoices by status
- Get invoice by ID
- Unknown invoice returns 404
- Mark invoice as paid
- Mark unknown invoice as paid returns 404

### UI

- Dashboard loads invoice table
- Search by customer name
- Search by invoice ID
- Filter unpaid invoices
- Filter paid invoices
- Filter overdue invoices
- Mark unpaid invoice as paid

### E2E

- Mark unpaid invoice as paid from UI and verify backend status through API

### Contract

- Invoice response contains required fields
- Invoice response field types are valid
- Invoice status has valid value
- Invoice list contains invoice objects with required fields

---

## Roadmap

Planned extensions:

### Customer & Contract Lifecycle

- Create customer
- Search customer
- Create contract for customer
- Activate contract
- Terminate contract
- Verify contract lifecycle status

### Billing Run

- Generate monthly invoice
- Validate invoice amount
- Prevent duplicate billing run
- Verify billing period

### Payment & Dunning

- Full payment closes invoice
- Partial payment keeps invoice open
- Overdue invoice triggers dunning
- Dunning level is visible in customer account

### Reporting & Export

- Download invoice PDF
- Generate monthly GL report
- Export GL report as CSV
- Validate report totals

### CI/CD Enhancements

- Separate API, UI, E2E, and contract jobs
- JUnit test report
- Scheduled nightly regression run
- Failure trace and screenshot artifacts

---

## Project Goal

The goal of this project is to demonstrate a realistic test automation setup for a business-oriented telecom billing scenario.

The focus is not only on writing UI tests, but also on building a maintainable testing structure with clear test layers, reusable abstractions, stable test data, and CI execution.