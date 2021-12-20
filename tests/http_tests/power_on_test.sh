#!/usr/bin/env sh

curl localhost:5000/power/on
printf "\n"
curl localhost:5000/power/off
