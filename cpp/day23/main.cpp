#include <cstdio>
#include <array>
#include <fstream>
#include <vector>
#include <algorithm>

namespace
{
    template<typename T, std::size_t N>
    struct Vec
    {
        std::array<T, N> coords{};

        using Scalar = T;

        static constexpr auto dim() noexcept -> std::size_t
        {
            return N;
        }

        constexpr auto operator==(Vec<T, N> const &other) const noexcept -> bool
        {
            return std::equal(coords.begin(), coords.end(),
                              other.coords.begin());
        }

        constexpr auto
        operator+=(Vec<T, N> const &other) noexcept -> Vec<T, N> &
        {
            for (std::size_t i = 0; i < coords.size(); i++) {
                coords[i] += other.coords[i];
            }
            return *this;
        }

        friend constexpr auto operator+(Vec<T, N> p, Vec<T, N> q) -> Vec<T, N>
        {
            p += q;
            return p;
        }

        friend constexpr auto operator+(T x, Vec<T, N> p) -> Vec<T, N>
        {
            for (std::size_t i = 0; i < N; i++) {
                p.coords[i] += x;
            }
            return p;
        }

        friend constexpr auto operator*(T x, Vec<T, N> p) -> Vec<T, N>
        {
            for (std::size_t i = 0; i < N; i++) {
                p.coords[i] *= x;
            }
            return p;
        }

        friend constexpr auto operator*(Vec<T, N> p, T x) -> Vec<T, N>
        {
            return x * p;
        }

        constexpr auto translated(Vec<T, N> v) const noexcept -> Vec<T, N>
        {
            Vec<T, N> p = this;
            p += v;
            return p;
        }

        struct DefaultHash
        {
            constexpr auto
            operator()(Vec<T, N> const &p) const noexcept -> std::size_t
            {
                constexpr std::size_t dst_bits = 8 * sizeof(std::size_t);
                constexpr std::size_t src_bits = 8 * sizeof(T);
                std::size_t result = 0;
                for (std::size_t i = 0; i < N; i++) {
                    result ^= static_cast<std::size_t>(p.coords[i])
                            << ((i * src_bits) & (dst_bits - 1));
                }
                return result;
            }
        };

    };

    template<typename T, std::size_t N>
    constexpr auto
    manhattan_distance(Vec<T, N> const &p, Vec<T, N> const &q) noexcept -> T
    {
        T accum{0};
        for (std::size_t i = 0; i < N; i++) {
            accum += std::abs(p.coords[i] - q.coords[i]);
        }
        return accum;
    }

    using Vec3 = Vec<int, 3>;

    struct Cube
    {
        Vec3 min{};
        Vec3 max{};

        constexpr auto empty() const noexcept -> bool
        {
            return min == max;
        }

        // Union, but reserved keyword in C++
        void join(Cube const& other)
        {
            for (std::size_t i = 0; i < Vec3::dim(); i++) {
                min.coords[i] = std::min(min.coords[i], other.min.coords[i]);
                max.coords[i] = std::max(max.coords[i], other.max.coords[i]);
            }
        }

        void inter(Cube const& other)
        {
            for (std::size_t i = 0; i < Vec3::dim(); i++) {
                min.coords[i] = std::min(min.coords[i], other.min.coords[i]);
                max.coords[i] = std::min(max.coords[i], other.max.coords[i]);
            }
        }
    };

    struct NanoBot
    {
        Vec3 pos{};
        int radius{0};

        void show() const
        {
            printf("[%d, %d, %d] (r=%d)\n", pos.coords[0], pos.coords[1],
                   pos.coords[2], radius);
        }
    };

    auto parse(std::string_view filename) -> std::vector<NanoBot>
    {
        std::ifstream file(filename.data());
        if (!file.is_open()) {
            throw std::runtime_error("unable to open file");
        }
        std::string line;
        std::vector<NanoBot> result;
        NanoBot bot;
        while (getline(file, line)) {
            if (sscanf(line.data(), " pos=<%d,%d,%d>, r=%d", &bot.pos.coords[0],
                       &bot.pos.coords[1], &bot.pos.coords[2], &bot.radius) !=
                4) {
                throw std::runtime_error("unable to parse line...");
            }
            result.push_back(bot);
            printf("NanoBot (Vec3 %d %d %d) %d,\n", bot.pos.coords[0], bot.pos.coords[1], bot.pos.coords[2], bot.radius);
        }
        return result;
    }

//    auto solve(std::vector<NanoBot> const& v, Cube area, std::size_t idx) -> std::pair<int, Vec3>
//    {
//        if (idx >= v.size()) {
//            // Pick the point in the area closest to (0, 0, 0)
//            // Must be one corner
//            //for ()
//            return {0, {0, 0, 0}};
//        }
//        auto const& el = v[idx];
//        if (not_in_area(area, el)) {
//            return {0, {0, 0, 0}};
//        }
//        auto not_included = solve(v, area, idx + 1);
//    }

    auto part_1(std::vector<NanoBot> const& v) -> int
    {
        auto m = std::max_element(v.begin(), v.end(), [](auto x, auto y) {return x.radius < y.radius; });
        if (m == v.end()) {
            throw std::runtime_error("no max found... empty vec?");
        }
        int count = 0;
        for (auto&& el : v) {
            if (manhattan_distance(m->pos, el.pos) <= m->radius) {
                count++;
            }
        }
        return count;
    }
}

int main(int argc, char **argv)
{
    puts("~~~ Advent of code 2018 -- Day 23 ~~~\n");
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }
//    for (auto &&el : parse(argv[1])) {
//        el.show();
//    }
    printf("Part1: %d\n", part_1(parse(argv[1])));
    return 0;
}