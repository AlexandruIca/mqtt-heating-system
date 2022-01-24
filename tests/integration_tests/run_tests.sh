#!/usr/bin/env sh

TESTS="temperature_tests.py water_temperature_tests.py"

for test in $TESTS
do
    poetry run python3 $test

    if [ $? -ne 0 ]; then
        echo "$test failed!"
    fi
done
