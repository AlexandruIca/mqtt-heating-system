#!/usr/bin/env sh

for test in $(ls -a | grep -i ".*\.py")
do
    poetry run python3 $test

    if [ $? -ne 0 ]; then
        echo "$test failed!"
    fi
done
