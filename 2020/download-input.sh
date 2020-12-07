#!/bin/bash

set -eu -o pipefail

curl --cookie "${AOC_COOKIE}" https://adventofcode.com/2020/day/$1/input > assets/day$1-input
