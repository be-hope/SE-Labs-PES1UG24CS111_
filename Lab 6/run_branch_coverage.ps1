$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m coverage run --branch --data-file=.coverage.branch --source=pet_boarding -m pytest test_branch_coverage.py -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m coverage report --data-file=.coverage.branch -m --fail-under=90
python -m coverage json --data-file=.coverage.branch -o branch_coverage.json
python -c "import json; t=json.load(open('branch_coverage.json'))['totals']; p=100*t['covered_branches']/t['num_branches']; print('Branch coverage: %.2f%% (%d/%d branches)' % (p,t['covered_branches'],t['num_branches'])); raise SystemExit(0 if p >= 90 else 1)"
