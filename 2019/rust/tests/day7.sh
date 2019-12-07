#!/bin/bash

set -xe -o pipefail

./target/debug/aoc 7 assets/day7-example-0 | grep -q "43210"
./target/debug/aoc 7 assets/day7-example-1 | grep -q "54321"
./target/debug/aoc 7 assets/day7-example-2 | grep -q "65210"
./target/debug/aoc 7 assets/day7-input | grep -q "368584"

./target/debug/aoc 7 assets/day7-example-3 | grep -q "139629729"
./target/debug/aoc 7 assets/day7-example-4 | grep -q "18216"
