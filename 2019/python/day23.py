from collections import defaultdict

import intcpu


class ExecError(Exception):
    pass


class Node:
    def __init__(self, src=None, cpu=None):
        self.cpu = cpu or intcpu.IntCpu()
        if src:
            self.cpu.load_file(src)
        self.waiting = 0

    def add_input(self, x, y):
        self.cpu.add_input(x)
        self.cpu.add_input(y)
        self.waiting = 0

    def run(self, max_steps=1):
        for i in range(max_steps):
            ret = self.cpu.run()
            if ret == 1:
                break
            elif ret == 5:
                self.cpu.add_input(-1)
                self.waiting += 1
                self.cpu.resume()
            elif ret != 0:
                self.cpu.dump()
                raise ExecError(f"Cpu leaved with code {ret}")
            if self.cpu.pending_output() >= 3:
                break

    def output_packets(self):
        while self.cpu.pending_output() >= 3:
            self.waiting = 0
            dst = self.cpu.pop_output()
            x, y = self.cpu.pop_output(), self.cpu.pop_output()
            yield dst, x, y


class Network:
    def __init__(self, src):
        self.nodes = [Node(src) for _ in range(50)]
        for i, n in enumerate(self.nodes):
            n.cpu.add_input(i)
        self.nat = []
        self.nat_old = None
        self.unrouted = defaultdict(list)

    def waiting_since(self):
        return min(n.waiting for n in self.nodes)

    def tick(self):
        packets = []
        for n in self.nodes:
            n.run()
            packets.extend(n.output_packets())
        for dst, x, y in packets:
            if dst == 255:
                self.nat = [(x, y)]
            if dst >= len(self.nodes):
                self.unrouted[dst].append((x, y))
            else:
                self.nodes[dst].add_input(x, y)

        if self.waiting_since() >= 1000:
            # print(f"Resending {self.nat[0]}")
            if self.nat_old == self.nat:
                return self.nat[0]
            self.nat_old = [self.nat[0]]
            self.nodes[0].add_input(*self.nat[0])


def part_1():
    network = Network("assets/day23-input")
    for i in range(1000):
        network.tick()
        if network.nat:
            return network.nat[0][1]


def part_2():
    network = Network("assets/day23-input")
    for i in range(100000):
        r = network.tick()
        if r:
            return r[1]


def main():
    print("part 1:", part_1())
    print("part 2:", part_2())
    pass


if __name__ == "__main__":
    main()
