#!/bin/bash

set -eu -o pipefail

curl --cookie "${AOC_COOKIE_GITHUB}" https://adventofcode.com/2020/day/$1/input > assets/day$1-input-1
