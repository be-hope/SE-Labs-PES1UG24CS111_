# Lab 5 - Reflection

The provided Lab 5 PDF requests reflection but contains no numbered reflection
questions. The README refers to four questions that are also absent. These four
responses address the stated learning outcomes, rather than quoting missing
questions.

## 1. What did the tools reveal?

Bandit found five security problems, including shell execution, eval, and MD5.
Pylint identified the shared mutable default, broad exception handling, missing
documentation, and resource-management issues. Flake8 found unused names, long
lines, the None comparison, and the missing final newline. Their overlapping
checks provided useful feedback from different perspectives.

## 2. How were fixes prioritized?

The two High Bandit findings and the Medium eval finding came first. Removing the
unnecessary shell preserved export without injection risk. Numeric discount
arithmetic replaced executable text. SHA-256 replaced MD5, and secrets replaced
random. Remaining fixes addressed exception handling, shared defaults, resources,
and style without suppressing any tool rules.

## 3. How were improvements and behavior verified?

Original and final script output were recorded. Pylint improved from 4.81 to
10.00; Bandit findings dropped from five to zero and Flake8 violations from nine
to zero. Six regression tests cover order creation and invalid/duplicate orders,
caller-owned logs, status and void operations, discount boundaries and rejection
of unsafe input, hash/PIN properties, and shell characters treated literally in
export filenames. Sample discount remains 40.5 and pending-table count remains
three. PIN values vary by design.

## 4. What are the benefits and limits of static analysis?

Automated analysis gives repeatable feedback before runtime, but cannot prove
business behavior or security. Manual review removed the printed hardcoded token
and import-time side effects, which the recorded security scan did not flag.
Tests remain necessary. Production work would also require persistence, a money
precision policy, authentication controls, and actual printer integration; clean
static reports do not establish those properties.
