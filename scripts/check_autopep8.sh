#!/usr/bin/env sh

poetry run autopep8 --recursive --diff server/ tests/
