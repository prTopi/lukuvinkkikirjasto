#!/usr/bin/env bash
set -e

# Run an individual test suite if the TEST_SUITE environmental variable is set.
if [ -z "$TEST_SUITE" ]; then
    TEST_SUITE=""
fi

# Give the app time to start
sleep 5

CMD="robot --console verbose --outputdir /documentation/test_reports/robot /src/tests/$TEST_SUITE"

echo ${CMD}

``${CMD}``
