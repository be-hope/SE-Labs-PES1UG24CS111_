# Lab 5 - Issues and fixes

Original line numbers refer to restaurant_order_system.py at commit a018232.
Bandit severities below are those actually reported by the tool.

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---|---|---|
| B605 | High security | 58 | Filename concatenated into shell command permits command injection. | Remove shell call; export file and print a plain message. |
| B324 | High security | 47 | Weak MD5 hash. | Use SHA-256; document digest as identifier, not authentication. |
| B307 / W0123 | Medium security | 42 | eval executes arbitrary Python expressions. | Replace expression with numeric discount constrained to [0, 1]. |
| B311 | Low security | 51 | Standard random unsuitable for a POS PIN. | Use secrets.randbelow with same four-digit range. |
| B110 / W0702 / E722 | Low security / correctness | 24-27 | Bare except silently hides unexpected failures. | Use orders.pop(table_id, None) for intended missing-table no-op. |
| W0102 | Correctness | 15 | Mutable default list persists across calls. | Default to None and initialize fresh list; retain caller-supplied logs. |
| W1514 / R1732 | Reliability | 55-57 | Open file lacks guaranteed close and explicit encoding. | Use context manager and UTF-8. |
| C0103 / C0116 | Maintainability | 15-61 | CamelCase names and missing documentation. | Use snake_case and function docstrings. |
| W0611 / F401 | Quality | 6 | Unused math import. | Remove import. |
| W0612 / F841 | Quality | 31, 41 | Unused tax variable; eval hides base_bill usage from tools. | Remove tax variable and reference base_bill directly in arithmetic. |
| C0121 / E711 / R1703 / R1705 | Quality | 32-37 | None equality and redundant boolean branches. | Identity check and direct boolean return. |
| W0621 / W0612 | Quality | 61-65 | Shadowed orders parameter and unused loop key. | Rename parameter and iterate over mapping values. |
| C0301 / E501 / C0209 / W292 | Style | 18, 19, 75, 83 | Long lines, old string interpolation, absent final newline. | Wrap dictionary, use f-string, shorten call and add newline. |
| Manual review | Secret handling | 69, 80 | Hardcoded token printed; not flagged by this Bandit run. | Remove unused token and output. |
| Manual review | Import behavior | 83 | Import runs demo and writes a file. | Add __main__ guard. |

## Measured results

| Check | Before | After |
|---|---|---|
| Pylint | 4.81/10, 28 messages | 10.00/10, no messages |
| Bandit | 5 findings: 2 High, 1 Medium, 2 Low | 0 findings |
| Flake8 | 9 violations | 0 violations |
| Regression tests | None provided | 6 passed |

Full raw reports are in reports/before and reports/after. No analyzer rules were
disabled. The analysis target is restaurant_order_system.py.

## Interface changes and limits

Functions now use snake_case. calculate_discounted_bill("T1", 0.10) replaces an
executable expression argument and retains the 40.50 sample result. Invalid
fractions (including NaN/infinity) raise ValueError; expression strings raise
TypeError; unknown tables raise KeyError. Hashes are now 64 hex characters.
Export still writes the mapping as text; the message accurately describes a file
export, without claiming physical printing. PIN range stays 1000-9999; randomness
alone is not a complete authentication system. Global in-memory data and float
billing remain demo limitations; persistence and payment integration are outside
this static-analysis lab.
