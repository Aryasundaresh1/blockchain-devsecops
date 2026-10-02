# Security Reports

This directory stores security scan reports generated automatically by
`security/run_security.py`.

The Security Module runs:

- Semgrep — Static Application Security Testing (SAST)
- Gitleaks — Secret detection
- Trivy — Container vulnerability scanning
- Checkov — Infrastructure/configuration scanning
- pip-audit — Python dependency vulnerability scanning

The generated JSON reports are intentionally excluded from Git using
`.gitignore`.

During the Jenkins pipeline, these reports are generated and combined into:

`security_report.json`

The combined report is then passed to the Security Decision Engine,
which produces an `ALLOW` or `BLOCK` decision.