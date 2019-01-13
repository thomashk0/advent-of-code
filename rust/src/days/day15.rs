use std::io;
use std::io::prelude::*;
use std::cmp;
use std::i32;
use std::collections::{HashSet, HashMap};
use pathfinding::directed::dijkstra;

type Point = (i32, i32);

const INITIAL_HP: i32 = 200;
const MOVES: &[Point] = &[(0, -1), (-1, 0), (1, 0), (0, 1)];

fn reading_order((px, py): Point, (qx, qy): Point) -> cmp::Ordering {
    (py, px).cmp(&(qy, qx))
}

fn manhattan_distance(p: Point, q: Point) -> i32 {
    (p.0 - q.0).abs() + (p.1 - q.1).abs()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum UnitRace {
    Goblin,
    Elf,
}

#[derive(Debug, Clone)]
struct Unit {
    pub race: UnitRace,
    pub loc: Point,
    pub hp: i32,
}

impl Unit {
    pub fn new_goblin(loc: Point) -> Self {
        Unit { race: UnitRace::Goblin, loc, hp: INITIAL_HP }
    }

    pub fn new_elf(loc: Point) -> Self {
        Unit { race: UnitRace::Elf, loc, hp: INITIAL_HP }
    }

    pub fn is_enemy_with(&self, other: &Self) -> bool {
        self.race != other.race
    }

    pub fn is_alive(&self) -> bool { self.hp > 0 }

    pub fn next_move(&self, walls: &HashSet<Point>, units: &[Unit]) -> Option<Point> {
        let units_loc: HashSet<Point> = units.iter().map(|u| u.loc).collect();

        let already_in_range =
            units.iter().any(|other| {
                self.is_enemy_with(other)
                    && (manhattan_distance(self.loc, other.loc) == 1)
            });
        if already_in_range {
            return None;
        }
        let adjacent_nodes = |from: Point| {
            MOVES.iter()
                .map(move |dir| (from.0 + dir.0, from.1 + dir.1))
                .filter(|p| !units_loc.contains(&p) && !walls.contains(p))
        };
        let paths =
            dijkstra::dijkstra_all(&self.loc, |&p| {
                adjacent_nodes(p).map(|q| (q, 1))
            });
        let mut targets: Vec<Point> = Vec::with_capacity(1024);
        for enemy in units.iter().filter(|other| self.is_enemy_with(other)) {
            targets.extend(adjacent_nodes(enemy.loc));
        }
        if targets.is_empty() {
            return None;
        }
        targets.sort_by(|x, y| {
            let dx = paths.get(&x).and_then(|p| Some(p.1)).unwrap_or(std::i32::MAX);
            let dy = paths.get(&y).and_then(|p| Some(p.1)).unwrap_or(std::i32::MAX);
            dx.cmp(&dy).then(reading_order(*x, *y))
        });
        let target = targets[0];
        adjacent_nodes(self.loc)
            .filter_map(|from| {
                dijkstra::dijkstra(
                    &from,
                    |&p| adjacent_nodes(p).map(|q| (q, 1)),
                    |&p| p == target)
                    .and_then(|(_, dist)| Some((from, dist)))
            })
            .min_by_key(|x| x.1)
            .and_then(|res| Some(res.0))
    }
}

fn winner(units: &[Unit]) -> Option<UnitRace> {
    let n_goblins = units.iter().filter(|u| u.is_alive() && u.race == UnitRace::Goblin).count();
    let n_elves = units.iter().filter(|u| u.is_alive() && u.race == UnitRace::Elf).count();
    if n_elves > 0 && n_goblins == 0 {
        Some(UnitRace::Elf)
    } else if n_elves == 0 && n_goblins > 0 {
        Some(UnitRace::Goblin)
    } else {
        None
    }
}

#[derive(Debug, Clone)]
struct State {
    walls: HashSet<Point>,
    units: Vec<Unit>,
    elf_attack_power: i32,
}

impl State {
    fn from_stdin(elf_attack_power: i32) -> Self {
        let mut walls = HashSet::new();
        let mut units = Vec::new();
        io::stdin().lock().lines().enumerate().for_each(|(y, line)| {
            line.unwrap().chars().enumerate().for_each(|(x, c)| {
                let loc = (x as i32, y as i32);
                match c {
                    '#' => { walls.insert(loc); }
                    'G' => units.push(Unit::new_goblin(loc)),
                    'E' => units.push(Unit::new_elf(loc)),
                    _ => {}
                }
            });
        });
        State {
            walls,
            units,
            elf_attack_power,
        }
    }

    fn battle_done(&self) -> bool {
        winner(&self.units).is_some()
    }

    fn num_elves(&self) -> usize {
        self.units.iter()
            .filter(|u| u.is_alive() && u.race == UnitRace::Elf)
            .count()
    }

    fn score(&self) -> i32 {
        self.units.iter().map(|u| u.hp).sum()
    }

    fn dims(&self) -> (i32, i32) {
        let xmax = self.walls.iter().map(|p| p.0).max().unwrap();
        let ymax = self.walls.iter().map(|p| p.1).max().unwrap();
        (xmax, ymax)
    }

    fn draw(&self) {
        let units: HashMap<Point, UnitRace> =
            self.units.iter().map(|x| (x.loc, x.race)).collect();
        let (w, h) = self.dims();
        for y in 0..=h {
            for x in 0..=w {
                let c = {
                    if let Some(race) = units.get(&(x, y)) {
                        assert_eq!(self.walls.contains(&(x, y)), false);
                        match race {
                            UnitRace::Goblin => 'G',
                            UnitRace::Elf => 'E'
                        }
                    } else if self.walls.contains(&(x, y)) {
                        '#'
                    } else {
                        '.'
                    }
                };
                print!("{}", c);
            }
            println!();
        }
    }

    fn round(&mut self) -> bool {
        let walls = &self.walls;
        self.units.sort_by(|x, y| reading_order(x.loc, y.loc));
        let units = &mut self.units;
        let mut units_alive: Vec<Unit>;
        for i in 0..units.len() {
            if !units[i].is_alive() {
                continue;
            }
            units_alive = units.iter().filter(|u| u.is_alive()).cloned().collect();
            if winner(&units_alive).is_some() {
                return false;
            }
            if let Some(loc) = units[i].next_move(walls, &units_alive) {
                units[i].loc = loc;
            }
            let u = units[i].clone();
            let target =
                units.iter_mut()
                    .filter(|other| {
                        other.is_alive() && u.is_enemy_with(other) && manhattan_distance(u.loc, other.loc) == 1
                    })
                    .min_by(|x, y| {
                        x.hp.cmp(&y.hp).then(reading_order(x.loc, y.loc))
                    });
            if let Some(t) = target {
                let attack = {
                    if u.race == UnitRace::Elf {
                        self.elf_attack_power
                    } else {
                        3
                    }
                };
                t.hp = cmp::max(0, t.hp - attack);
            }
        }
        units.drain_filter(|x| { !x.is_alive() });
        true
    }
}

fn simulate(mut s: State, debug: bool) -> (i32, i32, State) {
    let mut i = 0;
    while !s.battle_done() {
        i += 1;
        let completed = s.round();
        if debug {
            println!("After {} rounds", i);
            s.draw();
            s.units.iter().for_each(|u| {
                println!("{:?}", u);
            });
        }
        if !completed {
            i -= 1;
            break;
        }
    }
    let sum = s.score();
    (i, sum, s)
}

pub fn run() -> io::Result<()> {
    let s: State = State::from_stdin(3);
    let debug = false;
    if debug {
        println!("Initial state");
        s.draw();
    }
    let (i, sum, _) = simulate(s.clone(), debug);
    println!("Battle ended after {} full rounds", i);
    println!("Part 1: {} ({}x{})", sum * i, sum, i);

    for attack_power in 3..200 {
        let num_elves = s.num_elves();
        let mut s = s.clone();
        s.elf_attack_power = attack_power;
        let (i, sum, s_final) = simulate(s, debug);
        if s_final.num_elves() == num_elves {
            println!("Part 2: {} ({}x{})", sum * i, sum, i);
            break;
        }
    }
    Ok(())
}
