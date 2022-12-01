#!/bin/bash


set -eu -o pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: ./$0 <DAY_NUMBER>"
    exit 1
fi

if [[ -z "${AOC_COOKIE_GITHUB+x}" ]]; then
    echo "you must define AOC_COOKIE_GITHUB before calling this script"
    echo "  To obtain it: Firefox -> Inspect -> Storage, then copy the session cookie value."
    exit 1
fi

cookie="session=${AOC_COOKIE_GITHUB}"
curl --cookie "$cookie" https://adventofcode.com/2022/day/$1/input > assets/day$1-input-1
