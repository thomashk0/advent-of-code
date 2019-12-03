/// NOTE: This solution is purely iterative.
/// An iteration is made of a downward vertical expansion, followed by
/// a baking step once a wall is hit. The baking might produce new fallout points
/// to be expanded vertically during the next iteration. This approach is
/// pretty efficient, but makes code a bit complex and I'm not 100% sure it
/// covers all case of a water simulation (just enough to solve the AoC
/// problem :p).
///
/// TODO: Another possible solution is a pure cell-based simulation => may lead to cleaner code
/// TODO: Some people used recursion...
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <unordered_set>
#include <algorithm>
#include <vector>
#include <cassert>

namespace
{
    using Scalar = std::int32_t;

    struct Position
    {
        Scalar x{};
        Scalar y{};

        auto operator==(Position const &other) const -> bool
        {
            return x == other.x && y == other.y;
        }

        /// Returns a **copy** of the current location shifted by a given vector
        auto shifted(Position p) const noexcept -> Position
        {
            p.x += x;
            p.y += y;
            return p;
        }

        auto above() const noexcept -> Position
        {
            return shifted({0, -1});
        }

        auto below() const noexcept -> Position
        {
            return shifted({0, 1});
        }

        auto left() const noexcept -> Position
        {
            return shifted({-1, 0});
        }

        auto right() const noexcept -> Position
        {
            return shifted({1, 0});
        }

        struct DefaultHash
        {
            auto operator()(Position const &p) const -> std::size_t
            {
                return static_cast<std::uint64_t>(p.x) << 32 |
                       static_cast<std::uint64_t>(p.y);
            }
        };
    };

    // Sparse representation of positions
    using PositionSet = std::unordered_set<Position, typename Position::DefaultHash>;

    struct Map
    {
        PositionSet walls{};

        auto upper_left() const -> Position
        {
            auto min_x = std::min_element(walls.begin(), walls.end(),
                                          [](auto p, auto q) {
                                              return p.x < q.x;
                                          })->x;
            auto min_y = std::min_element(walls.begin(), walls.end(),
                                          [](auto p, auto q) {
                                              return p.y < q.y;
                                          })->y;
            return {min_x, min_y};
        }

        auto lower_right() const -> Position
        {
            auto max_x = std::max_element(walls.begin(), walls.end(),
                                          [](auto p, auto q) {
                                              return p.x < q.x;
                                          })->x;
            auto max_y = std::max_element(walls.begin(), walls.end(),
                                          [](auto p, auto q) {
                                              return p.y < q.y;
                                          })->y;
            return {max_x, max_y};
        }

        auto is_wall(Position p) const -> bool
        {
            return (walls.count(p) == 1);
        }
    };

    class Sim
    {
        Map const *map_;
        Position upper_left;
        Position lower_right;
        PositionSet water_;
        std::vector<Position> expand_;
        PositionSet explored_;

    public:
        explicit Sim(Map const *map) : map_{map}, upper_left{map->upper_left()},
                                       lower_right(map->lower_right()),
                                       water_{},
                                       expand_{}, explored_{}
        {
            expand_.push_back({500, 0});
        }

        auto reached_bottom(Position p) const -> bool
        {
            return p.y == lower_right.y;
        }

        auto is_wall(Position p) const -> bool
        {
            return map_->is_wall(p);
        }

        auto in_map_range(Position p) const -> bool
        {
            return (p.y >= upper_left.y) && (p.y <= lower_right.y);
        }

        auto is_water(Position p) const -> bool
        {
            return water_.count(p) == 1;
        }

        auto is_explored(Position p) const -> bool
        {
            return explored_.count(p) == 1;
        }

        auto is_empty(Position p) const -> bool
        {
            return !is_wall(p) && !is_water(p);
        }

        void draw()
        {
            for (Scalar y = upper_left.y - 1; y <= lower_right.y + 1; y++) {
                printf("%4d ", y);
                for (Scalar x = upper_left.x - 1; x <= lower_right.x + 1; x++) {
                    if (water_.count({x, y})) {
                        printf("\x1b[96m~\x1b[39m");
                    } else if (map_->walls.count({x, y})) {
                        putchar('#');
                    } else {
                        printf("\x1b[90m.\x1b[39m");
                    }
                }
                printf("\n");
            }
            printf("\n");
        }

        auto find_empty_cell(Position p, Scalar dir) -> Position
        {
            while (is_wall(p)) { p.x += dir; }
            return p;
        }

        /// Fill vertically with water until a wall is found. Returns
        /// std::nullopt if bottom is reached.
        auto water_fall(Position from) -> std::optional<Position>
        {
            while (!is_wall(from)) {
                water_.insert(from);
                if (reached_bottom(from)) { return std::nullopt; }
                from.y += 1;
            }
            return from;
        }

        auto horizontal_bake(Position p, Scalar xmin, Scalar xmax,
                             Scalar dir) -> Position
        {
            while (p.x >= xmin && p.x <= xmax) {
                if (is_wall(p)) {
                    break;
                }
                water_.insert(p);
                if (is_empty(p.below())) {
                    water_fall(p.below());
                }
                p.x += dir;
            }
            return p;
        }

        auto bake(Position p)
        {
            assert(is_wall(p));
            auto xmin = find_empty_cell(p, -1).right().x;
            auto xmax = find_empty_cell(p, 1).left().x;

            bool done = false;
            while (!done) {
                p.y -= 1;
                auto fill_l = horizontal_bake(p, xmin, xmax, -1);
                auto fill_r = horizontal_bake(p, xmin, xmax, 1);
                if (fill_l.x < xmin) {
                    expand_.push_back(fill_l);
                    done = true;
                }
                if (fill_r.x > xmax) {
                    expand_.push_back(fill_r);
                    done = true;
                }
            }
        }

        auto step() -> bool
        {
            static std::vector<Position> buff;
            buff = expand_;
            expand_.clear();

            for (Position el : buff) {
                if (is_explored(el)) { continue; }
                explored_.insert(el);
                auto floor_hit = water_fall(el);
                if (!floor_hit.has_value()) {
                    continue;
                }
                bake(*floor_hit);
            }
            return expand_.empty();
        }

        // Follow water path from source and remove "1 layer" of water
        auto drain()
        {
            std::vector<Position> next;
            std::vector<Position> current;
            next.reserve(128);
            current.reserve(128);

            auto clean = [&](Position p, Scalar dir) {
                while(is_water(p)) {
                    water_.erase(p);
                    p.x += dir;
                }
                return p;
            };
            next.push_back({500, 0});

            while (true) {
                current = next;
                next.clear();

                for (auto el: current) {
                    if (!is_water(el)) { continue; }

                    if (is_water(el.left()) || is_water(el.right())) {
                        Position next_l = clean(el.left(), -1);
                        if (!is_wall(next_l)) {
                            next.push_back(next_l.right().below());
                        }
                        Position next_r = clean(el.right(), 1);
                        if (!is_wall(next_r)) {
                            next.push_back(next_r.left().below());
                        }
                    } else {
                        next.push_back(el.below());
                    }
                    water_.erase(el);
                }
                if (next.empty()) { break; }
            }
        }

        auto result() const noexcept
        {
            std::size_t cnt{0};
            for (auto&& el : water_) {
                if (in_map_range(el)) {
                    cnt++;
                }
            }
            return cnt;
        }
    };


    Map parse_map(char const *filepath)
    {
        Map map{};
        auto f = fopen(filepath, "r");
        auto parse_fail = [] {
            fprintf(stderr, "%s:%d: parsing failed.\n", __FILE__, __LINE__);
            exit(1);
        };
        while (true) {
            char c;
            if (fscanf(f, " %c", &c) == EOF) {
                break;
            }

            switch (c) {
                case 'x': {
                    Scalar x, y_begin, y_end;
                    auto n_read = fscanf(f, "=%d, y=%d..%d\n", &x, &y_begin,
                                         &y_end);
                    if (n_read != 3) {
                        parse_fail();
                    }
                    for (Scalar y = y_begin; y <= y_end; y++) {
                        map.walls.insert(Position{x, y});
                    }
                }
                    break;
                case 'y': {
                    Scalar x_begin, x_end, y;
                    auto n_read = fscanf(f, "=%d, x=%d..%d\n", &y, &x_begin,
                                         &x_end);
                    if (n_read != 3) {
                        parse_fail();
                    }
                    for (Scalar x = x_begin; x <= x_end; x++) {
                        map.walls.insert(Position{x, y});
                    }
                }
                    break;
                default:
                    parse_fail();
            }
        }
        return map;
    }
}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }

    puts("~~~ Advent of code 2018 -- Day 17 ~~~\n");
    auto m = parse_map(argv[1]);
    printf("map_size: %zu\n", m.walls.size());
    auto upper_left = m.upper_left();
    auto lower_right = m.lower_right();
    printf("xmin, xmax = %d, %d\n", upper_left.x, lower_right.x);
    printf("ymin, ymax = %d, %d\n", upper_left.y, lower_right.y);

    Sim sim(&m);
    constexpr std::size_t max_step = 2000;

    puts("# Part 1\n");
    bool sim_finished = false;
    for (std::size_t i = 0; i < max_step; i++) {
        sim_finished = sim.step();
        if (sim_finished) {
            sim.draw();
            printf("solution: %zu\n", sim.result());
            break;
        }
    }
    if (!sim_finished) {
        fprintf(stderr, "simulation reached max step count...\n");
        return 1;
    }

    puts("# Part 2\n");
    sim.drain();
    sim.draw();
    printf("solution: %zu", sim.result());

    return 0;
}

