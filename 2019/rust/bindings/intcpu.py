import ctypes
from ctypes import POINTER

ICPU_LIB = ctypes.cdll.LoadLibrary('./target/debug/libaoc_bindings.so')

class IntCpuS(ctypes.Structure):
    pass

ICPU_LIB.icpu_create.restype = POINTER(IntCpuS)
# ICPU_LIB.icpu_load_tape.argtypes = POINTER(IntCpuS)


def to_i64_array(lst):
    t = ctypes.c_int64 * len(lst)
    return t(*lst)


def parse_tape(s):
    return list(map(int, s.split(',')))


class IntCpu:
    def __init__(self, lib=ICPU_LIB):
        self.lib = lib
        self._handle = self.lib.icpu_create()

    def load(self, tape):
        p = to_i64_array(tape)
        self.lib.icpu_load_tape(self._handle, p, ctypes.c_size_t(len(p)))

    def step(self):
        return self.lib.icpu_step(self._handle)

    def dump(self):
        self.lib.icpu_dump(self._handle)

    def __del__(self):
        self.lib.icpu_destroy(self._handle)


def main():
    c = IntCpu()
    src = parse_tape(open('../assets/day2-input').readline().strip())
    c.load(src)
    while True:
        if c.step() != 0:
            print("Simulation stopped")
            break
    c.dump()


if __name__ == "__main__":
    main()
