import json
import os
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)


def run_command(command, output_file=None):
    print("\n" + "=" * 70)
    print("RUNNING:")
    print(" ".join(command))
    print("=" * 70)

    result = subprocess.run(
        command,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if output_file and output_file.exists():
        print(f"Report created: {output_file}")

    return result.returncode


def run_semgrep():
    output = REPORT_DIR / "semgrep.json"

    command = [
        "docker", "run", "--rm",
        "-v", f"{PROJECT_DIR}:/src",
        "semgrep/semgrep",
        "semgrep", "scan",
        "--config=auto",
        "--json",
        "--output", "/src/security/reports/semgrep.json",
        "/src/application"
    ]

    return run_command(command, output)


def run_gitleaks():
    output = REPORT_DIR / "gitleaks.json"

    command = [
        "docker", "run", "--rm",
        "-v", f"{PROJECT_DIR}:/repo",
        "zricethezav/gitleaks:latest",
        "detect",
        "--source=/repo",
        "--report-format=json",
        "--report-path=/repo/security/reports/gitleaks.json",
        "--exit-code=0"
    ]

    return run_command(command, output)


def run_trivy():
    output = REPORT_DIR / "trivy.json"

    command = [
        "docker", "run", "--rm",
        "-v", f"{PROJECT_DIR}:/work",
        "aquasec/trivy",
        "image",
        "--format", "json",
        "--output", "/work/security/reports/trivy.json",
        "devsecops-app"
    ]

    return run_command(command, output)


def run_checkov():
    output = REPORT_DIR / "checkov.json"

    command = [
        "docker", "run", "--rm",
        "-v", f"{PROJECT_DIR}:/src",
        "bridgecrew/checkov",
        "-d", "/src",
        "-o", "json",
        "--output-file-path", "/src/security/reports/checkov.json"
    ]

    return run_command(command, output)


def run_pip_audit():
    output = REPORT_DIR / "pip_audit.json"

    command = [
        "docker", "run", "--rm",
        "-v", f"{PROJECT_DIR}:/src",
        "python:3.12-slim",
        "bash",
        "-c",
        (
            "pip install pip-audit -q && "
            "pip-audit "
            "-r /src/application/requirements.txt "
            "--format=json "
            "--output=/src/security/reports/pip_audit.json "
            "|| true"
        )
    ]

    return run_command(command, output)


def safe_read_json(file_path):
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return {}


def count_semgrep(data):
    counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for finding in data.get("results", []):
        severity = finding.get("extra", {}).get("severity", "").lower()

        if severity == "error":
            counts["high"] += 1
        elif severity == "warning":
            counts["medium"] += 1

    return counts


def count_gitleaks(data):
    if isinstance(data, list):
        return {
            "secrets": len(data)
        }

    return {
        "secrets": 0
    }


def count_trivy(data):
    counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for result in data.get("Results", []):
        for vulnerability in result.get("Vulnerabilities", []) or []:

            severity = vulnerability.get(
                "Severity", ""
            ).lower()

            if severity in counts:
                counts[severity] += 1

    return counts


def count_checkov(data):
    return {
        "failed_checks": len(
            data.get("results", {}).get("failed_checks", [])
        )
    }


def count_pip_audit(data):
    vulnerabilities = data.get("dependencies", [])

    count = 0

    for dependency in vulnerabilities:
        count += len(dependency.get("vulns", []))

    return {
        "vulnerabilities": count
    }


def create_combined_report():

    semgrep = safe_read_json(
        REPORT_DIR / "semgrep.json"
    )

    gitleaks = safe_read_json(
        REPORT_DIR / "gitleaks.json"
    )

    trivy = safe_read_json(
        REPORT_DIR / "trivy.json"
    )

    checkov = safe_read_json(
        REPORT_DIR / "checkov.json"
    )

    pip_audit = safe_read_json(
        REPORT_DIR / "pip_audit.json"
    )

    report = {

        "semgrep": count_semgrep(semgrep),

        "gitleaks": count_gitleaks(gitleaks),

        "trivy": count_trivy(trivy),

        "checkov": count_checkov(checkov),

        "pip_audit": count_pip_audit(pip_audit)
    }

    output = REPORT_DIR / "security_report.json"

    with open(output, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\n" + "=" * 70)
    print("COMBINED SECURITY REPORT")
    print("=" * 70)

    print(json.dumps(report, indent=4))

    return output


def main():

    print("\n")
    print("=" * 70)
    print("              DEVSECOPS SECURITY MODULE")
    print("=" * 70)

    run_semgrep()
    run_gitleaks()
    run_trivy()
    run_checkov()
    run_pip_audit()

    report = create_combined_report()

    print("\nSecurity scanning completed.")
    print(f"Combined report: {report}")


if __name__ == "__main__":
    main()