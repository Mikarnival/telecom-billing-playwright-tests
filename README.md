````md
# Telecom Billing Test Automation

A production-style QA automation project for a simulated telecom billing system.

The project started as a Playwright + Pytest automation framework and has gradually evolved into a broader quality engineering environment covering API, UI, E2E, schema validation, Selenium compatibility testing, BDD, Docker, CI/CD, and AWS staging deployment.

The goal is to practice not only test automation, but also the engineering work around automated testing: environment management, containerization, CI pipelines, deployment, post-deployment validation, and performance testing.

---

## Project Overview

The application simulates a focused part of a telecom Customer Care and Billing system.

The current business domain includes:

- invoices
- customers
- contracts
- billing periods
- monthly billing runs
- payment status
- invoice status
- invoice risk levels

The automation framework currently covers:

| Area | Implementation |
|---|---|
| API testing | Pytest + Playwright `APIRequestContext` |
| Contract/schema testing | Pytest |
| UI testing | Playwright for Python |
| E2E testing | Playwright + API verification |
| Compatibility testing | Selenium WebDriver |
| BDD | Gherkin + pytest-bdd |
| Backend | FastAPI |
| Frontend | HTML / CSS / JavaScript |
| Test architecture | Page Object Model + API Client abstraction |
| Containerization | Docker |
| Local orchestration | Docker Compose |
| CI | GitHub Actions |
| Container registry | GitHub Container Registry |
| CD | GitHub Actions |
| Cloud staging | AWS EC2 |
| Remote deployment | AWS Systems Manager |
| AWS authentication | GitHub OIDC |
| Post-deploy validation | Smoke checks |
| Performance testing | k6 — in progress |

---

## Current Delivery Architecture

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +-----------------------------+
    |                             |
    v                             v
Automated Test Jobs         Docker Image Build
    |                             |
    |                             v
    |                            GHCR
    |                             |
    +-------------+---------------+
                  |
                  v
            GitHub OIDC
                  |
                  v
             AWS IAM Role
                  |
                  v
        AWS Systems Manager
                  |
                  v
             EC2 Staging
                  |
                  v
           Docker Compose
            /          \
           v            v
       Backend       Frontend
       FastAPI        Nginx
           ^            |
           |            |
           +--- /api ---+
                  |
                  v
         Post-Deploy Smoke
````

The project therefore covers more than automated test execution.

The current engineering flow is:

```text
Code
  -> CI tests
  -> Docker image build
  -> GHCR
  -> AWS staging deployment
  -> post-deploy smoke testing
```

---

# Business Domain

## Invoice Management

The invoice module supports:

* listing invoices
* searching invoices
* filtering invoices by status
* retrieving invoice details
* marking invoices as paid
* displaying invoice status
* displaying invoice risk

Current invoice statuses:

```text
Paid
Unpaid
Overdue
```

Risk mapping:

| Invoice Status | Risk Badge     |
| -------------- | -------------- |
| `Paid`         | `Low Risk`     |
| `Unpaid`       | `Medium Risk`  |
| `Overdue`      | `High Risk`    |
| fallback       | `Unknown Risk` |

---

## Customer and Contract Lifecycle

The project models a basic customer and contract lifecycle.

Supported operations include:

* create customer
* retrieve customer
* create contract
* retrieve contract
* create draft contracts
* activate contracts
* validate customer-contract relationships

The lifecycle is covered through API, UI, schema, and E2E tests.

---

## Billing Run

The billing module simulates monthly telecom billing.

Current behavior includes:

* creating monthly billing runs
* retrieving billing runs
* generating invoices for active contracts
* ignoring draft contracts
* preventing duplicate invoice generation
* assigning billing periods
* calculating generated invoice amounts
* assigning generated invoices an initial unpaid status

Automated tests validate these behaviors through both the API and frontend.

---

# Test Strategy

The framework uses several test layers.

The goal is to validate behavior at the lowest useful level instead of using browser automation for every scenario.

```text
          E2E
           |
           |
          UI
           |
     API / Contract
           |
           |
       Backend
```

The repository also contains Selenium compatibility tests and a small BDD layer.

---

## API Tests

API tests validate backend behavior directly.

Reusable API clients wrap HTTP operations so test cases do not repeat endpoint URLs and request logic.

Current API coverage includes:

* backend health check
* invoice listing
* invoice search
* invoice filtering
* invoice detail retrieval
* invoice payment
* unknown invoice handling
* customer creation
* customer retrieval
* contract creation
* contract retrieval
* contract activation
* billing-run creation
* billing-run retrieval
* active-contract invoice generation
* draft-contract exclusion
* duplicate billing-run handling
* generated invoice validation
* negative and validation scenarios

---

## Contract / Schema Tests

Contract tests validate the structure of API responses independently from frontend behavior.

Current checks include:

* required fields
* field types
* valid enum/status values
* nested object structure
* customer references
* contract references
* generated invoice IDs
* billing-run structure
* duplicate billing-run response structure

This layer helps detect API contract changes even when the returned values are still technically valid HTTP responses.

---

## Playwright UI Tests

Playwright for Python is the primary browser automation tool in the project.

UI tests use Page Objects to separate browser implementation details from test intent.

Current UI coverage includes:

* dashboard loading
* invoice table rendering
* searching by customer
* searching by invoice ID
* filtering invoices by status
* marking an invoice as paid
* invoice status badges
* invoice risk badges
* customer lifecycle section
* contract lifecycle section
* customer search
* related contract display
* draft contract activation
* billing operations section
* running monthly billing
* displaying generated invoices

---

## End-to-End Tests

E2E tests verify workflows across multiple application layers.

Current E2E flows include:

### Invoice Payment

```text
UI
 -> mark invoice as paid
 -> API
 -> verify invoice status
```

### Contract Activation

```text
UI
 -> activate draft contract
 -> API
 -> verify contract state
```

### Monthly Billing

```text
UI
 -> run monthly billing
 -> API
 -> verify billing run
 -> API
 -> verify generated invoices
 -> UI
 -> verify generated invoice and risk
```

These tests validate integration between frontend behavior and backend state.

---

# Selenium Compatibility Testing

Selenium WebDriver is included as a secondary browser automation technology.

The project does not duplicate the full Playwright suite with Selenium.

Instead, Selenium is used for a small compatibility smoke layer.

This provides practical experience with:

* WebDriver lifecycle
* browser fixtures
* locators
* explicit waits
* browser interactions
* Selenium Page Objects
* headless execution
* CI execution

The Selenium tests run as a separate GitHub Actions job.

---

# BDD / Gherkin

The repository includes a minimal BDD implementation using:

```text
Gherkin
+
pytest-bdd
```

The purpose of this layer is to practice converting business-readable scenarios into executable tests.

Example structure:

```gherkin
Feature: Invoice search

  Scenario: Search an existing invoice
    Given the billing dashboard is open
    When the user searches for an invoice
    Then the invoice should be visible
```

BDD is intentionally kept small.

The complete automation suite is not converted into Gherkin because BDD is only useful when business-readable scenarios provide additional value.

---

# Smoke and Regression Strategy

The project distinguishes between fast feedback and broader regression testing.

## Smoke Tests

Smoke tests verify that the most important system functions are available.

Typical examples include:

* backend health
* frontend availability
* basic invoice retrieval
* critical browser workflow

Smoke tests are intended to fail quickly when the application is fundamentally unusable.

## Regression Tests

Regression tests provide broader coverage of application behavior.

They include:

* API behavior
* UI behavior
* contracts
* business workflows
* edge cases

## Post-Deploy Smoke

Post-deploy smoke tests are different from normal CI smoke tests.

They run only after the new application version has been deployed to the staging environment.

Their purpose is to answer:

```text
Was the application deployed successfully,
and is the deployed version actually usable?
```

---

# Tech Stack

| Area                         | Technology                             |
| ---------------------------- | -------------------------------------- |
| Main language                | Python                                 |
| Test framework               | Pytest                                 |
| Primary browser automation   | Playwright for Python                  |
| Secondary browser automation | Selenium WebDriver                     |
| API automation               | Playwright APIRequestContext           |
| BDD                          | pytest-bdd + Gherkin                   |
| Backend                      | FastAPI                                |
| Frontend                     | HTML / CSS / JavaScript                |
| Web server                   | Nginx                                  |
| Test architecture            | Page Object Model                      |
| API architecture             | Reusable API Client layer              |
| Configuration                | Pytest fixtures + environment settings |
| Containerization             | Docker                                 |
| Orchestration                | Docker Compose                         |
| CI/CD                        | GitHub Actions                         |
| Container registry           | GitHub Container Registry              |
| Cloud                        | AWS                                    |
| Staging compute              | EC2                                    |
| Remote execution             | AWS Systems Manager                    |
| Cloud authentication         | GitHub OIDC                            |
| Performance testing          | k6                                     |

---

# Project Structure

```text
telecom-billing-playwright-tests/
|
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|
|-- app/
|   |
|   |-- backend/
|   |   |-- Dockerfile
|   |   |-- __init__.py
|   |   |-- main.py
|   |   `-- data.py
|   |
|   `-- frontend/
|       |-- Dockerfile
|       |-- index.html
|       |-- app.js
|       `-- nginx.conf
|
|-- api_clients/
|   |-- invoice_client.py
|   |-- customer_client.py
|   |-- contract_client.py
|   `-- billing_run_client.py
|
|-- config/
|
|-- features/
|
|-- mcp_server/
|
|-- pages/
|
|-- tests/
|   |
|   |-- api/
|   |
|   |-- bdd/
|   |
|   |-- contract/
|   |
|   |-- e2e/
|   |
|   |-- selenium/
|   |
|   |-- smoke/
|   |
|   `-- ui/
|
|-- conftest.py
|-- docker-compose.yml
|-- docker-compose.staging.yml
|-- pytest.ini
|-- requirements.txt
`-- README.md
```

---

# Application Under Test

## Backend

The backend is implemented with FastAPI.

Default local URL:

```text
http://localhost:8000
```

Main endpoints include:

| Method | Endpoint                                | Purpose              |
| ------ | --------------------------------------- | -------------------- |
| GET    | `/health`                               | backend health check |
| POST   | `/api/test/reset`                       | reset test data      |
| GET    | `/api/invoices`                         | list invoices        |
| GET    | `/api/invoices?query=...`               | search invoices      |
| GET    | `/api/invoices?status=...`              | filter invoices      |
| GET    | `/api/invoices/{invoice_id}`            | retrieve invoice     |
| PATCH  | `/api/invoices/{invoice_id}/pay`        | mark invoice as paid |
| POST   | `/api/customers`                        | create customer      |
| GET    | `/api/customers/{customer_id}`          | retrieve customer    |
| POST   | `/api/contracts`                        | create contract      |
| GET    | `/api/contracts/{contract_id}`          | retrieve contract    |
| PATCH  | `/api/contracts/{contract_id}/activate` | activate contract    |
| POST   | `/api/billing-runs`                     | run monthly billing  |
| GET    | `/api/billing-runs/{billing_run_id}`    | retrieve billing run |

---

## Frontend

Default local URL:

```text
http://localhost:3000
```

The frontend includes:

* invoice dashboard
* invoice search
* status filtering
* invoice payment
* status badges
* risk badges
* customer and contract lifecycle
* billing operations

The Dockerized frontend uses Nginx.

Nginx also acts as a reverse proxy for backend API requests.

Example:

```text
Browser
   |
   v
Frontend / Nginx
   |
   +---- /
   |
   `---- /api/*
            |
            v
         Backend
```

---

# Local Setup

## Create Virtual Environment

Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Install Playwright Browser

```bash
playwright install chromium
```

---

# Run Application with Docker

The recommended local environment uses Docker Compose.

Build and start the application:

```bash
docker compose up -d --build --wait
```

Verify the backend:

```bash
curl http://localhost:8000/health
```

Verify the frontend:

```bash
curl http://localhost:3000
```

Open the application:

```text
http://localhost:3000
```

Stop the environment:

```bash
docker compose down
```

---

# Docker Health Checks

The backend container contains a health check.

Docker Compose waits for the backend to become healthy before starting dependent services.

Conceptually:

```text
backend starts
    |
    v
/health succeeds
    |
    v
backend = healthy
    |
    v
frontend starts
```

This reduces race conditions in local and CI environments.

---

# Running Tests

Run the complete Pytest suite:

```bash
pytest
```

Run API tests:

```bash
pytest -m api
```

Run contract tests:

```bash
pytest -m contract
```

Run Playwright UI tests:

```bash
pytest -m ui
```

Run E2E tests:

```bash
pytest -m e2e
```

Run Selenium tests:

```bash
pytest -m selenium
```

Run BDD scenarios:

```bash
pytest -m bdd
```

Run smoke tests:

```bash
pytest -m smoke
```

Run regression tests:

```bash
pytest -m regression
```

---

# Pytest Markers

Markers are defined in:

```text
pytest.ini
```

Current markers:

| Marker       | Purpose                       |
| ------------ | ----------------------------- |
| `api`        | API tests                     |
| `contract`   | API contract/schema tests     |
| `ui`         | Playwright UI tests           |
| `e2e`        | end-to-end business flows     |
| `selenium`   | Selenium compatibility tests  |
| `bdd`        | BDD scenarios                 |
| `smoke`      | critical fast-feedback tests  |
| `regression` | broader regression suite      |
| `billing`    | billing and invoice scenarios |
| `payment`    | payment and dunning scenarios |
| `staging`    | staging-specific tests        |

---

# Test Data Strategy

The backend currently uses in-memory test data.

Tests that depend on a known state can reset the backend using:

```text
POST /api/test/reset
```

The reset operation restores:

* invoices
* customers
* contracts
* billing runs

This makes automated tests more repeatable and reduces test-order dependencies.

Example initial invoice data:

| Invoice    | Customer     | Contract   | Amount | Status  | Billing Period |
| ---------- | ------------ | ---------- | -----: | ------- | -------------- |
| `INV-1001` | Alice Mobile | `CON-5001` |  89.00 | Paid    | `2026-05`      |
| `INV-1002` | Beta Telecom | `CON-5002` | 249.00 | Unpaid  | `2026-05`      |
| `INV-1003` | Delta GmbH   | `CON-5003` | 399.00 | Overdue | `2026-05`      |

---

# Framework Architecture

## API Client Layer

API operations are encapsulated in reusable client classes.

Current clients include:

```text
InvoiceClient
CustomerClient
ContractClient
BillingRunClient
```

Instead of writing:

```python
response = api_context.get(
    "http://localhost:8000/api/invoices/INV-1002"
)
```

directly in many tests, the tests can work with an abstraction such as:

```python
invoice_client.get_invoice("INV-1002")
```

This reduces:

* duplicated URLs
* duplicated request logic
* maintenance cost
* coupling between test logic and API implementation

---

# Page Object Model

UI locators and browser operations are encapsulated in Page Objects.

Typical Page Object responsibilities include:

* opening pages
* locating UI elements
* searching invoices
* filtering invoices
* marking invoices as paid
* reading invoice state
* running billing operations
* activating contracts

The test file can therefore focus on behavior.

Conceptually:

```text
Test
 |
 v
Page Object
 |
 v
Playwright / Selenium
 |
 v
Browser
```

---

# Shared Fixtures

Common test setup is managed with Pytest fixtures.

Shared fixture responsibilities include:

* API base URL
* frontend base URL
* API request context
* reusable API clients
* test-data reset
* browser lifecycle
* environment configuration

This reduces repeated setup code across the test suite.

---

# Continuous Integration

GitHub Actions runs the automated tests for pushes and pull requests to `main`.

The CI pipeline is divided into independent jobs.

Current jobs include:

```text
API Tests
Contract Tests
Playwright UI Tests
End-to-End Tests
Selenium Compatibility Smoke
```

The separation makes failures easier to classify.

For example:

```text
API job failed
    -> likely backend/API problem

Contract job failed
    -> likely response-contract change

UI job failed
    -> likely frontend/browser problem

E2E job failed
    -> likely integration/workflow problem

Selenium smoke failed
    -> likely compatibility/browser problem
```

---

# CI Test Environment

GitHub Actions does not depend on an external permanent test environment for the normal test jobs.

Instead, the application environment is created inside the CI runner with Docker Compose.

Example flow:

```text
GitHub Runner
     |
     v
docker compose up
     |
     +---- backend
     |
     `---- frontend
     |
     v
automated tests
     |
     v
docker compose down
```

This gives each CI run a clean and reproducible test environment.

---

# CI Artifacts

JUnit XML results are generated for the major test layers.

Examples:

```text
api-results.xml
contract-results.xml
ui-results.xml
e2e-results.xml
selenium-results.xml
```

GitHub Actions uploads these results as workflow artifacts.

For Playwright browser failures, the workflow can also retain debugging artifacts such as:

* screenshots
* traces
* test-result files

These artifacts help analyze failures that only occur in CI.

---

# Docker Image Build

When the main CI test jobs succeed on `main`, the workflow builds application images.

Current images:

```text
telecom-billing-backend
telecom-billing-frontend
```

The images are pushed to:

```text
GitHub Container Registry
```

or:

```text
GHCR
```

---

# Docker Image Versioning

Images use several tags.

Examples:

```text
latest
main
sha-<commit>
```

The SHA tag is important for deployment.

Instead of deploying:

```text
latest
```

the staging environment deploys a specific version such as:

```text
sha-a1b2c3d
```

This creates a direct relationship between:

```text
Git commit
    |
    v
CI result
    |
    v
Docker image
    |
    v
Staging deployment
```

The deployed application version can therefore be identified precisely.

---

# AWS Staging Environment

The project currently uses AWS EC2 as a small staging environment.

This environment is intended to simulate a real deployed test environment.

It is not the same as the temporary Docker environment inside GitHub Actions.

The two environments have different purposes.

```text
CI Docker environment
    |
    +--> temporary
    +--> isolated
    +--> created for test execution
    `--> destroyed after the job


AWS staging
    |
    +--> deployed environment
    +--> runs built application images
    +--> represents post-build deployment
    `--> used for post-deploy validation
```

---

# AWS Deployment Authentication

The deployment pipeline uses GitHub OIDC.

The workflow does not require permanent AWS access keys stored in GitHub.

Authentication flow:

```text
GitHub Actions
      |
      v
OIDC token
      |
      v
AWS IAM
      |
      v
AssumeRole
      |
      v
Temporary AWS credentials
```

This is safer than storing long-lived AWS credentials in repository secrets.

---

# AWS Systems Manager Deployment

GitHub Actions does not SSH directly into the EC2 instance.

Deployment commands are sent through AWS Systems Manager.

The flow is:

```text
GitHub Actions
      |
      v
AWS SSM
      |
      v
EC2
      |
      v
docker compose pull
      |
      v
docker compose up
```

The EC2 instance pulls the required images from GHCR.

---

# Staging Docker Compose

The local environment builds images from source.

The staging environment behaves differently.

Local:

```text
source code
   |
   v
docker build
   |
   v
containers
```

Staging:

```text
GHCR
  |
  v
pre-built versioned images
  |
  v
docker compose pull
  |
  v
containers
```

This is closer to a real CI/CD deployment process.

---

# Deployment Version Tracking

The deployed image tag is written to:

```text
/home/ubuntu/current-image-tag
```

Example:

```text
sha-a1b2c3d
```

This makes it possible to check which application version is currently running in staging.

---

# Post-Deploy Smoke Testing

A successful Docker deployment does not automatically mean that the application works correctly.

For this reason, the pipeline performs smoke checks after deployment.

Current staging checks include requests to:

```text
/
```

and:

```text
/api/invoices
```

The checks run on the EC2 instance through AWS Systems Manager.

Deployment pipeline:

```text
Build
  |
  v
Push Image
  |
  v
Deploy
  |
  v
Start Containers
  |
  v
Post-Deploy Smoke
  |
  +--> success -> deployment accepted
  |
  `--> failure -> deployment pipeline fails
```

---

# Nginx Reverse Proxy

The staging frontend container uses Nginx.

Nginx serves the frontend and forwards API requests to the backend container.

Conceptually:

```text
Client
   |
   v
Port 3000
   |
   v
Nginx
   |
   +-------- frontend files
   |
   `-------- /api/*
                |
                v
             backend
```

The backend does not need to be exposed as a separate public service in staging.

---

# MCP Server

The repository also contains a small MCP server for AI-assisted invoice lookup.

Current tool:

```text
get_invoice(invoice_id)
```

The tool calls:

```text
GET /api/invoices/{invoice_id}
```

and returns structured invoice information.

The MCP implementation is intentionally read-only.

It does not:

* modify invoices
* trigger billing runs
* execute tests
* execute shell commands
* control deployment

The MCP component is independent from the main CI/CD pipeline.

---

# Performance Testing

Performance testing is the current development area of the project.

k6 is being introduced for API load testing.

The first target is the invoice API.

Concepts being added include:

* virtual users
* iterations
* request rate
* ramp-up
* steady-state load
* response-time percentiles
* error rate
* thresholds
* load profiles

Planned performance scenarios include:

```text
Smoke Performance Test
        |
        v
Load Test
        |
        v
Stress Test
        |
        v
Spike Test
```

The performance test suite will first run against the local Docker environment.

Selected tests can later run against AWS staging.

---

# Current Engineering Status

## Test Automation

```text
[x] Pytest framework
[x] reusable fixtures
[x] reusable API clients
[x] Playwright UI tests
[x] Page Object Model
[x] API tests
[x] E2E tests
[x] contract/schema tests
[x] negative API scenarios
[x] validation tests
[x] Selenium smoke tests
[x] Selenium CI execution
[x] basic BDD / Gherkin implementation
```

## Containerization

```text
[x] backend Dockerfile
[x] frontend Dockerfile
[x] Docker Compose
[x] backend health check
[x] frontend/backend dependency handling
[x] Nginx frontend
[x] Nginx API reverse proxy
[x] staging-specific Docker Compose
```

## CI

```text
[x] GitHub Actions
[x] API test job
[x] contract test job
[x] Playwright UI job
[x] E2E job
[x] Selenium compatibility job
[x] JUnit artifacts
[x] Playwright failure artifacts
[x] Docker-based CI test environment
```

## CD

```text
[x] build backend image
[x] build frontend image
[x] push images to GHCR
[x] SHA image tagging
[x] AWS staging deployment
[x] GitHub OIDC authentication
[x] IAM deployment role
[x] AWS Systems Manager deployment
[x] EC2 Docker Compose deployment
[x] deployed-version tracking
[x] post-deploy smoke checks
```

## Performance / Cloud Testing

```text
[ ] complete first k6 load test
[ ] define performance thresholds
[ ] load-test profile
[ ] stress-test profile
[ ] spike-test profile
[ ] staging performance execution
[ ] performance result analysis
[ ] evaluate JMeter
[ ] evaluate BrowserStack / Sauce Labs
[ ] evaluate k6 Cloud or similar service
```

---

# Current Learning Roadmap

The current project roadmap focuses on automation engineering depth.

## Phase 1 — Java / JUnit / Cucumber-JVM

Java-side test automation is practiced in a separate Java project.

Topics include:

```text
Java
  |
  v
JUnit
  |
  v
Cucumber-JVM
```

The purpose is to complement the Python automation stack with technologies that frequently appear in enterprise QA environments.

---

## Phase 2 — Docker and CI/CD

This phase is largely implemented in this repository.

```text
Docker
  |
  v
Containerization
  |
  v
CI
  |
  v
Docker Image Build
  |
  v
GHCR
  |
  v
AWS Staging
  |
  v
Post-Deploy Smoke
```

Current status:

```text
mostly implemented
```

---

## Phase 3 — Performance and Cloud Testing

Current active development phase:

```text
k6 / JMeter
      |
      v
API Load Testing
      |
      v
Cloud Staging Testing
      |
      +--> BrowserStack / Sauce Labs
      |
      `--> k6 Cloud or similar services
```

---

## Phase 4 — Telecom API Testing Deepening

After the performance/cloud phase, the API layer will be expanded further.

Planned topics:

```text
authentication
      |
      v
authorization
      |
      v
schema validation
      |
      v
parameterization
      |
      v
boundary testing
      |
      v
cross-layer validation
```

Potential cross-layer tests may combine:

```text
API
 |
 v
Business state
 |
 v
UI / persistence / downstream validation
```

---

# Planned CI/CD Improvements

Possible next improvements include:

* Docker build caching
* multi-stage Docker builds where useful
* scheduled regression execution
* scheduled performance tests
* richer test reports
* deployment rollback strategy
* additional deployment health checks
* environment-specific test configuration
* staging-only automated tests

---

# Planned API Testing Improvements

The existing API suite already covers normal, negative, and schema scenarios.

The next API-focused phase will deepen coverage in areas such as:

* authentication
* authorization
* parameterized test data
* stronger schema validation
* boundary values
* invalid data combinations
* cross-entity validation
* cross-layer business validation

---

# Possible Future Telecom Features

Business functionality may also be extended later.

These features are secondary to the current automation-engineering roadmap.

Possible additions include:

## Partial Payment

```text
invoice amount
    |
    v
partial payment
    |
    v
remaining balance
    |
    v
invoice remains open
```

## Dunning

Possible workflow:

```text
Overdue invoice
      |
      v
Dunning Level 1
      |
      v
Dunning Level 2
      |
      v
Further collection action
```

## Reporting / GL Export

Possible functionality:

* monthly billing report
* GL-style CSV export
* row-level validation
* total validation
* reconciliation tests

---

# What This Project Demonstrates

The project is designed to demonstrate more than knowledge of one automation library.

It combines several QA engineering responsibilities:

```text
Business Test Design
        |
        v
API Automation
        |
        v
Contract Validation
        |
        v
Browser Automation
        |
        v
Cross-Layer E2E Testing
        |
        v
Compatibility Testing
        |
        v
Containerized Test Environment
        |
        v
Continuous Integration
        |
        v
Artifact / Image Management
        |
        v
Cloud Deployment
        |
        v
Post-Deployment Validation
        |
        v
Performance Testing
```

The project is therefore used as a practical environment for learning how automated tests fit into the wider software delivery lifecycle.

