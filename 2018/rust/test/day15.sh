#!/bin/bash

set -e

function day15_test() {
    echo "===> testing with $1..."
    if ! cargo run --release -- 15 < "assets/$1" | grep -q "$2"; then
       echo -e "\e[91m-> FAILED!!!\e[39m"
    else
        echo "-> PASSED"
    fi
}

day15_test "day15_example_0.txt" 27730
day15_test "day15_example_1.txt" 36334
day15_test "day15_example_2.txt" 39514
day15_test "day15_example_3.txt" 27755
day15_test "day15_example_4.txt" 28944
day15_test "day15_example_5.txt" 18740
day15_test "day15.txt" 193476
