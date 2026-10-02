import json
import sys


REPORT_FILE = "security/reports/security_report.json"


def decision_engine(report):

    reasons = []

    # -----------------------------
    # SEMGREP
    # -----------------------------

    semgrep = report.get("semgrep", {})

    if semgrep.get("critical", 0) > 0:
        reasons.append(
            "Semgrep detected CRITICAL issues"
        )

    if semgrep.get("high", 0) > 0:
        reasons.append(
            "Semgrep detected HIGH issues"
        )

    # -----------------------------
    # GITLEAKS
    # -----------------------------

    gitleaks = report.get("gitleaks", {})

    if gitleaks.get("secrets", 0) > 0:
        reasons.append(
            "Gitleaks detected hardcoded secrets"
        )

    # -----------------------------
    # TRIVY
    # -----------------------------

    trivy = report.get("trivy", {})

    if trivy.get("critical", 0) > 0:
        reasons.append(
            "Trivy detected CRITICAL vulnerabilities"
        )

    if trivy.get("high", 0) > 0:
        reasons.append(
            "Trivy detected HIGH vulnerabilities"
        )

    # -----------------------------
    # CHECKOV
    # -----------------------------

    checkov = report.get("checkov", {})

    if checkov.get("failed_checks", 0) > 0:
        reasons.append(
            "Checkov detected failed security checks"
        )

    # -----------------------------
    # PIP-AUDIT
    # -----------------------------

    pip_audit = report.get("pip_audit", {})

    if pip_audit.get("vulnerabilities", 0) > 0:
        reasons.append(
            "pip-audit detected vulnerable dependencies"
        )

    # -----------------------------
    # FINAL DECISION
    # -----------------------------

    if reasons:
        return "BLOCK", reasons

    return "ALLOW", [
        "No blocking security findings detected"
    ]


def main():

    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        report = json.load(file)

    decision, reasons = decision_engine(report)

    print()
    print("=" * 70)
    print("                 SECURITY GATE")
    print("=" * 70)

    print()

    print("Scanner Results:")
    print("----------------")

    for scanner, values in report.items():
        print(f"{scanner.upper():12} : {values}")

    print()
    print("Decision:")
    print("--------")

    print(f"SECURITY DECISION: {decision}")

    print()

    print("Reason:")

    for reason in reasons:
        print(f"  - {reason}")

    print()
    print("=" * 70)

    if decision == "BLOCK":
        print("PIPELINE RESULT: BLOCKED")
        print("Deployment must NOT continue.")
        print("=" * 70)

        sys.exit(1)

    print("PIPELINE RESULT: ALLOWED")
    print("Deployment may continue.")
    print("=" * 70)

    sys.exit(0)


if __name__ == "__main__":
    main()