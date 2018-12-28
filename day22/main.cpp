#include <aoc.h>
#include <numeric>
#include <queue>

namespace
{
    using Scalar = int;

    enum class RegionType : char
    {
        undefined = 0,
        rocky = '.',
        narrow = '|',
        wet = '='
    };

    struct Region
    {
        Scalar geolitic_level{0};
        RegionType type{RegionType::undefined};

        auto risk() const noexcept -> Scalar
        {
            switch (type) {
                case RegionType::rocky:
                    return 0;
                case RegionType::wet:
                    return 1;
                case RegionType::narrow:
                    return 2;
                case RegionType::undefined:
                    exit(1);
            }
            return 0;
        }
    };

    using Coord = aoc::Vec2<Scalar>;
    using Map = aoc::Dense2dMap<int, Region>;
    using SparseMap = aoc::Sparse2dMap<int, Region>;

    enum class Equip : char
    {
        torch,
        climbing,
        neither
    };

    auto equip_str(Equip equip) -> char const*
    {
        switch (equip)
        {
            case Equip::torch: return "torch";
            case Equip::climbing: return "climbing";
            case Equip::neither: return "neither";
        }
        return "?";
    }

    constexpr std::initializer_list<Equip> equips = {Equip::torch, Equip::climbing, Equip::neither};

    struct State
    {
        Coord loc{0, 0};
        Equip equip{Equip::torch};

        constexpr auto operator==(State const &other) const noexcept -> bool
        {
            return (loc == other.loc) && (equip == other.equip);
        }

        void dump() const
        {
            printf("(%d, %d) with %s", loc.x, loc.y, equip_str(equip));
        }

        struct DefaultHash
        {
            constexpr auto
            operator()(State const &s) const noexcept -> std::size_t
            {
                return Coord::DefaultHash()(s.loc) ^ static_cast<std::size_t>(s.equip);
            }
        };
    };

    auto is_valid_equip(RegionType type, Equip equip) noexcept -> bool {
        switch (type) {
            case RegionType::rocky: return equip != Equip::neither;
            case RegionType::narrow: return equip != Equip::climbing;
            case RegionType::wet: return equip != Equip::torch;
            default:
                return true;
        }
    }

    auto erosion_level(int depth, Region r) -> Scalar
    {
        return (depth + r.geolitic_level) % 20183;
    }

    auto make_region(int depth, Scalar geolitic_level)
    {
        RegionType t{RegionType::undefined};
        auto erosion_mod3 = ((depth + geolitic_level) % 20183) % 3;
        if (erosion_mod3 == 0) {
            t = RegionType::rocky;
        } else if (erosion_mod3 == 1) {
            t = RegionType::wet;
        } else {
            t = RegionType::narrow;
        }
        return Region{geolitic_level, t};
    }

    constexpr std::initializer_list<Coord> moves = {{1, 0}, {-1, 0}, {0, -1}, {0, 1}};

    struct Solver
    {
        Scalar depth;
        Coord target;
        SparseMap map;

        auto is_valid(State s) -> bool
        {
            if (s.loc.x < 0 || s.loc.y < 0) {
                return false;
            }
            auto type = get_tile(s.loc).type;
            return is_valid_equip(type, s.equip);
        }

        // A*-like path finding algorithm
        auto explore() -> int
        {
            std::unordered_map<State, int, typename State::DefaultHash> explored;

            auto compare = [&](State const &x, State const &y) -> bool {
                auto cx = explored[x] + aoc::manhattan_distance(x.loc, target);
                auto cy = explored[y] + aoc::manhattan_distance(y.loc, target);
                return cx > cy;
            };
            std::priority_queue<State, std::vector<State>, decltype(compare)> q{compare};
            auto insert_node = [&](State const& s, int elapsed) {
                if (!is_valid(s)) { return; }
                auto it = explored.find(s);
                if (it != explored.end() && it->second <= elapsed) {
                    return;
                }
                explored[s] = elapsed;
                q.push(s);
            };

            q.push(State{});
            while (q.size() > 0) {
                State top = q.top();
                // printf("exploring "); top.dump();
                q.pop();
                auto elapsed = explored[top];
                if (top.loc == target && top.equip == Equip::torch) {
                    return elapsed;
                }
                for (auto&& m : moves) {
                    auto snext = top;
                    snext.loc += m;
                    insert_node(snext, elapsed + 1);
                }
                for (auto&& equip : equips) {
                    if (equip == top.equip) {
                        continue;
                    }
                    auto snext = top;
                    snext.equip = equip;
                    insert_node(snext, elapsed + 7);
                }
            }
            return 0;
        }

        auto get_tile(Coord p) -> Region
        {
            auto it = map.data.find(p);
            if (it != map.data.end()) {
                return it->second;
            }
            auto create_tile = [&]() -> Region {
                if (((p.x == 0) && (p.y == 0)) || (p == target)) {
                    return make_region(depth, 0);
                } else if (p.x == 0) {
                    return make_region(depth, (48271 * p.y) % 20183);
                } else if (p.y == 0) {
                    return make_region(depth, (16807 * p.x) % 20183);
                } else {
                    auto left = get_tile(p.shifted({-1, 0}));
                    auto up = get_tile(p.shifted({0, -1}));
                    Scalar geolitic_level = (erosion_level(depth, left) *
                                             erosion_level(depth, up)) % 20183;
                    return make_region(depth, geolitic_level);
                }
            };
            auto r = create_tile();
            map.data[p] = r;
            return r;
        }

        // pre-compute some most of the map
        void populate()
        {
            get_tile({0, 0});
            get_tile(target.left());
            get_tile(target.above());
            get_tile(target);
        }
    };

    auto build_map(int depth, Coord target) -> Map
    {
        Map m{target.x + 1, target.y + 1, Region{}};
        m.data[0] = make_region(depth, 0);
        for (Scalar y = 1; y < m.h; y++) {
            m.data[y * m.w] = make_region(depth, (48271 * y) % 20183);
        }
        for (Scalar x = 1; x < m.w; x++) {
            m.data[x] = make_region(depth, (16807 * x) % 20183);
        }

        for (Scalar x = 1; x < m.w; x++) {
            for (Scalar y = 1; y < m.h; y++) {
                Scalar index =
                        (erosion_level(depth, m.data[(y - 1) * m.w + x]) *
                         erosion_level(depth, m.data[y * m.w + (x - 1)])) %
                        20183;
                m.data[y * m.w + x] = make_region(depth, index);
            }
        }
        m.data[target.y * m.w + target.x] = make_region(depth, 0);
        return m;
    }


    void part_1(int depth, Coord target)
    {
        auto m = build_map(depth, target);
        m.draw_ascii([](Region x) {
            if (x.type == RegionType::undefined) {
                return '?';
            } else {
                return static_cast<char>(x.type);
            }
        });
        printf("Part1: %d\n", std::accumulate(m.data.begin(), m.data.end(), 0,
                                              [](auto acc, auto x) {
                                                  return acc + x.risk();
                                              }));
    }

    void part_1_bis(int depth, Coord target)
    {
        auto s = Solver{depth, target, {}};
        s.populate();
        auto m = s.map.freeze(Region{});
        m.draw_ascii([](Region x) {
            if (x.type == RegionType::undefined) {
                return '?';
            } else {
                return static_cast<char>(x.type);
            }
        });
        printf("Part1: %d\n", std::accumulate(m.data.begin(), m.data.end(), 0,
                                              [](auto acc, auto x) {
                                                  return acc + x.risk();
                                              }));
    }

    auto part_2(int depth, Coord target) -> int
    {
        auto s = Solver{depth, target, {}};
        s.populate();
        return s.explore();
    }
}

int main(int, char **)
{
    part_1(510, {10, 10});
    part_1_bis(510, {10, 10});
    // real input:
    //      > depth: 3558
    //      > target: 15,740
    part_1(3558, {15, 740});
    part_1_bis(3558, {15, 740});
    printf("Part2: %d\n", part_2(510, {10, 10}));
    printf("Part2: %d\n", part_2(3558, {15, 740}));
    return 0;
}