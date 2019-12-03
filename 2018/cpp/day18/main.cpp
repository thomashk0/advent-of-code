#include <cstdio>
#include <vector>
#include <cstdint>
#include <array>
#include <fstream>
#include <algorithm>
#include <optional>

#include <aoc/utils.h>

namespace
{
    using Index = std::int32_t;

    enum class Acre : char
    {
        Ground = '.',
        Tree = '|',
        Lumberyard = '#'
    };

    struct Point
    {
        Index x;
        Index y;

        constexpr auto operator==(Point const &other) const -> bool
        {
            return x == other.x && y == other.y;
        }
    };

    struct Map
    {
        std::vector<Acre> data{};
        Index dim{0};

        using AdjacentAcres = aoc::StaticVector<Point, 8>;

        explicit Map(std::string_view filename)
        {
            std::ifstream file(filename.data());
            if (!file.is_open()) {
                throw std::runtime_error("unable to open file");
            }

            std::string line;
            if (!std::getline(file, line)) {
                throw std::runtime_error("unable to parse map");
            }
            dim = line.size();
            data.reserve(dim * dim);

            auto it = std::back_inserter(data);
            it = std::transform(line.begin(), line.end(), it,
                                [](char c) { return static_cast<Acre>(c); });
            for (std::size_t j = 1; j < dim; j++) {
                if (!std::getline(file, line)) {
                    throw std::runtime_error("unable to parse map");
                }
                if (line.size() != dim) {
                    throw std::runtime_error(
                            "parsing failed: bad line length");
                }
                it = std::transform(line.begin(), line.end(), it,
                                    [](char c) { return static_cast<Acre>(c); });
            }
        }

        auto adjacent_acres(Index x, Index y) const -> AdjacentAcres
        {
            std::initializer_list<Point> p = {
                    Point{x - 1, y - 1},
                    Point{x - 1, y},
                    Point{x - 1, y + 1},
                    Point{x, y - 1},
                    Point{x, y + 1},
                    Point{x + 1, y - 1},
                    Point{x + 1, y},
                    Point{x + 1, y + 1},
            };
            AdjacentAcres result{};
            std::copy_if(p.begin(), p.end(), std::back_inserter(result),
                         [&](Point p) {
                             return (p.x >= 0 && p.x < dim) &&
                                    (p.y >= 0 && p.y < dim);
                         });
            return result;
        }

        auto at(Index x, Index y) const -> Acre
        {
            return data[y * dim + x];
        }

        auto at(Point p) const -> Acre
        {
            return at(p.x, p.y);
        }

        void draw()
        {
            for (Index y = 0; y < dim; y++) {
                for (Index x = 0; x < dim; x++) {
                    putchar(static_cast<char>(at(x, y)));
                }
                puts("");
            }
        }

        auto update_acre(Index x, Index y) const -> Acre
        {
            auto neighbours = adjacent_acres(x, y);
            auto n_trees = std::count_if(neighbours.begin(), neighbours.end(),
                                      [&](Point p) { return at(p) == Acre::Tree; });
            auto n_lumberyard =
                    std::count_if(neighbours.begin(), neighbours.end(),
                               [&](Point p) {
                                   return at(p) == Acre::Lumberyard;
                               });
            auto acre = data[y * dim + x];
            switch (acre) {
                case Acre::Ground:
                    if (n_trees >= 3) { return Acre::Tree; }
                    break;
                case Acre::Tree:
                    if (n_lumberyard >= 3) { return Acre::Lumberyard; }
                    break;
                case Acre::Lumberyard:
                    if (n_lumberyard == 0 || n_trees == 0) {
                        return Acre::Ground;
                    }
                    break;
            }
            return acre;
        }

        void step()
        {
            static std::vector<Acre> next;
            next.clear();

            for (Index y = 0; y < dim; y++) {
                for (Index x = 0; x < dim; x++) {
                    next.push_back(update_acre(x, y));
                }
            }
            std::copy(next.begin(), next.end(), data.begin());
        }

        auto result() -> Index {
            Index n_wood{0};
            Index n_lumberyard{0};
            for (Acre acre : data) {
                switch (acre) {
                    case Acre::Ground: break;
                    case Acre::Tree:
                        n_wood++;
                        break;
                    case Acre::Lumberyard:
                        n_lumberyard++;
                        break;
                }
            }
            return n_lumberyard * n_wood;
        }
    };

    void part_1(std::string_view filename)
    {
        puts("# Part 1\n");
        Map m(filename);
        m.draw();
        for (int i = 0; i < 10; i++) {
            printf("After %3d minutes\n", i);
            m.step();
            m.draw();
        }
        m.draw();
        printf("result: %d\n", m.result());
    }

    auto search_period(Map const& ref, Index max) -> std::optional<Index>
    {
        Map m = ref;
        for (Index i = 1; i < max; i++) {
            m.step();
            if (std::equal(m.data.begin(), m.data.end(), ref.data.begin())) {
                return i;
            }
        }
        return std::nullopt;
    }

    void part_2(std::string_view filename, Index target, Index start, Index max=1000)
    {
        puts("# Part 2\n");
        Map m(filename);
        for (Index i = 0; i < start; i++) {
            m.step();
        }
        auto period = search_period(m, max);
        if (!period.has_value()) {
            fprintf(stderr, "unable to identify period, try with higher limit?\n");
            exit(1);
        }
        printf("found period: %d\n", *period);

        for (Index i = 0; i < (target - start) % *period; i++) {
            m.step();
        }
        printf("result: %d\n", m.result());
    }
}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }
    puts("~~~ Advent of code 2018 -- Day 18 ~~~\n");

    part_1(argv[1]);
    part_2(argv[1], 1000000000, 1000);
    return 0;
}

