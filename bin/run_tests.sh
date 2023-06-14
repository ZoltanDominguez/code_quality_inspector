#!/usr/bin/env bash

MIN_TEST_COVERAGE=40

print_line()
{
    printf -- '-%.0s' {1..100}; echo ""
}

coverage erase
pytest ./tests/ \
       -vv --random-order \
       --junitxml="./reports/xml/test_results.xml" \
       --html "./reports/html/test_results.html" \
       --cov-report xml:./reports/xml/test_coverage.xml \
       --cov-report html:./reports/html/test_coverage \
       --cov=cqi --cov-branch

TESTS_EXIT_CODE=$?
echo "Exit code for tests: " $TESTS_EXIT_CODE

if [[ "$TESTS_EXIT_CODE" == 0 ]] 
then
  coverage report --fail-under=$MIN_TEST_COVERAGE;            COVERAGE_EXIT_CODE=$?
  echo "Coverage exit code: " $COVERAGE_EXIT_CODE
fi

print_line
echo "Running pylint:"
pylint cqi/;                                                  PYLINT_EXIT_CODE=$?

echo "Running ruff:"
ruff check cqi/;                                              RUFF_EXIT_CODE=$?
if [ $RUFF_EXIT_CODE -eq 0 ]; then echo "Ruff passed!"; fi

print_line && echo "Running black:"
black . --check;                                              BLACK_EXIT_CODE=$?

print_line && echo "Running semgrep:"
semgrep scan --config auto;                                   SEMGREP_EXIT_CODE=$?

print_line && echo "Running mypy:"
mypy cqi/;                                                    MYPY_EXIT_CODE=$?

print_line && echo "Summary:"
echo "Tests exit code: "    $TESTS_EXIT_CODE
echo "Coverage exit code: " $COVERAGE_EXIT_CODE
echo "Pylint exit code: "   $PYLINT_EXIT_CODE
echo "Ruff exit code: "     $RUFF_EXIT_CODE
echo "Black exit code: "    $BLACK_EXIT_CODE
echo "Semgrep exit code: "  $SEMGREP_EXIT_CODE
echo "Mypy exit code: "     $MYPY_EXIT_CODE


if  [ $TESTS_EXIT_CODE -ne 0 ] || \
    [ $COVERAGE_EXIT_CODE -ne 0 ] || \
    [ $PYLINT_EXIT_CODE -ne 0 ] || \
    [ $RUFF_EXIT_CODE -ne 0 ] || \
    [ $BLACK_EXIT_CODE -ne 0 ]; then
    exit 1
fi
