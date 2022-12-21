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


def optimal_production(cost, bots, minerals, duration):
    choices = []
    for b in range(0, duration):
        new_minerals = minerals - cost * b
        for step in range(0, duration):
            new_minerals += bots + min(step, b)
        choices.append(new_minerals)
    return choices


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


# @dataclass
# class Context:
#     cache: Any

def is_optimal(costs, robots):
    # Can we produce one robot per cycle?
    for r, c in zip(robots, costs):
        if c != 0 and r < c:
            return False
    return True


# def explore(costs, duration):
#     config =
#     for i in range(duration):
#         pass

# def available_choices(costs, robots, minerals, duration):
#     max_needed = np.sum(costs, axis=0)
#     for bot_id in range(costs.shape[0]):
#         delay = bot_prod_time(costs[bot_id], robots, minerals)
#         if max_needed[bot_id] != 0 and robots[bot_id] == max_needed[bot_id]:
#             continue
#         if delay != -1 and delay < duration:
#             minerals_new = tuple(m + (delay + 1) * b - c for m, b, c in zip(minerals, robots, costs[bot_id]))
#             bots_new = tuple(x + int(i == bot_id) for i, x in enumerate(robots))
#             # FIXME: check delay is correct
#             yield bots_new, minerals_new, delay + 1
#     minerals_without_bots = tuple(m + duration * b for m, b in zip(minerals, robots))
#     yield robots, minerals_without_bots, duration


@dataclass
class Ctx:
    costs: np.ndarray
    max_needed: np.ndarray
    cache: Any = field(default_factory=dict)


def next_configs(ctx, minerals, bots, remaining):
    for i, (b, cost) in enumerate(zip(bots, ctx.costs)):
        if 0 < ctx.max_needed[i] <= bots[i]:
            continue
        delay = bot_prod_time(cost, bots, minerals)
        if delay == -1 or delay >= remaining:
            continue
        new_minerals = tuple(m - c + (delay + 1) * bb for m, c, bb in zip(minerals, cost, bots))
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


def valid_configs(ctx: Ctx, minerals, bots):
    for i in range(len(bots)):
        if 0 < ctx.max_needed[i] <= bots[i]:
            continue
        new_minerals = minerals - ctx.costs[i]
        if np.any(new_minerals < 0):
            continue
        new_bots = np.copy(bots)
        new_bots[i] += 1
        yield new_minerals + bots, new_bots
    yield minerals + bots, bots


def memo_explore(ctx, remaining, minerals, bots):
    key = remaining, tuple(minerals), tuple(bots)
    v = ctx.cache.get(key)
    if v is not None:
        return v
    r = explore(ctx, remaining, minerals, bots)
    ctx.cache[key] = r
    return r


def explore(ctx: Ctx, remaining, minerals, bots):
    if remaining == 0:
        return minerals, bots
    # print(f"\nexplore(remaining={remaining}): minerals={minerals}, bots={bots}")
    choices = list(valid_configs(ctx, minerals, bots))
    # for c in choices:
    #     print(f"   - {c}")
    configs = list(memo_explore(ctx, remaining - 1, m, b) for m, b in choices)
    # Idea: truncate the number of minerals (too much minerals is useless!) => prevents caching...
    #
    return max(configs, key=lambda x: tuple(reversed(x[0])))


def greedy_explore(ctx: Ctx, duration, minerals, bots):
    for i in range(duration):
        search_depth = min(duration - i, 11)
        scores = []
        for m, b in valid_configs(ctx, minerals, bots):
            scores.append(((m, b), memo_explore(ctx, search_depth, m, b)))
        # print(f"step={i}:")
        # for cfg, r in scores:
        #     print(f"  - {cfg} ==> {r}")
        best_m, best_b = max(scores, key=lambda x: tuple(reversed(x[1][0])))[0]
        minerals, bots = best_m, best_b
        # print(f"  * selecting: {minerals} {bots}")
    return minerals, bots


def part_1(costs):
    sanity_check()
    r_init = (1, 0, 0, 0)
    s_init = (0, 0, 0, 0)
    # c = costs[1]
    # ctx = Ctx(costs=c, max_needed=np.max(c, axis=0), cache={})
    # print("valid configs:")
    # for cfg in next_configs(ctx, s_init, r_init, 5):
    #     print(f"- {cfg}")
    # print(memo_optimal_prod(ctx, s_init, r_init, 24))
    # return

    quality_level = 0
    scores = []
    for i in range(len(costs)):
        c = costs[i]
        ctx = Ctx(costs=c, max_needed=np.max(c, axis=0), cache={})
        # print(explore(ctx, 10, np.zeros(4, dtype=np.int64), np.array([1, 0, 0, 0], dtype=np.int64)))
        # r = greedy_explore(ctx, 24, np.zeros(4, dtype=np.int64), np.array([1, 0, 0, 0], dtype=np.int64))
        r = memo_optimal_prod(ctx, s_init, r_init, 24)
        scores.append(r)
        print(r)
        quality_level += (i + 1) * r
    print(scores)
    return quality_level


def part_2(input):
    return 2 * len(input)


def aoc_inputs():
    return {
        # "example": ("day19-input-ex", 33, 8),
        "real": ("day19-input-1", None, None)  ## 1035 your answer is too low, 1115: too low, 1299: too low
    }
