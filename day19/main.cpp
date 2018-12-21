
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <array>
#include <unordered_map>
#include <vector>
#include <fstream>
#include <cassert>
#include <unordered_set>

namespace
{
    using CpuWord = std::int32_t;

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

    auto from_string(std::string const& v) -> Opcode
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
        char src0;
        char src1;
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

        void dump()
        {
            printf("%5s %d %d %d", opcode_str(opcode), src0, src1, dst);
        }
    };

    struct CpuState
    {
        std::array<CpuWord, 6> regs{};
        std::size_t ip{0};

        auto operator==(CpuState &other) const -> bool
        {
            return regs == other.regs;
        }

        constexpr auto eval(Instruction i) -> CpuState &
        {
            auto eval_cond = [](bool x) -> CpuWord { return x?1:0; };
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
            return *this;
        }

        auto ipr() const { return regs[ip]; };

        void dump() const
        {
            printf("[%3d, %3d, %3d, %3d, %3d, %3d]", regs[0], regs[1], regs[2], regs[3], regs[4], regs[5]);
        }
    };

    class Cpu
    {
        std::vector<Instruction> program_;
        CpuState state_;
    public:

        explicit Cpu(std::string_view filename) : program_{}, state_{}
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
            state_.ip = ip;
            while (std::getline(file, line)) {
                opcode.resize(line.size());
                int src0, src1, dst;
                if (sscanf(line.data(), " %s %d %d %d ", opcode.data(), &src0, &src1, &dst) != 4)
                {
                    throw std::runtime_error("unable to parse instruction");
                }
                auto i = Instruction{from_string(std::string(opcode.data())), (char)src0, (char)src1, (char)dst};
                assert(i.is_valid());
                program_.push_back(i);
            }
        }

        void dump() const
        { state_.dump(); }

        auto state() -> CpuState& { return state_; }
        auto state() const -> CpuState const& { return state_; }

        auto ipr() const { return state_.ipr(); }

        template<bool Verbose = false, bool ShowCfg = false>
        auto step() -> bool
        {
            auto ip = state_.ipr();
            if ((ip < 0) || (ip >= (CpuWord)program_.size()))
            {
                return true;
            }
            if (Verbose) {
                printf("ip=%2d ", ip);
                state_.dump();
                program_[ip].dump(); printf(" | ");
            }
            state_.eval(program_[ip]);
            auto ip_new = state_.ipr();
            if (ShowCfg && (ip != ip_new)) {
                if (ip_new != 7) {
                    printf("%d -> %d\n", ip, ip_new);
                    dump();
                    printf("\n");
                }
            }
            if (Verbose) {
                state_.dump();
                puts("");
            }
            state_.regs[state_.ip] += 1;
            return false;
        }
    };

    auto part_1(std::string_view filename)
    {
        puts("# Part 1\n");
        Cpu cpu{filename};
        for (std::size_t i = 0; i < 10 * 10000 * 10000ull; i++) {
            if (cpu.step()) {
                printf("\nCpu halted, final state is: ");
                cpu.dump();
                puts("\n");
                return;
            }
        }
        fprintf(stderr, "max iteration count reached\n");
        exit(1);
    }

    void part_2()
    {
        puts("# Part 2\n");
        puts("This part is hard to automate. The trick is to guess what "
             "the algorithm is doing. Once this is done, observing the "
             "CPU state during the first cycles (with r0 = 1 initially) "
             "almost gives the answer.");
    }
}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT [part2]", argv[0]);
        exit(1);
    }
    puts("~~~ Advent of code 2018 -- Day 19 ~~~\n");
    part_1(argv[1]);
    part_2();
    return 0;
}
