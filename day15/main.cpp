#include <cstdio>
#include <cstdint>
#include <vector>
#include <cstdlib>
#include <array>
#include <fstream>
#include <algorithm>

namespace
{
    namespace details
    {
        template<typename T>
        constexpr auto abs(T x) -> T
        {
            return x > 0 ? x : -x;
        }
    }

    using u8 = std::uint8_t;
    using Health = std::uint32_t;
    using Index = std::int32_t;

    struct Location
    {
        Index x;
        Index y;

        auto operator<(Location& other) const -> bool
        {
            return (y < other.y) || (x < other.x);
        }

        constexpr auto distance(Location p) const
        {
            return details::abs(x - p.x) + details::abs(y - p.y);
        }
    };

    constexpr auto moves = std::array<Location, 4>{Location{0, -1}, {1, 0}, {0, 1}, {-1, 0}};

    struct Map
    {
        std::vector<char> data;
        Index w;
        Index h;

        constexpr auto in_range(Location p) const -> bool
        {
            return (p.x >= 0) && (p.x < w) && (p.y >= 0) && (p.y < h);
        }
    };

    enum class Type : char
    {
        Elf,
        Goblin
    };

    struct GameState
    {
        std::vector<Location> loc;
        std::vector<Health> health;
        std::vector<Type> type;
    };

    auto parse_map(std::string_view filename) -> Map
    {
        Map map{};
        Index y{0};
//        auto process_line = [&](auto&& s) {
//            Index x{0};
//            for (auto&& c : s) {
//
//                x++;
//            }
//            std::transform(s.begin(), s.end(), std::back_inserter(map.data), [](char c) {
//                if (c == 'G' || c == 'E') {
//                    return '.';
//                }
//                return c;
//            });
//            y++;
//        };
        std::ifstream file(filename.data());

        if (file.is_open()) {
            std::string line;
            if (!std::getline(file, line)) {
                throw std::runtime_error("unable to parse map");
            }
            printf("%zu\n", line.size());

            while (std::getline(file, line)) {

                // using printf() in all tests for consistency
                printf("%s\n", line.c_str());
            }
        }
        return map;
    }
}

int main(int argc, char** argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }
    parse_map(argv[1]);

    puts("~~~ Advent of code 2018 -- Day 15 ~~~\n");
}