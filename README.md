# Solutions for the Advent of Code programming puzzles

This repository contains my solutions to the [Advent of Code 2018](https://adventofcode.com/).
Solutions are provided "as this", not all of them are cleaned-up neither optimized.

# Organisation

Solutions are written in various languages including C++17, Haskell, Python and even Rust!

* Day 1-8 are written in Python (see [day1-8](./day1-8/) directory).
* Day 1-12 are written in Rust (see [rust](./rust) directory).
* Day 23 part 2 is written using Haskell + SBV.
* The remaining solutions are written in C++ (one directory per-day).

# Running

For C++ solutions:

```console
$ mkdir build && cd build
$ cmake ..
$ make
```

For Rust solutions:

```
$ cd rust
$ cargo build
$ cargo run [DAY] < assets/input_DAY.txt
```

For Python solutions:

```
$ cd day1-8
$ python day_[DAY] < ../assets/input_DAY.txt
```
