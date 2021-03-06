import enum
import ctypes
from ctypes import POINTER
import pkg_resources

lib_intcpu_debug = pkg_resources.resource_filename('intcpu',
                                                   'libaoc_bindings_debug.so')
lib_intcpu = pkg_resources.resource_filename('intcpu', 'libaoc_bindings.so')

ICPU_LIB_DEBUG = ctypes.cdll.LoadLibrary(lib_intcpu_debug)
ICPU_LIB = ctypes.cdll.LoadLibrary(lib_intcpu)


class IntCpuS(ctypes.Structure):
    pass


for lib in [ICPU_LIB, ICPU_LIB_DEBUG]:
    lib.icpu_create.restype = POINTER(IntCpuS)
    lib.icpu_clone.restype = POINTER(IntCpuS)


def to_i64_array(lst):
    t = ctypes.c_int64 * len(lst)
    return t(*lst)


def parse_tape(s):
    return list(map(int, s.split(',')))


class Status(enum.IntEnum):
    RUNNING = 0
    HALTED = 1
    INVALID_PC = 2
    MEMORY_ERROR = 3
    DECODE_ERROR = 4
    NO_MORE_INPUT = 5


class IntCpu:
    def __init__(self, lib=ICPU_LIB, other=None):
        self.lib = lib
        self.tape = []
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
        self.tape = p
        self.lib.icpu_load_tape(self._handle, p, ctypes.c_size_t(len(p)))

    def resume(self):
        self.lib.icpu_resume(self._handle)

    def step(self):
        return Status(self.lib.icpu_step(self._handle))

    def run(self):
        return Status(self.lib.icpu_run(self._handle))

    def add_input(self, input):
        self.lib.icpu_add_input(self._handle, ctypes.c_int64(input))

    def invert_branch(self, addr):
        self.lib.icpu_invert_branch(self._handle, ctypes.c_int64(addr))

    def pending_output(self):
        return self.lib.icpu_pending_output(self._handle)

    def pending_input(self):
        return self.lib.icpu_pending_input(self._handle)

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
    src = parse_tape(open('../assets/day21-input').readline().strip())
    disassemble(src)
    # c = IntCpu()
    # src = parse_tape(open('../assets/day2-input').readline().strip())
    # c.load(src)
    # c.write(1, 12)
    # c.write(2, 2)
    # c.run()
    # print(c.read(0))


if __name__ == "__main__":
    main()
