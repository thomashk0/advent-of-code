import copy
import re
import networkx as nx
import numpy as np

LINE_RE = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

NODES = {"ore": 0, "clay": 1, "obs": 2, "geode": 3}


def parse_input(raw: str):
    costs = []
    for line in raw.splitlines():
        cost_matrix = np.zeros((4, 4), dtype=np.int64)
        m = LINE_RE.match(line)
        _i, ore_cost, clay_cost, obs_cost_ore, obs_cost_clay, geode_cost_ore, geode_cost_obs = m.groups()
        cost_matrix[0, 0] = ore_cost
        cost_matrix[1, 0] = clay_cost
        cost_matrix[2, 0] = obs_cost_ore
        cost_matrix[2, 1] = obs_cost_clay
        cost_matrix[3, 0] = geode_cost_ore
        cost_matrix[3, 2] = geode_cost_obs
        costs.append(cost_matrix)
    return costs


def memo_produced(cache, costs, robots, minerals, budget):
    key = (robots, minerals, budget)
    v = cache.get(key)
    if v is not None:
        return v
    r = max_produced(cache, costs, robots, minerals, budget)
    cache[key] = r
    return r


# def set_field(field, value):
#     mask = 0xFFFF_FFFF
#     return (value ^ (mask << (32 * field))) | value << (32 * field)
#
#
# def get_field(field, value):
#     return value >> (32 * field) & 0xFFFF_FFFF

def optimal_prod(unit_cost, robots, init, duration):
    choices = [
        init + duration * robots  # Production if no robots are created.
    ]
    for bots_created in range(1, duration):
        choice = init - unit_cost * bots_created
        for i in range(1, bots_created):
            choice += robots + i - 1
        choice += (robots + bots_created) * (duration - bots_created)
        choices.append(choice)
    return choices


def max_produced(cache, costs, robots, minerals, clock):
    if clock > 3:
        # Return the number of geodes available
        return minerals[3]
    # TODO: pruning??

    print()
    print(f"scanning config (clock={clock}): robots={robots}, minerals={minerals}")
    choices = []
    r_avail = [r + x for r, x in zip(robots, minerals)]
    print(f"    - new minerals: {r_avail}")
    # First option: just wait.
    choices.append((tuple(robots), tuple(r_avail)))
    # Second option, build one new robot (if possible)
    for r in range(costs.shape[0]):
        r_new = tuple(r_avail[i] - c for i, c in enumerate(costs[r]))
        m_new = tuple(x + int(i == r) for i, x in enumerate(minerals))
        if any(r < 0 for r in r_new):
            continue
        print(f"    - creating robot {r} (cost={costs[r]}): robots={m_new} minerals={r_new}")
        choices.append((r_new, m_new))
    scores = []
    for (r_new, m_new) in choices:
        scores.append(memo_produced(cache, costs, r_new, m_new, clock + 1))
    return max(scores)


def part_1(costs):
    import matplotlib.pyplot as plt
    r_init = (1, 0, 0, 0)
    s_init = (0, 0, 0, 0)
    prod = optimal_prod(2, 1, 0, 5)
    plt.plot(prod, marker='o')
    plt.show()
    # cache = {}
    # return memo_produced(cache, costs[0], r_init, s_init, 1)
    # t_max = [np.max(costs, axis=0)

    # print(t_max)
    return None


def part_2(input):
    return 2 * len(input)


def aoc_inputs():
    return {
        "example": ("day19-input-ex", 4, 8),
    }
