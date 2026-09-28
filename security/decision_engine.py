import json
import sys


def make_decision(report):
    critical = report.get("critical", 0)
    high = report.get("high", 0)

    if critical > 0 or high > 0:
        return "BLOCK"

    return "ALLOW"


def main():

    report_file = sys.argv[1]

    with open(report_file, "r") as file:
        report = json.load(file)

    decision = make_decision(report)

    print("Security Decision:", decision)

    if decision == "BLOCK":
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
    