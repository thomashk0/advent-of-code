# Solutions for the Advent of Code 2019

## Organisation

* Most solutions are written in Python (see [python](./python/) directory)
* Some solutions are written in Rust (see [rust](./rust/) directory)
* The IntCode emulator is written in Rust:

    * [intcode.rs](./rust/src/intcode.rs)
    * Some low level FFI bindings for the emulator are exposed in the [bindings](./rust/bindings) directory
    * Python bindings are available in [bindings](./rust/bindings)

## Usage

To create the Python virtualenv:

```
$ python -mvenv venv
$ source venv/bin/activate
$ pip install wheel networkx numpy
$ make -C ./rust/bindings wheel
$ pip install ./rust/bindings/dist/aoc_intcpu-1.0.2-py3-none-any.whl
```
