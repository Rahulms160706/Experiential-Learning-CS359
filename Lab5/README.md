# Lab 5: Static Code Analysis

## Overview
This project uses Pylint, Bandit, and Flake8 to check a Python flight reservation demo for code-quality, security, and style issues.

## Files
- `flight_reservation_system.py` — updated program.
- `issues.md` — issues identified and their fixes.
- `reflection.md` — reflection answers based on the supplied handout's learning outcomes.
- `pylint_report_before.txt`, `bandit_report_before.txt`, `flake8_report_before.txt` — original reports, if included in this bundle.

## Requirements
Use Python 3 and install the tools in your virtual environment:

```bash
python -m pip install pylint bandit flake8
```

## Run the program

```bash
python flight_reservation_system.py
```

The program writes `flight_manifest.txt` in the current directory.

## Generate after-reports

```bash
pylint flight_reservation_system.py > pylint_report_after.txt 2>&1
bandit -r flight_reservation_system.py > bandit_report_after.txt 2>&1
flake8 flight_reservation_system.py > flake8_report_after.txt 2>&1
```

Compare the after-reports with the original reports. The lab requires a Pylint score above 9.5 and expects findings to be addressed. Verify actual results instead of assuming the tools report no issues.

## Secret environment variable
The program optionally checks whether `AIRLINE_API_SECRET` is set. It does not display the secret value. In PowerShell, a test value can be set with:

```powershell
$env:AIRLINE_API_SECRET="your-test-token"
python flight_reservation_system.py
```

## Submission checklist
- [ ] Updated Python program
- [ ] `issues.md`
- [ ] `reflection.md`
- [ ] Before and after reports for all three tools
- [ ] Three commits as required by the handout
