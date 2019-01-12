import collections
import sys
import networkx as nx

def part_1(g):
    pending = set(n for n in g.nodes if len(list(g.predecessors(n))) == 0)
    explored = set()
    chain = ""
    while pending:
        top = None
        for s in sorted(pending):
            if all(n in explored for n in g.predecessors(s)):
                top = s
                break
        assert top
        pending.remove(top)
        chain += top
        explored.add(top)
        pending.update(n for n in g.successors(top) if n not in explored)
    print("Part 1:", chain)

def part_2(g, workers=5):
    pending = set(n for n in g.nodes if len(list(g.predecessors(n))) == 0)
    busy = {}
    finished = set()
    time = 0

    while True:
        if len(busy) == workers:
            _, time = min(busy.items(), key=lambda x:x[1])

        finished.update(el for el, t in busy.items() if t == time)
        busy = {el: t for el, t in busy.items() if t > time}
        if not busy and not pending:
            break

        top = None
        for s in sorted(pending):
            if all(n in finished for n in g.predecessors(s)):
                top = s
                break
        if top is None:
            _, time = min(busy.items(), key=lambda x:x[1])
            continue
        assert top
        pending.remove(top)
        diff = (ord(top) - ord('A') + 1)
        busy[top] = time + 60 + diff
        pending.update(n for n in g.successors(top) if n not in finished and n not in busy)

    print("Part 2:", time)


def main():
    g = nx.DiGraph()
    for l in sys.stdin:
        parts = l.split()
        g.add_edge(parts[1], parts[7])

    part_1(g)
    part_2(g)


if __name__ == '__main__':
    main()
