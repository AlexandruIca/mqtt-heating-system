#!/usr/bin/env sh

poetry run autopep8 --recursive server/ tests/ --in-place
