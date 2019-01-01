#include <string>
#include <vector>
#include <cstdio>
#include <stdexcept>
#include <fstream>
#include <algorithm>
#include <unordered_set>
#include <unordered_map>
#include <numeric>

namespace
{
    using Scalar = long;

    struct Attribute
    {
        enum class Type : char
        {
            weak_to,
            immune_to
        };
        Type type;
        std::string str;
    };

    struct Group
    {
        long unit_life{};
        long n_units{};
        long damage{};
        long initiative{};
        std::string attack_type{};
        std::unordered_set<std::string> weak_to{};
        std::unordered_set<std::string> immune_to{};
        bool immune_army{false};

        constexpr auto effective_power() const noexcept -> long
        {
            return n_units * damage;
        }

        constexpr auto is_dead() const noexcept -> bool
        {
            return n_units == 0;
        }

        void show() const
        {
            if (immune_army) {
                printf("immune: ");
            } else {
                printf("infection: ");
            }
            printf("%li units each with %li hit points ", n_units, unit_life);
            bool has_attrs = !weak_to.empty() || !immune_to.empty();
            if (has_attrs) { printf("("); }
            if (!weak_to.empty()) {
                printf("weak to ");
                for (auto &&s : weak_to) {
                    printf("%s, ", s.data());
                }
                printf(";");
            }
            if (!immune_to.empty()) {
                printf("immune to ");
                for (auto &&s : immune_to) {
                    printf("%s, ", s.data());
                }
            }
            if (has_attrs) { printf(") "); }
            printf("with an attack that does %li %s damage at initiative %li\n",
                   damage, attack_type.data(), initiative);
        }
    };

    auto damage(Group const &attacker, Group const &defender) -> long
    {
        auto power = attacker.effective_power();
        if (defender.immune_to.find(attacker.attack_type) !=
            defender.immune_to.end()) {
            return 0;
        } else if (defender.weak_to.find(attacker.attack_type) !=
                   defender.weak_to.end()) {
            return 2 * power;
        }
        return power;
    }

    struct Battle
    {
        std::vector<Group> all;
    };


    struct Simulation
    {
        Battle b;

        auto add_boost(long value)
        {
            for (auto&& el : b.all) {
                if (el.immune_army) {
                    el.damage += value;
                }
            }
        }

        auto result() const -> long
        {
            return std::accumulate(b.all.begin(), b.all.end(), 0, [](auto acc, auto v) { return acc + v.n_units; });
        }

        auto immune_left() const -> long
        {
            return std::count_if(b.all.begin(), b.all.end(), [](auto& v) {
                return v.immune_army && !v.is_dead();
            });
        }

        auto infection_left() const -> long
        {
            return std::count_if(b.all.begin(), b.all.end(), [](auto& v) {
                return !v.immune_army && !v.is_dead();
            });
        }

        auto step() -> bool
        {
            std::vector<Group *> living{};
            std::unordered_map<Group *, Group*> target{};
            std::unordered_set<Group *> defending{};
            auto is_defending = [&](Group *g) -> bool {
                return defending.find(g) != defending.end();
            };
            living.reserve(32);
            for (Group& g : b.all) {
                if (!g.is_dead()) {
                    living.push_back(&g);
                }
            }
            std::sort(living.begin(), living.end(),
                      [](Group *ga, Group *gb) {
                          if (ga->effective_power() == gb->effective_power()) {
                              return ga->initiative > gb->initiative;
                          }
                          return ga->effective_power() > gb->effective_power();
                      });

            std::vector<Group *> best;
            best.reserve(living.size());
            for (auto el : living) {
                best.clear();
                std::copy_if(living.begin(), living.end(),
                             std::back_inserter(best), [&](auto v) {
                            return (v != el) && !is_defending(v) &&
                                   (damage(*el, *v) > 0) &&
                                   (el->immune_army == !v->immune_army);
                        });
                if (best.empty()) {
                    continue;
                }
                std::sort(best.begin(), best.end(),
                          [&](Group *ga, Group *gb) {
                              auto da = damage(*el, *ga);
                              auto db = damage(*el, *gb);
                              if (da == db) {
                                  if (ga->effective_power() ==
                                      gb->effective_power()) {
                                      return ga->initiative > gb->initiative;
                                  }
                                  return ga->effective_power() >
                                         gb->effective_power();
                              }
                              return da > db;
                          });
                target[el] = best[0];
                defending.insert(best[0]);
            }
            std::sort(living.begin(), living.end(), [](auto ga, auto gb) {
                return ga->initiative > gb->initiative;
            });
            for (auto el : living) {
                if (!el->is_dead()) {
                    auto it = target.find(el);
                    if (it != target.end()) {
                        Group* defender = it->second;
                        auto p = damage(*el, *defender);
                        defender->n_units -= (p / defender->unit_life);
                        defender->n_units = std::max(0l, defender->n_units);
//                        printf("[\n");
//                        el->show();
//                        printf("--> %li damage --> \n", p);
//                        defender->show();
//                        printf("]\n");
                    }
                }
            }
            return (immune_left() == 0) || (infection_left() == 0);
        }
    };

    auto parse_attr(std::string_view v, Group &g)
    {
        std::string buff{};
        auto it = v.begin(), it_prev = v.begin();
        auto next_until = [&](auto f) -> void {
            if (it == v.end()) {
                throw std::runtime_error("unexpected end of input");
            }
            it_prev = it;
            it = std::find_if(it, v.end(), f);
            buff = std::string(it_prev, it);
        };
        auto next_word = [&]() -> void {
            next_until([](char c) { return c == ' '; });
        };
        auto next_attr = [&]() -> void {
            next_until([](char c) { return (c == ',') || (c == ';'); });
        };

        while (it != v.end()) {
            Attribute::Type t;
            next_word();
            ++it;
            if (buff == "weak") {
                t = Attribute::Type::weak_to;
            } else if (buff == "immune") {
                t = Attribute::Type::immune_to;
            }
            next_word();
            ++it;
            if (buff != "to") { throw std::runtime_error("parsing failed"); }

            while (true) {
                next_attr();
                if (t == Attribute::Type::weak_to) {
                    g.weak_to.insert(buff);
                } else {
                    g.immune_to.insert(buff);
                }
                if (it == v.end()) {
                    break;
                }
                if (*it == ';') {
                    it += 2;
                    break;
                }
                it += 2;
            }
        }
    }

    auto parse(std::string_view filename) -> Battle
    {
        std::ifstream file(filename.data());
        if (!file.is_open()) {
            throw std::runtime_error("unable to open file");
        }

        Battle result{};
        std::string line;
        char attrs[256], damage[128];

        auto parse_group = [&](std::vector<Group> &v, bool in_immune) {
            while (std::getline(file, line) && !line.empty()) {
                Group g;
                g.immune_army = in_immune;
                attrs[0] = '\0';
                auto n = sscanf(line.data(),
                                "%li units each with %li hit points (%128[A-Za-z,; ]) with an attack that does %li %64s damage at initiative %li\n",
                                &g.n_units, &g.unit_life, attrs, &g.damage,
                                damage,
                                &g.initiative);
                g.attack_type = damage;
                if (n == 6) {
                    parse_attr(attrs, g);
                } else {
                    n = sscanf(line.data(),
                               "%li units each with %li hit points with an attack that does %li %64s damage at initiative %li\n",
                               &g.n_units, &g.unit_life, &g.damage, damage,
                               &g.initiative);
                    g.attack_type = damage;
                    if (n != 5) {
                        throw std::runtime_error("parsing failed");
                    }
                }
                v.push_back(g);
            }
        };

        if (std::getline(file, line) && line != "Immune System:") {
            throw std::runtime_error("parsing failed");
        }
        parse_group(result.all, true);

        if (std::getline(file, line) && line != "Infection:") {
            throw std::runtime_error("parsing failed");
        }
        parse_group(result.all, false);

        return result;
    }

    void part_1(std::string_view filename)
    {
        auto battle = parse(filename);

        Simulation sim{battle};
        std::size_t step{0};
        while (true) {
            if (sim.step()) {
                break;
            }
            step++;
        }
        printf("Part 1: %li\n", sim.result());
    }

    void part_2(std::string_view filename)
    {
        auto battle = parse(filename);
        long boost = 1;
        Simulation sim{battle};

        while (true) {
            sim.b = battle;
            sim.add_boost(boost);
            if ((boost % 10) == 0) {
                printf("boost : %li\n", boost);
            }
            for (std::size_t i = 0; i < 100000; i++) {
                if(sim.step()) {
                    break;
                }
            }
            if (sim.immune_left() > 0 && sim.infection_left() == 0) {
                break;
            }
            boost++;
        }
        printf("stopped at boost=%li\n", boost);
        printf("Part 2: %li\n", sim.result());
    }
}

int main(int argc, char **argv)
{
    if (argc <= 1) {
        fprintf(stderr, "USAGE: %s INPUT", argv[0]);
        exit(1);
    }
    part_1(argv[1]);
    part_2(argv[1]);
    return 0;
}