import copy
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

LINE_RE = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)

NODES = {"ore": 0, "clay": 1, "obs": 2, "geode": 3}


def parse_input(raw: str):
    costs = []
    for line in raw.splitlines():
        cost_matrix = np.zeros((4, 4), dtype=np.int64)
        m = LINE_RE.match(line)
        (
            _i,
            ore_cost,
            clay_cost,
            obs_cost_ore,
            obs_cost_clay,
            geode_cost_ore,
            geode_cost_obs,
        ) = m.groups()
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


def optimal_production(cost, bots, minerals, duration):
    # Production if no robots are created.
    choices = []
    for b in range(0, duration):
        new_minerals = minerals - cost * b
        for step in range(0, duration):
            new_minerals += bots + min(step, b)
        choices.append(new_minerals)
    return choices


# def tmin_to_produce(cost, bots, minerals, target):
#     if minerals > target:
#         return 0
#     remaining = target - minerals
#     # Worst case time
#     t_min = (remaining + bots - 1) // bots
#     choices = []
#     for b in range(0, t_min):
#         new_minerals = minerals - cost * b
#         for step in range(0, t_min):
#             new_minerals += bots + min(step, b)
#             if new_minerals > target:
#                 choices.append(t_min)
#     return min(t_min, min(choices))

# def prod_time(costs, target, t):
#     if t == 0:
#     choices = []
#     for i, d in enumerate(costs[t]):
#         choices.append(prod_time(costs, target * d, i))
#     return max(choices) + 1


# def optimal_prod(cost, bots, minerals, duration, bot):
#     # Production if no robots are created.
#     choices = []
#     for b in range(0, duration):
#         new_minerals = minerals - cost * b
#         for step in range(0, duration):
#             new_minerals += bots + min(step, b)
#         choices.append(new_minerals)
#     return choices

# def optimal_cray_prod(cost, bot, minerals, duration):
#     pass


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
        print(
            f"    - creating robot {r} (cost={costs[r]}): robots={m_new} minerals={r_new}"
        )
        choices.append((r_new, m_new))
    scores = []
    for (r_new, m_new) in choices:
        scores.append(memo_produced(cache, costs, r_new, m_new, clock + 1))
    return max(scores)


#
# @dataclass(order=True)
# class Config:
#     priority: int
#     # minerals: Tuple[int, int, int, int] = field(compare=False)
#     # bots: Tuple[int, int, int, int] = field(compare=False)


# def cost_in_ore(costs, row):
#     if row == 0:
#         return 1
#     return sum(cost_in_ore(costs, i) for i, r in enumerate(costs[row]) if r != 0)


def part_1(costs):
    r_init = (1, 0, 0, 0)
    s_init = (0, 0, 0, 0)

    c = costs[0]
    print(c)
    print(optimal_production(c[0, 0], 3, 0, 24))
    # print("  - clay:", cost_in_ore(c, 1))
    # print("  - obs:", cost_in_ore(c, 2))
    # print("  - geode:", cost_in_ore(c, 3))
    plt.plot(optimal_production(c[0, 0], 1, 0, 24), label="ore", marker="o")
    plt.plot(optimal_production(c[1, 0] * c[0, 0], 0, 0, 24), label="clay", marker="o")
    plt.legend()
    plt.show()

    return None
    # prod = optimal_prod(2, 1, 0, 5)
    plt.plot(prod, marker="o")
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
