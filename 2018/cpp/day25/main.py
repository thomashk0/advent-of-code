import sys
import networkx as nx

def manhattan_distance(p, q):
    return sum([abs(pc - qc) for pc, qc in zip(p, q)])

def draw(g):
    import matplotlib.pyplot as plt
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()

def main():
    coords = []
    if len(sys.argv) != 2:
        print("USAGE: ./day25.py INPUT")
        sys.exit(1)

    for l in open(sys.argv[1]):
        coords.append(tuple(map(int, l.split(','))))
    print(coords)
    g = nx.Graph()
    for i in range(len(coords)):
        g.add_node(i, label="{:d},{:d},{:d},{:d}".format(*coords[i]))
        p = coords[i]
        for j in range(i, len(coords)):
            q = coords[j]
            if manhattan_distance(p, q) <= 3:
                g.add_edge(i, j)
    print([c for c in sorted(nx.connected_components(g), key=len, reverse=True)])
    print("Part 1: {}".format(len(list(nx.connected_components(g)))))
    draw(g)

if __name__ == '__main__':
    main()