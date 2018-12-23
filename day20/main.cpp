#include <cstdio>
#include <cstdlib>
#include <string_view>
#include <stdexcept>
#include <fstream>
#include <unordered_map>

#include <aoc.h>
#include <cassert>
#include <vector>
#include <variant>
#include <unordered_set>

namespace
{
    using Scalar = int;
    using Point = aoc::Vec2<Scalar>;
    enum class Tile : char
    {
        unknown = 0,
        wall = '#',
        room = '.',
        door_h = '|',
        door_v = '-'
    };

    auto to_char(Tile t) -> char
    {
        switch (t) {
            case Tile::wall:
            case Tile::room:
            case Tile::door_h:
            case Tile::door_v:
                return static_cast<char>(t);
            case Tile::unknown:
                return '?';
            default:
                return 'X';
        }
    }

    using Sparse2dMap = aoc::Sparse2dMap<Scalar, Tile>;
    using Dense2dMap = aoc::Dense2dMap<Scalar, Tile>;
    using PointSet = std::unordered_set<Point, typename Point::DefaultHash>;

    std::string parse_regex(std::string_view filename)
    {
        std::ifstream file(filename.data());
        if (!file.is_open()) {
            throw std::runtime_error("unable to open file");
        }
        std::string regex;
        if (!getline(file, regex)) {
            throw std::runtime_error("parsing failed: need at least one line!");
        }
        if (regex[0] != '^' || regex[regex.size() - 1] != '$') {
            throw std::runtime_error("parsing failed: bad regex format.");
        }
        return regex.substr(1, regex.size() - 2);
    }

    constexpr auto is_direction(char c) noexcept -> bool
    {
        switch(c) {
            case 'N':
            case 'E':
            case 'W':
            case 'S':
                return true;
            default:
                return false;
        }
    }

    constexpr auto to_direction(char c) noexcept -> Point
    {
        switch(c) {
            case 'N': return {0, -1};
            case 'S': return {0, 1};
            case 'E': return {1, 0};
            case 'W': return {-1, 0};
            default:
                return {0, 0};
        }
    }

    auto find_closing(std::string_view s) -> std::pair<std::string_view, std::string_view>
    {
        std::size_t offset = 0;
        int stack = 0;
        for (offset = 0; offset < s.size(); offset++) {
            char c = s[offset];
            if (c == ')') {
                if (stack == 0) { break; }
                stack--;
            } else if (c == '(') {
                stack++;
            }
        }
        if (offset >= s.size()) {
            return {s, ""};
        }
        return {s.substr(0, offset), s.substr(offset + 1)};
    }

    auto alternatives(std::string_view s) -> std::vector<std::string_view>
    {
        std::vector<std::string_view> result;
        int stack = 0;
        std::size_t start = 0, offset;
        for (offset = 0; offset < s.size(); offset++) {
            switch (s[offset]) {
                case '(':
                    stack++;
                    break;
                case ')':
                    stack--;
                    break;
                case '|':
                    if (stack == 0) {
                        result.push_back(s.substr(start, offset - start));
                        start = offset + 1;
                    }
                    break;
                default:
                    break;
            }
        }
        result.push_back(s.substr(start));
        return result;
    }

    auto explore_door(char c, Sparse2dMap &m, Point from) -> Point
    {
        auto dir = to_direction(c);
        from += dir;
        m[from] = (dir.y != 0)?Tile::door_v:Tile::door_h;
        from += dir;
        m[from] = Tile::room;
        return from;
    }

    void explore_map_(Sparse2dMap &m, PointSet &ends, Point start,
                      std::string_view s)
    {
        std::size_t offset = 0;
        for (offset = 0; offset < s.size(); offset++) {
            char c = s[offset];
            if (!is_direction(c)) {
                break;
            }
            start = explore_door(c, m, start);
        }
        if (offset == s.size()) {
            ends.insert(start);
            return;
        }

        char c = s[offset];
        if (c == '(') {
            PointSet tmp{};
            auto [enclosed, rest] = find_closing(s.substr(offset + 1));
            for (auto&& el : alternatives(enclosed)) {
                explore_map_(m, tmp, start, el);
            }
            for (auto&& el : tmp) {
                explore_map_(m, ends, el, rest);
            }
        } else {
            throw std::runtime_error("unexpected result");
        }
    }

    auto create_map(std::string_view s) -> Sparse2dMap {
        Sparse2dMap m;
        PointSet tmp{};
        m[{0, 0}] = Tile::room;
        explore_map_(m, tmp, {0, 0}, s);
        return m;
    }

    constexpr std::initializer_list<Point> adjacent = {
        {1, 0},
        {-1, 0},
        {0, 1},
        {0, -1}
    };

    auto solve(Sparse2dMap const& map) -> std::pair<int, int>
    {
        std::unordered_set<Point, typename Point::DefaultHash> explored;
        std::vector<Point> explore_next = {Point{0, 0}};
        std::vector<Point> explore_current{};
        std::size_t low_count = 0;

        int distance = 0;
        while (true) {
            if (distance == 1000) {
                low_count = explored.size();
            }
            explore_current = explore_next;
            explore_next.clear();
            for (auto p : explore_current) {
                explored.insert(p);
                for (auto dir : adjacent) {
                    Point next = p + dir;
                    if (explored.find(p + 2*dir) != explored.end()) {
                        continue;
                    }
                    auto it = map.data.find(next);
                    if (it == map.data.end()) { continue; }
                    if (it->second == Tile::door_v || it->second == Tile::door_h) {
                        explore_next.push_back(p + 2 * dir);
                    }
                }
            }

            if (explore_next.empty()) {
                break;
            }
            distance++;
        }
        return {distance, (int)(explored.size()) - (int)low_count};
    }

    void draw(Dense2dMap const& m)
    {
        printf("    ");
        for(int i = 0; i < m.w; i++) {
            if (m.xmin + i < 0) { putchar('-'); }
            else { putchar(' '); }
        }
        puts("");
        for (int acc = 1; acc > 0; acc /= 10) {
            printf("    ");
            for(int i = 0; i < m.w; i++) {
                printf("%d", (std::abs(m.xmin + i) / acc) % 10);
            }
            puts("");
        }

        for (Scalar y = 0; y < m.h; y++) {
            printf("%3d ", m.ymin + y);
            for (Scalar x = 0; x < m.w; x++) {
                putchar(to_char(m.data[y * m.w + x]));
            }
            puts("");
        }
    }

    void part_1(std::string_view filename)
    {
        puts("# Part 1\n");
        std::string regex = parse_regex(filename);
        auto m = create_map(regex);
        auto [min_distance, part2] = solve(m);
        printf("result: %d\n\n", min_distance);
        puts("# Part 2\n");
        printf("result: %d\n\n", part2);
    }

    struct TestCase
    {
        std::string_view s;
        int expected;
    };
}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT [part2]", argv[0]);
        exit(1);
    }

    std::vector<TestCase> examples{
            {{"WNE"}, 3},
            {{"W(S(W|)S|N)"}, 4},
            {{"ENWWW(NEEE|SSE(EE|N))"}, 10},
            {{"ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN"}, 18},
            {{"ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))"}, 23},
            {{"WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))"}, 31}
    };

    int id = 0;
    for (auto&& ex : examples) {
        auto m = create_map(ex.s);
        auto result = solve(m).first;
        if (result != ex.expected) {
            printf("Test#%d [FAILED]: got %d instead of %d\n", id, result, ex.expected);
        } else {
            printf("Test#%d [PASSED]: got %d\n", id, result);
        }
        id++;
    }

    constexpr bool debug = false;
    if (debug)
    {
        // Test
        auto m = create_map(examples[1].s);
        // Add surrounding walls
        auto [xmin, xmax] = m.xrange();
        auto [ymin, ymax] = m.yrange();
        m[{xmin - 1, ymin - 1}] = Tile::wall;
        m[{xmax + 1, ymax + 1}] = Tile::wall;

        Dense2dMap map = m.freeze(Tile::wall);
        draw(map);
        printf("result: %d\n", solve(m).first);
    }

    part_1(argv[1]);

    return 0;
}