#!/bin/bash

set -xe -o pipefail

./target/debug/aoc 5 | grep -q "7988899"
./target/debug/aoc 5 | grep -q "13758663"
