#!/bin/bash

set -xe -o pipefail

# ./target/debug/aoc 9 assets/day9-example-0 | grep -q "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
./target/debug/aoc 9 assets/day9-example-1 | grep -q "1219070632396864"
./target/debug/aoc 9 assets/day9-example-2 | grep -q "1125899906842624"
./target/debug/aoc 9 assets/day9-input | grep -q "73439"
./target/debug/aoc 9 assets/day9-input | grep -q "3742852857"
