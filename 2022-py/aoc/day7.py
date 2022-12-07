import networkx as nx


def parse_input(raw: str):
    lines = raw.splitlines()
    i = 0
    cmds = []

    while i < len(lines):
        current = lines[i]
        if current.startswith("$"):
            current_cmd = current[1:].split()
            i += 1
            output = []
            while i < len(lines) and not lines[i].startswith("$"):
                output.append(lines[i])
                i += 1
            cmds.append((current_cmd, output))
        else:
            raise NotImplementedError("expecting an command")

    g = nx.DiGraph()
    path = ["/"]
    for cmd, output in cmds:
        if cmd[0] == "cd":
            if cmd[1] == "/":
                path = ["/"]
            elif cmd[1] == "..":
                path = path[:-1]
            else:
                g.add_edge("/".join(path), "/".join(path + [cmd[1]]))
                path.append(cmd[1])
        elif cmd[0] == "ls":
            for r in output:
                t, v = r.split()
                if t == "dir":
                    g.add_edge("/".join(path), "/".join(path + [v]))
                else:
                    g.nodes["/".join(path)][v] = int(t)
    return g


def directory_size(i, sizes, g: nx.DiGraph):
    local_size = sum(g.nodes[i].values())
    for j in g.successors(i):
        if child_size := sizes.get(j):
            local_size += child_size
        else:
            child_size = directory_size(j, sizes, g)
            sizes[j] = child_size
            local_size += child_size
    return local_size


def part_1(input: nx.DiGraph):
    sizes = {}
    total = 0
    assert nx.is_tree(input)
    for i, n in input.nodes.data():
        dir_size = directory_size(i, sizes, input)
        if dir_size < 100000:
            total += dir_size
    return total


def part_2(input):
    threshold = 30000000
    sizes = {}
    mem_used = directory_size("/", sizes, input)
    mem_free = 70000000 - mem_used
    s = [directory_size(i, sizes, input) for i in input.nodes]
    return min(x for x in s if mem_free + x > threshold)


def aoc_inputs():
    return {
        "example-0": ("day7-input-ex", 95437, 24933642),
        "real": ("day7-input-1", 1543140, 1117448),  # Not 1074226
    }
