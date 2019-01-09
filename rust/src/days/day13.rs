use std::io;
use std::io::prelude::*;
use std::collections::{HashSet, HashMap};
use std::cmp;
use std::iter;

type Point = (i32, i32);
type Vector = (i32, i32);

#[derive(Debug, Clone, Eq, PartialEq)]
enum Direction {
    Left,
    Straight,
    Right,
}

fn apply_choice(c: Direction, v: Vector) -> Vector {
    match c {
        Direction::Left => (v.1, -v.0),
        Direction::Straight => v,
        Direction::Right => (-v.1, v.0)
    }
}

#[derive(Debug, Eq, PartialEq, Clone)]
struct Cart
{
    loc: Point,
    dir: Vector,
    next_choice: Direction
}

impl PartialOrd for Cart {
    fn partial_cmp(&self, other: &Self) -> Option<cmp::Ordering> {
        Some(self.cmp(&other))
    }
}

impl Ord for Cart {
    fn cmp(&self, other: &Self) -> cmp::Ordering {
        self.loc.0.cmp(&other.loc.0)
            .then(self.loc.1.cmp(&other.loc.1))
            .then(self.dir.cmp(&other.dir))
    }
}

impl Cart {
    fn update(&mut self, val: u8) {
        self.dir = match val {
            b'\\' => (self.dir.1, self.dir.0),
            b'/' => (-self.dir.1, -self.dir.0),
            b'+' => {
                let choice = self.next_choice.clone();
                match choice {
                    Direction::Left => self.next_choice = Direction::Straight,
                    Direction::Straight => self.next_choice = Direction::Right,
                    Direction::Right => self.next_choice = Direction::Left
                }
                apply_choice(choice, self.dir)
            }
            b'-' | b'|' => self.dir,
            _ => {
                panic!("out of rails !!!");
            }
        };
        self.loc.0 += self.dir.0;
        self.loc.1 += self.dir.1;
    }
}

struct Dense2dMap
{
    w: i32,
    h: i32,
    data: Vec<u8>,
}

impl Dense2dMap {
    pub fn new(w: i32, h: i32, default: u8) -> Self {
        Dense2dMap {
            w: w,
            h: h,
            data: iter::repeat(default).take((w * h) as usize).collect(),
        }
    }

    pub fn at(&self, (x, y): (i32, i32)) -> Option<u8> {
        if x >= 0 && x < self.w && y >= 0 && y < self.h {
            Some(self.data[(y * self.w + x) as usize])
        } else {
            None
        }
    }

    pub fn dims(&self) -> (i32, i32) {
        (self.w, self.h)
    }
}


struct Map
{
    map: Dense2dMap,
    carts: Vec<Cart>,
    dead: HashSet<usize>,
    reserved: HashMap<Point, (usize, Cart)>,
}

fn parse_cart(c: u8) -> Option<Vector> {
    match c {
        b'^' => Some((0, -1)),
        b'>' => Some((1, 0)),
        b'<' => Some((-1, 0)),
        b'v' => Some((0, 1)),
        _ => None
    }
}

fn replace_cart(c: u8) -> u8 {
    match c {
        b'^' | b'v' => b'|',
        b'>' | b'<' => b'-',
        _ => c
    }
}

impl Map {
    pub fn from_string(lines: &Vec<String>) -> Self {
        let h = lines.len();
        let w = lines.iter().map(|s| s.len()).max().unwrap();
        let mut map = Dense2dMap::new(w as i32, h as i32, b' ');
        let mut carts: Vec<Cart> = Vec::with_capacity(4);
        for (y, l) in lines.iter().enumerate() {
            for (x, &c) in l.as_bytes().iter().enumerate() {
                map.data[y * w + x] = {
                    if let Some(dir) = parse_cart(c) {
                        carts.push(Cart { loc: (x as i32, y as i32), dir: dir, next_choice: Direction::Left });
                        replace_cart(c)
                    } else {
                        c
                    }
                }
            }
        }
        carts.sort();
        Map {
            map,
            carts,
            dead: HashSet::new(),
            reserved: HashMap::new(),
        }
    }

    pub fn draw(&self) {
        let (w, h) = self.map.dims();
        for y in 0..h {
            for x in 0..w {
                if self.reserved.contains_key(&(x, y)) {
                    print!("*");
                } else {
                    print!("{}", self.map.data[(w * y + x) as usize] as char);
                }
            }
            println!();
        }
    }

    pub fn step(&mut self) -> Vec<Point> {
        self.reserved.clear();
        self.dead.clear();
        let map = &self.map;
        let carts = &mut self.carts;
        carts.sort();

        let mut crashes = Vec::new();
        for (i, c) in carts.iter().enumerate() {
            self.reserved.insert(c.loc, (i, c.clone()));
        }

        for (i, c) in carts.iter().enumerate() {
            if self.dead.contains(&i) {
                continue;
            }
            let c_new = { let mut tmp = c.clone(); tmp.update(map.at(c.loc).unwrap_or(b' ')); tmp };
            if let Some((_, (id, _))) = self.reserved.remove_entry(&c_new.loc) {
                crashes.push(c_new.loc);
                self.dead.insert(i);
                self.dead.insert(id);
            } else {
                self.reserved.insert(c_new.loc, (i, c_new));
            }
            self.reserved.remove(&c.loc);
        }

        carts.clear();
        for (_, (_, cart)) in &self.reserved {
            carts.push(cart.clone());
        }
        crashes
    }
}

pub fn run() -> io::Result<()> {
    let lines: Vec<String> = io::stdin().lock().lines().map(|l| {
        l.unwrap().trim_end().to_string()
    }).collect();

    let mut m = Map::from_string(&lines);
    let mut part_1_solved = false;
    println!("State at t=0");
    m.draw();
    for _step in 1..=200000 {
        let v = m.step();

        // m.draw();
        if !v.is_empty() && !part_1_solved {

            let (x, y) = v[0];
            println!("Part 1: {},{}", x, y);
            part_1_solved = true;
        }
        if m.carts.len() == 0 {
            println!("WARNING: all cart crashed... leaving");
            break;
        }
        if m.carts.len() == 1 {
            let (x, y) = m.carts[0].loc;
            println!("Part 2: {},{}", x, y);
            break;
        }
    }
    Ok(())
}