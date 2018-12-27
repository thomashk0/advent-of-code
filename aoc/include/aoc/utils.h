#pragma once

#include <algorithm>
#include <vector>
#include <unordered_map>

namespace aoc
{
    template<typename T, std::size_t N>
    struct StaticVector
    {
        std::array<T, N> storage{};
        std::size_t size{0};
        static constexpr std::size_t capacity = N;

        explicit constexpr StaticVector() : storage{}, size{0}
        {
        }

        constexpr auto push_back(T el)
        {
            if (size > capacity) {
                throw std::out_of_range("");
            }
            storage[size] = el;
            size += 1;
        }

        using value_type = T;
        using iterator = T *;

        constexpr auto begin() noexcept
        {
            return storage.data();
        }

        constexpr auto end() noexcept
        {
            return storage.data() + size;
        }

        using const_iterator = T const *;

        auto begin() const noexcept
        {
            return storage.data();
        }

        auto end() const noexcept
        {
            return storage.data() + size;
        }
    };

    template<typename T>
    struct Vec2
    {
        using Scalar = T;

        T x{};
        T y{};

        constexpr auto operator==(Vec2<T> const &other) const noexcept -> bool
        {
            return (x == other.x) && (y == other.y);
        }

        constexpr auto operator+=(Vec2<T> const &other) noexcept -> Vec2<T> &
        {
            x += other.x;
            y += other.y;
            return *this;
        }

        friend constexpr auto operator+(Vec2<T> p, Vec2<T> q) -> Vec2<T>
        {
            p += q;
            return p;
        }

        friend constexpr auto operator*(T x, Vec2<T> p) -> Vec2<T>
        {
            p.x *= x;
            p.y *= x;
            return p;
        }

        friend constexpr auto operator*(Vec2<T> p, T x) -> Vec2<T>
        {
            return x * p;
        }

        constexpr auto shifted(Vec2<T> v) const noexcept -> Vec2<T>
        {
            return Vec2{x + v.x, y + v.y};
        }

        constexpr auto above() const noexcept -> Vec2<T>
        {
            return shifted({0, -1});
        }

        constexpr auto below() const noexcept -> Vec2<T>
        {
            return shifted({0, 1});
        }

        constexpr auto left() const noexcept -> Vec2<T>
        {
            return shifted({-1, 0});
        }

        constexpr auto right() const noexcept -> Vec2<T>
        {
            return shifted({1, 0});
        }

        struct DefaultHash
        {
            constexpr auto
            operator()(Vec2<T> const &p) const noexcept -> std::size_t
            {
                static_assert(sizeof(T) * 8 <= 32,
                              "scalar type is too big for using this hash policy");
                return static_cast<std::size_t>(p.x) << 32 |
                       static_cast<std::size_t>(p.y);
            }
        };
    };


    template<typename T>
    struct PairHash
    {
        constexpr auto
        operator()(std::pair<T, T> const &p) const noexcept -> std::size_t
        {
            return static_cast<std::size_t>(p.first) ^
                   static_cast<std::size_t>(p.second);
        }
    };

    template<typename Scalar, typename Value>
    struct Dense2dMap
    {
        Scalar xmin{};
        Scalar xmax{};
        Scalar ymin{};
        Scalar ymax{};
        Scalar w{};
        Scalar h{};
        std::vector<Value> data{};
    };

    template<typename Scalar, typename Value>
    struct Sparse2dMap
    {
        using Point = Vec2<Scalar>;

        std::unordered_map<Point, Value, typename Point::DefaultHash> data;

        auto insert(Point p, Value v)
        {
            data[p] = v;
        }

        auto remove(Point p)
        {
            data.erase(p);
        }

        auto freeze(Value fill) const -> Dense2dMap<Scalar, Value>
        {
            Dense2dMap<Scalar, Value> result{};
            auto[xmin, xmax] = xrange();
            Scalar w = xmax - xmin + 1;
            auto[ymin, ymax] = yrange();
            Scalar h = ymax - ymin + 1;
            result.xmin = xmin;
            result.xmax = xmax;
            result.ymin = ymin;
            result.ymax = ymax;
            result.w = w;
            result.h = h;
            result.data.resize(w * h, fill);
            for (auto &&el : data) {
                result.data[(el.first.y - ymin) * w +
                            (el.first.x - xmin)] = el.second;
            }
            return result;
        }

        auto operator[](Point p) -> Value &
        {
            return data[p];
        }

        auto xrange() const -> std::pair<Scalar, Scalar>
        {
            auto it = std::minmax_element(data.begin(), data.end(),
                                          [](auto p, auto q) {
                                              return p.first.x < q.first.x;
                                          });
            return {(it.first)->first.x, (it.second)->first.x};
        }

        auto yrange() const -> std::pair<Scalar, Scalar>
        {
            auto it = std::minmax_element(data.begin(), data.end(),
                                          [](auto p, auto q) {
                                              return p.first.y < q.first.y;
                                          });
            return {(it.first)->first.y, (it.second)->first.y};
        }
    };

    /// \name Helper for describing std::variant visitor.
    /// More info at https://en.cppreference.com/w/cpp/utility/variant/visit
    /// \{
    template<class... Ts>
    struct overloaded : Ts ...
    {
        using Ts::operator()...;
    };
    template<class... Ts> overloaded(Ts...) -> overloaded<Ts...>;
    /// \}
}