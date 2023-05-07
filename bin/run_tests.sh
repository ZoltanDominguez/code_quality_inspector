#!/usr/bin/env bash
coverage erase
pytest ./tests/ \
       -vv --random-order \
       --junitxml="./reports/xml/test_results.xml" \
       --html "./reports/html/test_results.html" \
       --cov-report xml:./reports/xml/test_coverage.xml \
       --cov-report html:./reports/html/test_coverage \
       --cov=code_quality_inspector --cov-branch

TESTS_EXIT_CODE=$?
echo "Exit code for tests: " $TESTS_EXIT_CODE

if [[ "$TESTS_EXIT_CODE" == 0 ]] 
then
  coverage report --fail-under=85
  COVERAGE_EXIT_CODE=$?
  echo "Coverage exit code for tests: " $COVERAGE_EXIT_CODE
fi

if  [ $COVERAGE_EXIT_CODE -ne 0 ] || \
    [ $TESTS_EXIT_CODE -ne 0 ]; then
    exit 1
fi
