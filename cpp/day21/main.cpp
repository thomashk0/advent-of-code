// NOTE: the problem is solved through bruteforcing there.
//       there might be a better way to solve this...
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <array>
#include <unordered_map>
#include <vector>
#include <fstream>
#include <cassert>
#include <unordered_set>
#include <set>
#include <sstream>

#include <aoc/utils.h>
#include <aoc/colors.h>
#include <iostream>
#include <algorithm>

namespace
{
    using CpuWord = std::int64_t;

    enum class Opcode : char
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

    static const std::unordered_map<std::string, Opcode> opcode_map = {
            {"addr", Opcode::addr},
            {"addi", Opcode::addi},
            {"mulr", Opcode::mulr},
            {"muli", Opcode::muli},
            {"banr", Opcode::banr},
            {"bani", Opcode::bani},
            {"borr", Opcode::borr},
            {"bori", Opcode::bori},
            {"setr", Opcode::setr},
            {"seti", Opcode::seti},
            {"gtir", Opcode::gtir},
            {"gtri", Opcode::gtri},
            {"gtrr", Opcode::gtrr},
            {"eqir", Opcode::eqir},
            {"eqri", Opcode::eqri},
            {"eqrr", Opcode::eqrr}
    };

    auto from_string(std::string const &v) -> Opcode
    {
        auto it = opcode_map.find(v);
        if (it == opcode_map.end()) {
            throw std::invalid_argument("invalid opcode");
        }
        return it->second;
    }

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
        return "<?>";
    }

    struct Instruction
    {
        Opcode opcode;
        int src0;
        int src1;
        char dst;

        constexpr auto is_valid() const -> bool
        {
            if (dst >= 6) {
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
                    return (src0 <= 5) && (src1 <= 5);
                case Opcode::addi:
                case Opcode::bani:
                case Opcode::bori:
                case Opcode::gtri:
                case Opcode::eqri:
                case Opcode::muli:
                    return (src0 <= 5);
                case Opcode::gtir:
                case Opcode::eqir:
                    return (src1 <= 5);
                case Opcode::seti:
                    return true;
            }
            return true;
        }

        void dump() const
        {
            printf("%5s %d %d %d", opcode_str(opcode), src0, src1, dst);
        }

        auto show() const -> std::string
        {
            std::stringstream s;
            s << opcode_str(opcode) << " " << src0 << " " << src1 << " "
              << (int) dst;
            return s.str();
        }

        auto disasm() const -> std::string
        {
            std::stringstream s;
            auto reg = [](int reg) -> std::string_view {
                switch (reg) {
                    case 0:
                        return FBLU("R0");
                    case 1:
                        return FCYN("R1");
                    case 2:
                        return FGRN("R2");
                    case 3:
                        return FMAG("R3");
                    case 4:
                        return FRED("R4");
                    case 5:
                        return FYEL("R5");
                    default:
                        return "??";
                }
            };

            auto rr_op = [&](std::string_view op) {
                s << reg(dst) << " <- " << reg(src0) << " " << op << " "
                  << reg(src1);
            };

            auto ri_op = [&](std::string_view op) {
                s << reg(dst) << " <- " << reg(src0) << " " << op << " "
                  << src1;
            };

            auto ir_op = [&](std::string_view op) {
                s << reg(dst) << " <- " << src0 << " " << op << " "
                  << reg(src1);
            };

            switch (opcode) {
                case Opcode::addr:
                    rr_op("+");
                    break;
                case Opcode::addi:
                    ri_op("+");
                    break;
                case Opcode::mulr:
                    rr_op("*");
                    break;
                case Opcode::muli:
                    ri_op("*");
                    break;
                case Opcode::banr:
                    rr_op("&");
                    break;
                case Opcode::bani:
                    ri_op("&");
                    break;
                case Opcode::borr:
                    rr_op("|");
                    break;
                case Opcode::bori:
                    ri_op("|");
                    break;
                case Opcode::setr:
                    s << reg(dst) << " <- " << reg(src0);
                    break;
                case Opcode::seti:
                    s << reg(dst) << " <- " << src0;
                    break;
                case Opcode::gtir:
                    ir_op(">");
                    break;
                case Opcode::gtri:
                    ri_op(">");
                    break;
                case Opcode::gtrr:
                    rr_op(">");
                    break;
                case Opcode::eqir:
                    ir_op("==");
                    break;
                case Opcode::eqri:
                    ri_op("==");
                    break;
                case Opcode::eqrr:
                    rr_op("==");
                    break;
            }
            return s.str();
        }
    };

    struct CpuState
    {
        std::array<CpuWord, 6> regs{};
        CpuWord cycle{0};

        auto operator==(CpuState &other) const -> bool
        {
            return (regs == other.regs) && (cycle == other.cycle);
        }

        constexpr auto eval(Instruction i) -> CpuState &
        {
            auto eval_cond = [](bool x) -> CpuWord { return x ? 1 : 0; };
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
                    regs[i.dst] = eval_cond(i.src0 > regs[i.src1]);
                    break;
                case Opcode::gtri:
                    regs[i.dst] = eval_cond(regs[i.src0] > i.src1);
                    break;
                case Opcode::gtrr:
                    regs[i.dst] = eval_cond(regs[i.src0] > regs[i.src1]);
                    break;
                case Opcode::eqir:
                    regs[i.dst] = eval_cond(i.src0 == regs[i.src1]);
                    break;
                case Opcode::eqri:
                    regs[i.dst] = eval_cond(regs[i.src0] == i.src1);
                    break;
                case Opcode::eqrr:
                    regs[i.dst] = eval_cond(regs[i.src0] == regs[i.src1]);
                    break;
            }
            cycle++;
            return *this;
        }

        void dump() const
        {
            printf("[%3lu, %3lu, %3lu, %3lu, %3lu, %3lu]", regs[0], regs[1],
                   regs[2], regs[3], regs[4], regs[5]);
        }
    };

    class Cpu
    {
        std::vector<Instruction> program_;
        std::unordered_map<std::size_t, CpuState> info_;
        std::unordered_set<std::pair<CpuWord, CpuWord>, aoc::PairHash<CpuWord>> branches_;
        CpuState state_;
        std::size_t ip_;
        bool halted_;
    public:

        explicit Cpu(std::string_view filename)
                : program_{}, info_{}, branches_{}, state_{}, ip_{0},
                  halted_{false}
        {
            program_.reserve(1024);
            std::ifstream file(filename.data());
            if (!file.is_open()) {
                throw std::runtime_error("unable to open file");
            }

            std::string line, opcode;
            if (!std::getline(file, line)) {
                throw std::runtime_error("parsing failed");
            }
            int ip;
            if (sscanf(line.data(), " #ip %d", &ip) != 1) {
                throw std::runtime_error("unable to parse instruction pointer");
            };
            ip_ = static_cast<std::size_t>(ip);
            while (std::getline(file, line)) {
                opcode.resize(line.size());
                int src0, src1, dst;
                if (sscanf(line.data(), " %s %d %d %d ", opcode.data(), &src0,
                           &src1, &dst) != 4) {
                    throw std::runtime_error("unable to parse instruction");
                }
                auto i = Instruction{from_string(std::string(opcode.data())),
                                     src0, src1, (char) dst};
                // assert(i.is_valid());
                program_.push_back(i);
            }
        }

        auto branch_to(CpuWord target) const -> std::vector<CpuWord>
        {
            std::vector<CpuWord> result{};
            auto it = branches_.begin();
            while (true) {
                it = std::find_if(it, branches_.end(),
                                  [&](auto &&x) { return x.second == target; });
                if (it == branches_.end()) {
                    break;
                }
                result.push_back(it->first);
                ++it;
            }
            return result;
        }

        void disasm() const
        {
            int idx = 0;
            std::vector<CpuWord> v{};
            for (auto &&el: program_) {
                v.clear();
                v = branch_to(idx);
                if (!v.empty()) {
                    printf("\n\t");
                    for (auto &&src : v) {
                        printf("%lu ", src);
                    }
                    printf("\n~~~~~~\n");
                }
                if (idx == ipr()) {
                    printf("+> ");
                }
                printf("%-3d %-20s | %s\t\t", idx, el.show().data(),
                       el.disasm().data());
                auto it = info_.find(idx);
                if (it != info_.end()) {
                    it->second.dump();
                }
                printf("\n");
                idx++;
            }
        }

        void reset()
        {
            state_ = CpuState{};
            halted_ = false;
        }

        void dump() const
        {
            state_.dump();
        }

        auto halted() const noexcept -> bool
        {
            return halted_;
        }

        auto state() -> CpuState &
        {
            return state_;
        }

        auto state() const -> CpuState const &
        {
            return state_;
        }

        constexpr auto ipr() const -> CpuWord const &
        {
            return state_.regs[ip_];
        }

        constexpr auto ipr() -> CpuWord &
        {
            return state_.regs[ip_];
        }

        constexpr auto cycle() const noexcept
        {
            return state_.cycle;
        }

        template<bool LogState = false>
        auto step() -> bool
        {
            CpuWord ip = ipr();
            if ((ip < 0) || (ip >= (CpuWord) program_.size())) {
                halted_ = true;
                return true;
            }

            state_.eval(program_[ip]);
            if (LogState) {
                info_[ip] = state_;
                if (ipr() != ip) {
                    branches_.insert({ip, ipr() + 1});
                }
            }
            ipr() += 1;
            return false;
        }
    };

    auto part_1(std::string_view filename)
    {
        puts("# Part 1\n");
        Cpu cpu{filename};
        constexpr bool debug = false;
        std::size_t hit{0};
        std::unordered_map<CpuWord, CpuWord> values;
        while (!cpu.halted()) {
            cpu.step<false>();
            if (cpu.ipr() == 28) {
                CpuWord r1 = cpu.state().regs[1];
                if (hit == 0) {
                    printf("Part1: %lu\n", r1);
                }
                if (values.find(r1) == values.end()) {
                    values[r1] = cpu.cycle();
                }
                if (cpu.cycle() % 1024 == 0) {
                    printf("cycle#%lu found %zu distinct values\n", cpu.cycle(),
                           values.size());
                }
                if (cpu.cycle() >= 3097486336ll) {
                    auto it = std::max_element(values.begin(), values.end(),
                                               [](auto x, auto y) {
                                                   return x.second < y.second;
                                               });
                    for (auto&& el : values) {
                        if (el.second == it->second) {
                            printf("Part2: %lu (stop at %lu cycles)\n", it->first,
                                   it->second);
                        }
                    }

                    break;
                }
                hit++;
            }
            if (debug) {
                cpu.disasm();
                printf("\n");
                std::cin.get();
            }
        }
    }

}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }
    puts("~~~ Advent of code 2018 -- Day 21 ~~~\n");
    part_1(argv[1]);
    return 0;
}


