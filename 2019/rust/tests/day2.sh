#!/bin/bash

set -xe -o pipefail

./target/debug/aoc 2 | grep -q "5434663"
./target/debug/aoc 2 | grep -q "4559"
