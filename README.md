# Telecom Billing Playwright Test Automation

## Project Overview

This project is a Playwright + Pytest + FastAPI test automation framework for a simulated telecom billing system.

It is built as a learning and portfolio project, with a structure that reflects common patterns used in production-style automation repositories:

- API testing with reusable API clients
- UI testing with Page Object Model
- E2E testing across frontend and backend
- Contract/schema testing for response validation
- Shared Pytest fixtures and test data reset
- FastAPI mock backend with in-memory data
- Static HTML/CSS/JavaScript frontend
- GitHub Actions CI

The current application covers invoice management, customer and contract lifecycle checks, monthly billing runs, and invoice risk badges.

Current full test suite result:

```text
68 passed
```

---

## Business Background

The application simulates a focused slice of a telecom Customer Care and Billing system.

In a real telecom billing environment, invoices are connected to customers, contracts, billing periods, payment status, monthly billing operations, and downstream financial processes. This project models those relationships in a compact mock application designed for automation practice.

Current business entities and concepts include:

- Invoice
- Customer
- Contract
- Billing run
- Billing period
- Invoice status
- Payment status
- Risk badge

Current invoice statuses:

- `Paid`
- `Unpaid`
- `Overdue`

Invoice risk mapping:

| Invoice Status | Risk Badge |
|---|---|
| `Paid` | `Low Risk` |
| `Unpaid` | `Medium Risk` |
| `Overdue` | `High Risk` |
| Fallback | `Unknown Risk` |

---

## Implemented Modules

### 1. Invoice Module

- Backend API
- Frontend invoice dashboard
- API client
- Page Object
- API tests
- UI tests
- E2E tests
- Contract/schema tests

### 2. Customer & Contract Lifecycle Module

- Backend API
- Frontend customer and contract lifecycle section
- API clients
- Page Object
- API tests
- UI tests
- E2E tests
- Contract/schema tests

### 3. Billing Run Module

- Backend API
- Billing Run API client
- API tests
- Contract/schema tests
- Billing Operations frontend section
- UI tests
- E2E test

### 4. Risk Badge / Status Badge

- Invoice table status badges
- Invoice table `Risk` column
- Risk mapping for `Paid`, `Unpaid`, `Overdue`, and fallback statuses
- UI coverage for low, medium, and high risk values

---

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| Test Framework | Pytest |
| Browser Automation | Playwright for Python |
| API Testing | Playwright APIRequestContext |
| Backend Mock App | FastAPI |
| Frontend Mock App | HTML, CSS, JavaScript |
| Test Architecture | Page Object Model, API Client abstraction |
| CI/CD | GitHub Actions |

---

## Test Strategy

The test suite is split into four layers.

### 1. API Tests

API tests validate backend behavior directly through reusable API clients.

They cover:

- Health check
- Listing, searching, filtering, and retrieving invoices
- Marking invoices as paid
- Creating and retrieving customers
- Creating, retrieving, and activating contracts
- Creating monthly billing runs
- Preventing duplicate billing-run invoice generation
- Verifying generated invoice status, billing period, and amount
- Handling unknown resource IDs

### 2. UI Tests

UI tests validate user-facing behavior in the browser through Page Objects.

They cover:

- Dashboard loading
- Invoice table rendering
- Searching invoices by customer or invoice ID
- Filtering invoices by status
- Marking an unpaid invoice as paid
- Customer and contract lifecycle UI behavior
- Billing Operations section loading
- Running monthly billing from the UI
- Generated invoices appearing after billing
- Risk Badge display for paid, unpaid, and overdue invoices

### 3. E2E Tests

E2E tests validate complete workflows across frontend and backend.

Current E2E flows:

- Mark an unpaid invoice as paid in the UI and verify the updated invoice through the API.
- Activate a draft contract in the UI and verify the contract status through the API.
- Run monthly billing from the UI, verify the billing run through the API, verify generated invoices through the API, and verify generated invoice risk in the UI.

### 4. Contract/Schema Tests

Contract tests validate API response shape and field types.

They cover:

- Invoice response fields, field types, and valid statuses
- Customer response fields, field types, and valid statuses
- Contract response fields, field types, valid statuses, and customer references
- Billing Run response fields, field types, valid status, generated invoice IDs, and duplicate-run response shape

---

## Project Structure

```text
telecom-billing-playwright-tests/
|-- app/
|   |-- frontend/
|   |   |-- index.html
|   |   `-- app.js
|   `-- backend/
|       |-- __init__.py
|       |-- main.py
|       `-- data.py
|-- api_clients/
|   |-- __init__.py
|   |-- billing_run_client.py
|   |-- contract_client.py
|   |-- customer_client.py
|   `-- invoice_client.py
|-- pages/
|   |-- __init__.py
|   |-- billing_dashboard_page.py
|   `-- customer_contract_page.py
|-- tests/
|   |-- api/
|   |   |-- test_billing_run_api.py
|   |   |-- test_customer_contract_api.py
|   |   `-- test_invoice_api.py
|   |-- contract/
|   |   |-- test_billing_run_schema.py
|   |   |-- test_customer_contract_schema.py
|   |   `-- test_invoice_schema.py
|   |-- e2e/
|   |   |-- test_billing_run_flow.py
|   |   |-- test_customer_contract_flow.py
|   |   `-- test_invoice_payment_flow.py
|   `-- ui/
|       |-- test_billing_dashboard_ui.py
|       `-- test_customer_contract_ui.py
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
|-- README.md
`-- .github/
    `-- workflows/
        `-- ci.yml
```

---

## Application Under Test

The mock application has a FastAPI backend and a static HTML/JavaScript frontend.

### Backend

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
| POST | `/api/customers` | Create a customer |
| GET | `/api/customers/{customer_id}` | Get customer by ID |
| POST | `/api/contracts` | Create a draft contract for an existing customer |
| GET | `/api/contracts/{contract_id}` | Get contract by ID |
| PATCH | `/api/contracts/{contract_id}/activate` | Activate a contract |
| POST | `/api/billing-runs` | Run monthly billing for a billing period |
| GET | `/api/billing-runs/{billing_run_id}` | Get billing run by ID |

### Frontend

Default URL:

```text
http://localhost:3000
```

The frontend includes:

- Invoice dashboard with search, status filter, payment action, status badge, and risk badge
- Customer & Contract Lifecycle section
- Billing Operations section for monthly billing runs

---

## Setup

### 1. Create and activate virtual environment

On Windows Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
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

Before tests that depend on a known state, the test suite calls:

```text
POST /api/test/reset
```

This resets invoices, customers, contracts, and billing runs.

Initial invoice data:

| Invoice | Customer | Contract | Amount | Status | Billing Period |
|---|---|---|---:|---|---|
| `INV-1001` | Alice Mobile | `CON-5001` | 89.00 | Paid | `2026-05` |
| `INV-1002` | Beta Telecom | `CON-5002` | 249.00 | Unpaid | `2026-05` |
| `INV-1003` | Delta GmbH | `CON-5003` | 399.00 | Overdue | `2026-05` |

Initial active contracts:

| Contract | Customer | Plan | Status |
|---|---|---|---|
| `CON-5001` | `CUST-001` | 5G Unlimited | Active |
| `CON-5002` | `CUST-002` | Fiber Business | Active |
| `CON-5003` | `CUST-003` | Business Mobile | Active |

This keeps tests independent and repeatable.

---

## Page Object Model

UI locators and common UI actions are encapsulated in Page Objects.

Current Page Objects:

- `pages/billing_dashboard_page.py`
- `pages/customer_contract_page.py`

Example responsibilities:

- Open the dashboard
- Search and filter invoices
- Locate invoice rows
- Mark an invoice as paid
- Verify invoice status and risk
- Run monthly billing from the UI
- Verify billing success messages
- Search customers and validate related contracts
- Activate draft contracts

This keeps UI and E2E test files focused on test intent instead of locator details.

---

## API Client Abstraction

API calls are encapsulated in reusable clients.

Current API clients:

- `api_clients/invoice_client.py`
- `api_clients/customer_client.py`
- `api_clients/contract_client.py`
- `api_clients/billing_run_client.py`

Example responsibilities:

- Health check
- Reset test data
- List, search, filter, retrieve, and pay invoices
- Create and retrieve customers
- Create, retrieve, and activate contracts
- Create and retrieve billing runs

This keeps API and E2E tests readable and reduces duplicated endpoint paths.

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
- `reset_test_data`
- `invoice_client`
- `customer_client`
- `contract_client`
- `billing_run_client`

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

### API Coverage

- Health check returns OK
- Invoice list, search, filter, detail, payment, and 404 behavior
- Customer creation, retrieval, and 404 behavior
- Contract creation, retrieval, activation, and 404 behavior
- Reset endpoint restores invoices, customers, contracts, and billing runs
- Billing run creation
- Billing run schema fields in API response
- Active contracts generate invoices
- Draft contracts are ignored by billing runs
- Generated invoices are unpaid
- Generated invoices use the requested billing period
- Generated invoice amounts match plan prices
- Duplicate billing runs do not create duplicate invoices
- Billing run retrieval and 404 behavior

### UI Coverage

- Invoice dashboard loads invoice table
- Search by customer name and invoice ID
- Filter by invoice status
- Mark unpaid invoice as paid
- Status badge behavior
- Risk Badge values for paid, unpaid, and overdue invoices
- Customer & Contract Lifecycle section loads
- Search existing and unknown customers
- Related contract display
- Draft contract activation from UI
- Billing Operations section loads
- Monthly billing can be run from UI
- Generated invoices appear in the table after billing
- Generated invoices show `Medium Risk`

### E2E Coverage

- Mark invoice as paid from UI and verify invoice status through API
- Activate draft contract from UI and verify contract status through API
- Run monthly billing from UI, verify billing run through API, verify generated invoices through API, and verify generated invoice risk in UI

### Contract/Schema Coverage

- Invoice response required fields and field types
- Invoice valid status values
- Invoice list object structure
- Customer response required fields, field types, and valid status values
- Contract response required fields, field types, valid status values, and customer references
- Billing Run response required fields and field types
- Billing Run valid status value
- Billing Run generated invoice ID structure
- Generated invoice IDs can be fetched through the invoice API
- Duplicate Billing Run response shape

---

## Roadmap

Planned future extensions:

### Partial Payment

- Support partial payment against an invoice
- Keep invoice open until fully paid
- Validate remaining balance

### Dunning

- Trigger dunning for overdue invoices
- Track dunning level
- Surface dunning state in customer account views

### Reporting / GL CSV Export

- Generate monthly GL reports
- Export GL reports as CSV
- Validate report totals and row-level data

### CI/CD Enhancements

- Separate API, UI, E2E, and contract jobs
- JUnit test report publishing
- Scheduled nightly regression runs
- Failure trace, screenshot, and video artifacts

---

## Project Goal

The goal of this project is to demonstrate a realistic, maintainable test automation setup for a business-oriented telecom billing scenario.

The focus is not only on writing UI tests, but also on building a layered automation framework with clear test responsibilities, reusable abstractions, stable test data, backend/frontend coverage, and CI execution.
