# Lab 5: Static Code Analysis - Restaurant Order System

Completed locally. Lab 2/Jira is excluded as requested.

## Deliverables

- restaurant_order_system.py: cleaned application.
- issues.md: issue table with original lines, priorities, fixes, results, and interface changes.
- reflection.md: four reflection responses and missing-question explanation.
- reports/before and reports/after: all three raw tool reports and demo output.
- reports/after/tests.txt: six passing regression tests.
- test_restaurant_order_system.py: behavioral regression tests.
- requirements-dev.txt: pinned analysis dependencies.

## Reproduce (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe restaurant_order_system.py
.\.venv\Scripts\python.exe -m pylint --persistent=n restaurant_order_system.py
.\.venv\Scripts\python.exe -m bandit -r restaurant_order_system.py
.\.venv\Scripts\python.exe -m flake8 restaurant_order_system.py
.\.venv\Scripts\python.exe -m unittest -v
```

Save stdout for Pylint/Flake8 reports. Use Bandit's -o option to save its report.
The original baseline comes from commit a018232, before edits. The demo takes no
interactive input despite the original README's claim.

## Verified results

Python 3.12.14; Pylint 4.1.3: 10.00/10; Bandit 1.9.4: zero findings;
Flake8 7.4.1: zero violations. Six tests passed. The final Flake8 report is
intentionally empty. No checks were suppressed.

## Submission history

Three commits on codex/complete-labs group Bandit security fixes, Pylint quality
fixes, and Flake8 formatting with evidence. Reports preserve the original results.
All work and commits are local; remote submission is not claimed.

Discounts now accept a numeric fraction (0.10 for ten percent) rather than Python
expressions. Function names use snake_case. See issues.md for other changes.
