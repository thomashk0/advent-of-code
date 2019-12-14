import copy

import networkx as nx


def load_input(f):
    def elt_spec(l):
        p = l.strip().split()
        return int(p[0]), p[1].strip()

    g = nx.DiGraph()
    for line in f:
        l, r = tuple(line.strip().split("=>"))
        produced, dst = elt_spec(r)
        g.add_node(dst, batch_size=produced)
        for cost, element in map(elt_spec, l.split(",")):
            g.add_edge(element, dst, cost=cost)
    g.nodes['ORE']['batch_size'] = 1
    return g


def run_part_1(f_name):
    with open(f_name) as f:
        g = load_input(f)
        return min_number_of(g, 'ORE', 1)


def run_part_2(f_name):
    with open(f_name) as f:
        g = load_input(f)
        return search_fuel(g, 1000000000000)


def divup(x, q):
    return (x + (q - 1)) // q


def min_number_of(g, elt, n_fuel):
    """Compute the minimum number of element of type elt required to create
    n_fuel FUEL elements.
    """
    if elt == 'FUEL':
        return n_fuel
    t = sum([g.edges[elt, s]['cost'] * min_number_of(g, s, n_fuel) for s in
             g.successors(elt)])
    return divup(t, g.nodes[elt]['batch_size'])


def search_fuel(g, ore):
    """
    Binary seach of the fuel amount that can be created with 'ore' ORE elements.

    Binary search applies there, because the function
        f : n_ore -> n_fuel
    is monotonic.
    """
    s_min, s_max = 0, ore
    while True:
        if s_min == s_max:
            return s_min
        middle = s_min + (s_max - s_min) // 2
        ore_needed = min_number_of(g, 'ORE', middle)
        if ore_needed > ore:
            s_max = middle
        else:
            if middle == s_min:
                return middle
            s_min = middle


def main():
    assert run_part_1('assets/day14-example-0') == 165
    assert run_part_1('assets/day14-example-1') == 13312
    assert run_part_1('assets/day14-example-2') == 180697
    assert run_part_1('assets/day14-example-3') == 2210736
    print("part 1:", run_part_1("assets/day14-input"))

    print("part 2:", run_part_2('assets/day14-input'))
    assert run_part_2('assets/day14-example-2') == 5586022
    assert run_part_2('assets/day14-example-3') == 460664
    assert run_part_2('assets/day14-example-1') == 82892753


if __name__ == '__main__':
    main()
