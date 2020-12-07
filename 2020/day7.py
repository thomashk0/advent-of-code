import itertools
import re
import networkx as nx

BAG_SPEC_RE = re.compile(r"^(\w+) (\w+) (bag|bags) contain\s+")
BAG_CONTENT_RE = re.compile(r"(\d+) (\w+) (\w+)")


def load_input(lines):
    g = nx.DiGraph()
    for line in lines:
        start = BAG_SPEC_RE.match(line)
        rest = line[len(start.group(0)):].split(',')
        # print(BAG_SPEC_RE.match(line).groups())
        node_name = f'{start.group(1)} {start.group(2)}'
        g.add_node(node_name)
        for r in rest:
            r = r.strip()
            if r.startswith("no other"):
                break
            match = BAG_CONTENT_RE.match(r)
            n = int(match.group(1))
            target_name = f'{match.group(2)} {match.group(3)}'
            g.add_edge(node_name, target_name, weight=n)
            # print(match.groups())
    return g


def number_of_subbags(g: nx.DiGraph, n):
    total = 1
    # print(g.succ[n].data('weight'))
    for succ in g.successors(n):
        weight = g.edges[n, succ]['weight']
        total += weight * number_of_subbags(g, succ)
    return total


def main():
    g = load_input(open('assets/day7-input'))
    print("part 1:", len(nx.ancestors(g, 'shiny gold')))
    print("part 2:", number_of_subbags(g, 'shiny gold') - 1)


if __name__ == '__main__':
    main()
