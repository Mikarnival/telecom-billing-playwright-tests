# Telecom Billing Playwright Test Automation

## Project Overview

This project is a UI and API test automation framework for a simulated telecom billing system.  
It is built with Python, Pytest, Playwright, and FastAPI.

The project focuses on invoice search, invoice status filtering, payment status updates, API validation, UI validation, and UI/API consistency checks.

## Business Background

The application simulates a small part of a telecom Customer Care and Billing system.  
The current scope covers invoice data, customer names, contract IDs, billing periods, invoice status, and payment status changes.

## Tech Stack

- Python
- Pytest
- Playwright
- FastAPI
- GitHub Actions

## Test Types

- API tests
- UI tests
- E2E tests
- Contract tests
- Smoke tests

## Project Structure

```text
app/
  frontend/
    index.html
    app.js
  backend/
    main.py
    data.py

api_clients/
  invoice_client.py

pages/
  billing_dashboard_page.py

tests/
  api/
  ui/
  e2e/
  contract/