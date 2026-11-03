$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
python -m coverage run --data-file=.coverage.code --source=pet_boarding -m pytest test_code_coverage.py -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m coverage report --data-file=.coverage.code -m --fail-under=90
