# Blockchain-Enabled Security Enforcement Framework for DevSecOps Pipelines

A DevSecOps pipeline framework that integrates automated security
scanning, security-based deployment decisions, and blockchain-backed
logging into a CI/CD workflow.

## Project Status

The project is being developed incrementally. The current implementation
has established the application, containerization, baseline CI/CD
structure, and initial security-scanning stage. The security decision
engine, blockchain integration, and deployment enforcement are planned
next.

## Current Architecture
[![Architecture diagram](https://gitdiagram.com/diagram-badge.svg)](https://gitdiagram.com/aryasundaresh1/blockchain-devsecops?utm_source=readme&utm_medium=badge)

The final pipeline will use blockchain logging to create a
tamper-evident record of security decisions and pipeline outcomes.

## Current Repository Structure

``` text
blockchain-devsecops/
├── application/
│   ├── app.py
│   ├── requirements.txt
│   └── test_app.py
├── blockchain/
├── reports/
├── security/
├── Dockerfile
├── Jenkinsfile
└── README.md
```

Local development environments and generated files such as `venv/`,
`__pycache__/`, and `.pytest_cache/` are not part of the source code.

## Implemented So Far

### 1. Application

A basic Flask application has been created as the application under
test.

The application exposes:

-   `/` --- application status
-   `/health` --- health-check endpoint

Automated tests are available in:

``` text
application/test_app.py
```

The current test suite contains tests for both endpoints and has been
successfully executed locally with `pytest`.

### 2. Docker

Docker has been installed and verified locally.

The application has a Dockerfile so that the application can be packaged
and executed as a container.

The containerized application is intended to run on port `5000`.

### 3. CI/CD Foundation

Jenkins has been introduced as the CI/CD automation server.

The repository contains:

``` text
Jenkinsfile
```

The intended baseline pipeline is:

``` text
Checkout
   ↓
Install Dependencies
   ↓
Build
   ↓
Test
```

Jenkins uses the repository's `application/requirements.txt` to install
the Python dependencies before executing the tests.

### 4. Security Scanning

Initial security-scanning tools have been tested using Docker
containers.

#### SAST --- Semgrep

Semgrep has been successfully executed against the application source.

Purpose:

-   Static analysis of source code
-   Identification of potentially insecure coding patterns
-   Automated security findings for later use by the security decision
    engine

#### Secret Detection --- Gitleaks

Gitleaks has been successfully executed against the Git repository.

The current scan reported:

``` text
4 commits scanned
No leaks found
```

The scan was performed against the local Git history available at the
time of execution.

### 5. GitHub Integration

The project is maintained in a GitHub repository and is being used as
the source repository for the CI/CD pipeline.

## Security Pipeline --- Planned Integration

The complete security stage will contain four categories:

  -----------------------------------------------------------------------
  Security Component      Purpose                 Status
  ----------------------- ----------------------- -----------------------
  SAST                    Detect insecure         Initial Semgrep scan
                          source-code patterns    completed

  SCA                     Identify vulnerable     Planned
                          third-party             
                          dependencies            

  Secrets Detection       Detect accidentally     Gitleaks scan completed
                          committed secrets       

  Configuration /         Detect insecure         Planned
  Infrastructure Scan     configuration and       
                          infrastructure issues   
  -----------------------------------------------------------------------

The results from these scanners will eventually be passed to a central
**Security Decision Engine**.

## Security Decision Engine

The planned decision engine will:

1.  Collect security scan results.
2.  Normalize findings from different scanners.
3.  Assign or interpret severity levels.
4.  Determine whether the pipeline should continue.
5.  Block deployment when a configured high-severity security issue is
    detected.
6.  Record the security decision for auditability.

Conceptually:

``` text
Security Scan Results
        ↓
Security Decision Engine
        ↓
High-Severity Issue?
     /        \
   Yes         No
    ↓           ↓
 Block       Continue
Deployment    Pipeline
```

## Blockchain Integration --- Planned

The `blockchain/` directory is reserved for the blockchain component.

The planned blockchain layer will record security-related pipeline
events such as:

-   Build result
-   Security scan result
-   Security decision
-   Deployment decision
-   Timestamp / pipeline information

The purpose is to provide a tamper-evident audit trail rather than
storing the complete application or security reports directly on-chain.

## Deployment Enforcement --- Planned

The final pipeline is intended to enforce the security decision before
deployment:

``` text
Security Checks
      ↓
Security Decision
      ↓
 ┌────┴────┐
 │         │
Block     Pass
 │         │
 X         ↓
        Blockchain
        Logging
           ↓
        Deployment
```

A failed security decision should prevent the deployment stage from
executing.

## Technology Stack

-   **Application:** Python, Flask
-   **Testing:** Pytest
-   **Containerization:** Docker
-   **CI/CD:** Jenkins
-   **Source Control:** Git, GitHub
-   **SAST:** Semgrep
-   **Secret Detection:** Gitleaks
-   **Blockchain:** Planned
-   **SCA:** Planned
-   **Configuration / Infrastructure Security:** Planned

## Development Roadmap

### Phase 1 --- Application & Baseline CI/CD

-   [x] Create Flask application
-   [x] Add health/status endpoints
-   [x] Add automated tests
-   [x] Verify tests locally
-   [x] Create Dockerfile
-   [x] Verify Docker installation
-   [x] Create Jenkins pipeline foundation
-   [ ] Complete and verify Jenkins baseline pipeline end-to-end

### Phase 2 --- Security Gates

-   [x] Initial Semgrep scan
-   [x] Initial Gitleaks scan
-   [ ] Integrate SAST into Jenkins
-   [ ] Integrate SCA
-   [ ] Integrate configuration/infrastructure scanning
-   [ ] Generate structured security reports
-   [ ] Implement Security Decision Engine
-   [ ] Block deployment on configured high-severity findings

### Phase 3 --- Blockchain Audit Layer

-   [ ] Design blockchain data model
-   [ ] Implement blockchain logging
-   [ ] Record security decisions
-   [ ] Record deployment decisions
-   [ ] Verify audit records

### Phase 4 --- Complete DevSecOps Pipeline

-   [ ] Connect security decision engine to Jenkins
-   [ ] Connect blockchain logging to the pipeline
-   [ ] Enforce deployment blocking
-   [ ] Deploy only after successful security validation
-   [ ] Perform end-to-end testing
-   [ ] Document results and limitations

## Project Goal

The goal is to demonstrate how security can become an enforceable part
of a CI/CD pipeline rather than a separate manual activity.

The intended final workflow is:

``` text
GitHub
   ↓
Jenkins
   ↓
Build & Test
   ↓
Security Scanning
   ↓
Security Decision Engine
   ↓
Blockchain Audit Logging
   ↓
Deployment
```

with insecure builds being prevented from deployment based on the
configured security policy.

## Disclaimer

This repository is an academic/final-year project and is being developed
incrementally. Security tools, severity thresholds, blockchain
implementation, and deployment enforcement are being integrated and
validated as separate project phases.
