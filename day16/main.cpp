#include <cstdio>
#include <cstdint>
#include <array>
#include <vector>
#include <optional>
#include <bitset>
#include <algorithm>
#include <cassert>
#include <numeric>

namespace
{
    using u8 = std::uint8_t;
    using u32 = std::uint32_t;

    namespace details
    {
        /// Return the value if the set has a single element, otherwise nothing
        template<typename BitSet>
        auto pick_single(BitSet &&s) -> std::optional<std::size_t>
        {
            if (s.count() == 1) {
                for (std::size_t i = 0; i < s.size(); i++) {
                    if (s[i]) {
                        return i;
                    }
                }
            }
            return std::nullopt;
        }
    }

    enum class Opcode : u8
    {
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr
    };

    constexpr auto opcode_str(Opcode opcode) -> char const *
    {
        switch (opcode) {
            case Opcode::addr:
                return "addr";
            case Opcode::addi:
                return "addi";
            case Opcode::mulr:
                return "mulr";
            case Opcode::muli:
                return "muli";
            case Opcode::banr:
                return "banr";
            case Opcode::bani:
                return "bani";
            case Opcode::borr:
                return "borr";
            case Opcode::bori:
                return "bori";
            case Opcode::setr:
                return "setr";
            case Opcode::seti:
                return "seti";
            case Opcode::gtir:
                return "gtir";
            case Opcode::gtri:
                return "gtri";
            case Opcode::gtrr:
                return "gtrr";
            case Opcode::eqir:
                return "eqir";
            case Opcode::eqri:
                return "eqri";
            case Opcode::eqrr:
                return "eqrr";
        }
        return "unknown";
    }

    struct Instruction
    {
        Opcode opcode;
        u8 src0;
        u8 src1;
        u8 dst;

        constexpr auto is_valid() const -> bool
        {
            if (dst >= 4) {
                return false;
            }
            switch (opcode) {
                case Opcode::addr:
                case Opcode::mulr:
                case Opcode::banr:
                case Opcode::borr:
                case Opcode::setr:
                case Opcode::gtrr:
                case Opcode::eqrr:
                    return (src0 <= 3) && (src1 <= 3);
                case Opcode::addi:
                case Opcode::bani:
                case Opcode::bori:
                case Opcode::seti:
                case Opcode::gtri:
                case Opcode::eqri:
                case Opcode::muli:
                    return (src0 <= 3);
                case Opcode::gtir:
                case Opcode::eqir:
                    return (src1 <= 3);
            }
            return true;
        }
    };

    struct CpuState
    {
        std::array<u32, 4> regs{};

        auto operator==(CpuState &other) const -> bool
        {
            return regs == other.regs;
        }

        constexpr auto eval(Instruction i) -> CpuState &
        {
            switch (i.opcode) {
                case Opcode::addr:
                    regs[i.dst] = regs[i.src0] + regs[i.src1];
                    break;
                case Opcode::addi:
                    regs[i.dst] = regs[i.src0] + i.src1;
                    break;
                case Opcode::mulr:
                    regs[i.dst] = regs[i.src0] * regs[i.src1];
                    break;
                case Opcode::muli:
                    regs[i.dst] = regs[i.src0] * i.src1;
                    break;
                case Opcode::banr:
                    regs[i.dst] = regs[i.src0] & regs[i.src1];
                    break;
                case Opcode::bani:
                    regs[i.dst] = regs[i.src0] & i.src1;
                    break;
                case Opcode::borr:
                    regs[i.dst] = regs[i.src0] | regs[i.src1];
                    break;
                case Opcode::bori:
                    regs[i.dst] = regs[i.src0] | i.src1;
                    break;
                case Opcode::setr:
                    regs[i.dst] = regs[i.src0];
                    break;
                case Opcode::seti:
                    regs[i.dst] = i.src0;
                    break;
                case Opcode::gtir:
                    regs[i.dst] = (i.src0 > regs[i.src1]) ? u8{1} : u8{0};
                    break;
                case Opcode::gtri:
                    regs[i.dst] = (regs[i.src0] > i.src1) ? u8{1} : u8{0};
                    break;
                case Opcode::gtrr:
                    regs[i.dst] = (regs[i.src0] > regs[i.src1]) ? u8{1} : u8{0};
                    break;
                case Opcode::eqir:
                    regs[i.dst] = (i.src0 == regs[i.src1]) ? u8{1} : u8{0};
                    break;
                case Opcode::eqri:
                    regs[i.dst] = (regs[i.src0] == i.src1) ? u8{1} : u8{0};
                    break;
                case Opcode::eqrr:
                    regs[i.dst] = (regs[i.src0] == regs[i.src1]) ? u8{1} : u8{
                            0};
                    break;
            }
            return *this;
        }

        void dump() const
        {
            printf("[%u, %u, %u, %u]\n", regs[0], regs[1], regs[2], regs[3]);
        }
    };

    template<typename F>
    void
    foreach_valid_opcode(Instruction inst, CpuState initial, CpuState final,
                         F f)
    {
        for (u8 i = 0; i < 16; i++) {
            CpuState tmp = initial;
            auto opcode = static_cast<Opcode>(i);
            inst.opcode = opcode;
            if (inst.is_valid()) {
                if (tmp.eval(inst) == final) {
                    f(opcode);
                }
            }
        }
    }

    std::optional<CpuState> parse_state(char const *match_str)
    {
        CpuState s{};
        auto n = scanf(match_str, &s.regs[0], &s.regs[1], &s.regs[2],
                       &s.regs[3]);
        if (n != 4) {
            return std::nullopt;
        }
        return s;
    }

    std::optional<Instruction> parse_inst()
    {
        Instruction i{};
        u8 opcode;
        auto n = scanf(" %hhu %hhu %hhu %hhu\n", &opcode, &i.src0, &i.src1,
                       &i.dst);
        if (n != 4) {
            return std::nullopt;
        }
        i.opcode = static_cast<Opcode>(opcode);
        return i;
    }

    template<bool Verbose = true>
    class CollisionCounter
    {
    public:
        CollisionCounter() : buff_{}, collides_{0}
        {
            buff_.reserve(128);
        }

        void process(Instruction inst, CpuState initial, CpuState final)
        {
            buff_.clear();
            foreach_valid_opcode(inst, initial, final, [&](auto x) {
                buff_.push_back(x);
            });
            if (buff_.size() >= 3) {
                collides_ += 1;
            }
            if (Verbose) {
                printf("Found %zu collisions:\n", buff_.size());
                for (auto &&el : buff_) {
                    printf("\t- %u (%s)\n", static_cast<u8>(el),
                           opcode_str(el));
                }
            }
        }

        constexpr auto result() -> std::size_t
        {
            return collides_;
        }

    private:
        std::vector<Opcode> buff_;
        std::size_t collides_;
    };


    class Solver
    {
    public:
        Solver()
        {
            for (auto &&v : values_) {
                v.set();
            }
        }

        void process(Instruction inst, CpuState initial, CpuState final)
        {
            std::bitset<16> tmp{};
            foreach_valid_opcode(inst, initial, final, [&](auto x) {
                tmp.set(static_cast<std::size_t>(x));
            });
            auto id = static_cast<std::size_t>(inst.opcode);
            values_[id] &= tmp;
        }

        auto solve() -> bool
        {
            std::size_t num_found = 0;
            while (true) {
                bool fixed_point = true;
                for (std::size_t i = 0; i < values_.size(); i++) {
                    auto b = details::pick_single(values_[i]);
                    if (b.has_value()) {
                        num_found++;
                        fixed_point = false;
                        translation_[i] = (u8) *b;
                        for (auto &&row : values_) {
                            row.set(*b, false);
                        }
                    }
                }
                if (fixed_point) {
                    break;
                }
            }
            return num_found == values_.size();
        }

        auto result() const -> std::array<u8, 16> const &
        {
            return translation_;
        }

    private:
        std::array<std::bitset<16>, 16> values_{};
        std::array<u8, 16> translation_{};
    };
}

int main()
{
    puts("~~~ Advent of code 2018 -- Day 16 ~~~\n\n");

    puts("# part 1\n");
    CollisionCounter<false> counter;
    Solver solver;
    while (true) {
        auto initial = parse_state(" Before: [%hhu, %hhu, %hhu, %hhu]\n");
        if (!initial.has_value()) {
            break;
        }

        auto inst = parse_inst();
        if (!inst.has_value()) {
            fprintf(stderr, "%s:%d: parsing failed.\n", __FILE__, __LINE__);
            exit(1);
        }

        auto final = parse_state(" After: [%hhu, %hhu, %hhu, %hhu]\n");
        if (!final.has_value()) {
            fprintf(stderr, "%s:%d: parsing failed.\n", __FILE__, __LINE__);
            exit(1);
        }
        counter.process(*inst, *initial, *final);
        solver.process(*inst, *initial, *final);
    }

    printf("Number of >=3 collisions: %lu\n\n", counter.result());

    puts("# part 2\n");

    if (!solver.solve()) {
        fprintf(stderr, "%s:%d: unable to recover opcode mapping.\n",
                __FILE__, __LINE__);
        exit(1);
    }

    puts("Opcode mapping found:");
    std::size_t i = 0;
    for (auto &&x : solver.result()) {
        printf("\t- %zu -> %s\n", i++, opcode_str(static_cast<Opcode>(x)));
    }

    CpuState s{};
    while (true) {
        auto inst = parse_inst();
        if (!inst.has_value()) {
            break;
        }
        inst->opcode = static_cast<Opcode>(solver.result()[static_cast<std::size_t>(inst->opcode)]);
        s.eval(*inst);
    }
    printf("Evaluation result: %lu\n", static_cast<std::size_t>(s.regs[0]));

    return 0;
}
