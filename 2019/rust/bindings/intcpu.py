import ctypes
from ctypes import POINTER

ICPU_LIB = ctypes.cdll.LoadLibrary('./target/debug/libaoc_bindings.so')


class IntCpuS(ctypes.Structure):
    pass


ICPU_LIB.icpu_create.restype = POINTER(IntCpuS)
ICPU_LIB.icpu_clone.restype = POINTER(IntCpuS)


def to_i64_array(lst):
    t = ctypes.c_int64 * len(lst)
    return t(*lst)


def parse_tape(s):
    return list(map(int, s.split(',')))


class IntCpu:
    def __init__(self, lib=ICPU_LIB, other=None):
        self.lib = lib
        if other:
            self._handle = self.lib.icpu_clone(other._handle)
        else:
            self._handle = self.lib.icpu_create()

    def clone(self):
        return IntCpu(lib=self.lib, other=self)

    def load_file(self, f_name):
        with open(f_name) as f:
            self.load(parse_tape(f.readline().strip()))

    def load(self, tape):
        p = to_i64_array(tape)
        self.lib.icpu_load_tape(self._handle, p, ctypes.c_size_t(len(p)))

    def resume(self):
        self.lib.icpu_resume(self._handle)

    def step(self):
        return self.lib.icpu_step(self._handle)

    def run(self):
        return self.lib.icpu_run(self._handle)

    def add_input(self, input):
        self.lib.icpu_add_input(self._handle, ctypes.c_int64(input))

    def pending_output(self):
        return self.lib.icpu_pending_output(self._handle)

    def pop_output(self):
        dst = (ctypes.c_int64 * 1)(0)
        ret = self.lib.icpu_pop_output(self._handle, dst)
        if not ret:
            return None
        return int(dst[0])

    def write(self, addr, value):
        ret = self.lib.icpu_mem_write(self._handle, ctypes.c_int64(addr),
                                      ctypes.c_int64(value))
        assert ret == 0

    def read(self, addr):
        dst = (ctypes.c_int64 * 1)(addr)
        ret = self.lib.icpu_mem_read(self._handle, ctypes.c_int64(addr), dst)
        assert ret == 0
        return dst[0]

    def dump(self):
        self.lib.icpu_dump(self._handle)

    def __del__(self):
        self.lib.icpu_destroy(self._handle)


def main():
    c = IntCpu()
    src = parse_tape(open('../assets/day2-input').readline().strip())
    c.load(src)
    c.write(1, 12)
    c.write(2, 2)
    c.run()
    # while True:
    #     if c.step() != 0:
    #         print("Simulation stopped")
    # break
    print(c.read(0))
    # c.dump()


if __name__ == "__main__":
    main()
