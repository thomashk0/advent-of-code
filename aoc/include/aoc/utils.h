#pragma once

namespace aoc
{
    template<typename T, std::size_t N>
    struct StaticVector
    {
        std::array<T, N> storage{};
        std::size_t size{0};
        static constexpr std::size_t capacity = N;

        explicit constexpr StaticVector() : storage{}, size{0} {}

        constexpr auto push_back(T el)
        {
            if (size > capacity) {
                throw std::out_of_range("");
            }
            storage[size] = el;
            size += 1;
        }

        using value_type = T;
        using iterator = T*;
        constexpr auto begin() noexcept {return storage.data();}
        constexpr auto end() noexcept {return storage.data() + size;}

        using const_iterator = T const*;
        auto begin() const noexcept {return storage.data();}
        auto end() const  noexcept {return storage.data() + size;}
    };
}