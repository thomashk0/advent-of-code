import re
from dataclasses import dataclass, field
from typing import Any

import numpy as np

LINE_RE = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
)


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


def tuple_add(xs, ys):
    return tuple(x + y for x, y in zip(xs, ys))


def tuple_sub(xs, ys):
    return tuple(x - y for x, y in zip(xs, ys))


def prod_time(target, bots, minerals):
    """
    Number of cycles before we can start building the given bot.
    """
    if minerals >= target:
        return 0
    if bots == 0:
        return -1
    return (target - minerals + bots - 1) // bots


def prod_time_slow(target, bots, minerals):
    if minerals >= target:
        return 0
    if bots == 0:
        return -1
    c = minerals
    step = 0
    while c < target:
        step += 1
        c += bots
    return step


def bot_prod_time(costs, bots, minerals):
    t_max = 0
    for c, b, m in zip(costs, bots, minerals):
        if c == 0:
            continue
        t = prod_time(c, b, m)
        if t == -1:
            return -1
        t_max = max(t_max, t)
    return t_max


def sanity_check():
    for k in range(6):
        for i in range(12):
            for j in range(12):
                p_ref = prod_time(k, i, j)
                p_actual = prod_time_slow(k, i, j)
                if p_ref != p_actual:
                    print("failed", i, j, p_ref, p_actual)
                assert p_ref == p_actual


@dataclass
class Ctx:
    costs: np.ndarray
    max_needed: np.ndarray
    cache: Any = field(default_factory=dict)


def next_configs(ctx, minerals, bots, remaining):
    minerals = list(minerals)
    for i, m in enumerate(minerals):
        if 0 < ctx.max_needed[i] <= bots[i]:
            minerals[i] = min(minerals[i], ctx.max_needed[i])
        if i < 3:
            minerals[i] = min(minerals[i], 50)
    minerals = tuple(minerals)
    for i, (b, cost) in enumerate(zip(bots, ctx.costs)):
        if 0 < ctx.max_needed[i] <= bots[i]:
            # print(minerals)
            continue
        delay = bot_prod_time(cost, bots, minerals)
        if delay == -1 or delay >= remaining:
            continue
        new_minerals = tuple(
            m - c + (delay + 1) * bb for m, c, bb in zip(minerals, cost, bots)
        )
        if any(m < 0 for m in new_minerals):
            raise NotImplemented("unreachable")
        new_bots = tuple(x + int(j == i) for j, x in enumerate(bots))
        yield new_minerals, new_bots, delay + 1
    minerals_without_bots = tuple(m + remaining * b for m, b in zip(minerals, bots))
    yield minerals_without_bots, bots, remaining


def memo_optimal_prod(ctx: Ctx, minerals, bots, duration):
    key = minerals, bots, duration
    v = ctx.cache.get(key)
    if v is not None:
        return v
    r = optimal_prod(ctx, minerals, bots, duration)
    if len(ctx.cache) > 4e6:
        import itertools

        to_remove = list(itertools.islice(ctx.cache.keys(), 0, 1000 * 1000))
        for k in to_remove:
            del ctx.cache[k]

    ctx.cache[key] = r
    return r


def optimal_prod(ctx: Ctx, minerals, bots, duration):
    if duration <= 0:
        return minerals[3]
    best = 0
    for m_new, b_new, delta in next_configs(ctx, minerals, bots, duration):
        # TODO: shrink minerals
        best = max(best, memo_optimal_prod(ctx, m_new, b_new, duration - delta))
    return best


def part_1(costs):
    # return 1389
    sanity_check()
    r_init = (1, 0, 0, 0)
    s_init = (0, 0, 0, 0)

    quality_level = 0
    scores = []
    for i in range(len(costs)):
        c = costs[i]
        ctx = Ctx(costs=c, max_needed=np.max(c, axis=0), cache={})
        r = memo_optimal_prod(ctx, s_init, r_init, 24)
        scores.append(r)
        print(r)
        quality_level += (i + 1) * r
    print(scores)
    return quality_level


def part_2(costs):
    r_init = (1, 0, 0, 0)
    s_init = (0, 0, 0, 0)
    xs = []
    for i in range(0, 3):
        c = costs[i]
        ctx = Ctx(costs=c, max_needed=np.max(c, axis=0), cache={})
        r = memo_optimal_prod(ctx, s_init, r_init, 32)
        print(r)
        xs.append(r)
    return xs[0] * xs[1] * xs[2]


def aoc_inputs():
    return {
        # "example": ("day19-input-ex", 33, 8),
        "real": (
            "day19-input-1",
            1389,
            None,
        )  ## 1035 your answer is too low, 1115: too low, 1299: too low
    }
