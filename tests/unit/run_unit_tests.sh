#!/usr/bin/env sh

for unit_test in $(ls -a | grep -i ".*\.py"); do
    poetry run python3 $unit_test

    if [ $? -ne 0 ]; then
        echo "$unit_test failed!"
    fi
done
