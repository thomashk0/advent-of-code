import networkx as nx


def load_input(f, directed=True):
    g = nx.DiGraph() if directed else nx.Graph()
    for l in f:
        src, dst = tuple(l.strip().split(')'))
        g.add_edge(dst, src)
    return g


def part_1(fname):
    with open(fname) as f:
        g = load_input(f)
        return sum(len(nx.descendants(g, n)) for n in g.nodes)


def part_2(fname):
    with open(fname) as f:
        g = load_input(f, directed=False)
        return nx.shortest_path_length(g, 'YOU', 'SAN') - 2


def main():
    assert part_1('assets/day6-example-0') == 42
    assert part_2('assets/day6-example-1') == 4
    print("part 1:", part_1('assets/day6-input'))
    print("part 2:", part_2('assets/day6-input'))


if __name__ == '__main__':
    main()
