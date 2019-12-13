use crate::intcode::{load_tape, HaltCause, IntCpu};
use std::collections::HashMap;
use std::io;

type Vec2 = (i64, i64);

fn rotr90(p: Vec2) -> Vec2 {
    (p.1, -p.0)
}

fn rotl90(p: Vec2) -> Vec2 {
    (-p.1, p.0)
}

fn vec_add(p: Vec2, q: Vec2) -> Vec2 {
    (p.0 + q.0, p.1 + q.1)
}

pub fn limits(world: &HashMap<Vec2, i8>) -> (Vec2, Vec2) {
    let coords: Vec<Vec2> = world.iter().map(|(coords, _)| *coords).collect();
    assert!(coords.len() == world.len());
    let xmin = coords.iter().map(|p| p.0).min().unwrap();
    let xmax = coords.iter().map(|p| p.0).max().unwrap();
    let ymin = coords.iter().map(|p| p.1).min().unwrap();
    let ymax = coords.iter().map(|p| p.1).max().unwrap();
    ((xmin, xmax), (ymin, ymax))
}

pub fn draw(world: &HashMap<Vec2, i8>) {
    let ((xmin, xmax), (ymin, ymax)) = limits(world);
    for y in (ymin..=ymax).rev() {
        for x in xmin..=xmax {
            let c = world.get(&(x, y)).cloned().unwrap_or(0);
            let tile = if c == 1 { "#" } else { " " };
            print!("{}", tile);
        }
        println!();
    }
}

struct Robot {
    pub brain: IntCpu,
    pub loc: Vec2,
    pub dir: Vec2,
}

impl Robot {
    pub fn new() -> Self {
        Robot {
            brain: IntCpu::new(),
            loc: (0, 0),
            dir: (0, 1),
        }
    }

    pub fn step(&mut self, world: &mut HashMap<Vec2, i8>) -> Result<bool, HaltCause> {
        if self.brain.step() {
            match self.brain.cause() {
                Some(HaltCause::NoMoreInput) => {
                    let color = world.get(&self.loc).cloned().unwrap_or(0i8);
                    self.brain.add_input(color as i64);
                    self.brain.resume();
                }
                Some(HaltCause::Exit) => {
                    return Ok(true);
                }
                Some(e) => {
                    return Err(e);
                }
                _ => {}
            }
        }
        if self.brain.pending_output() == 2 {
            let color = self.brain.pop_output().unwrap();
            let dir = self.brain.pop_output().unwrap();
            world.insert(self.loc, color as i8);
            match dir {
                0 => self.dir = rotl90(self.dir),
                1 => self.dir = rotr90(self.dir),
                _ => unreachable!("invalid direction, should be in {0, 1}"),
            }
            self.loc = vec_add(self.loc, self.dir);
        }
        Ok(false)
    }

    pub fn run(&mut self, world: &mut HashMap<Vec2, i8>) -> Result<(), HaltCause> {
        loop {
            let done = self.step(world)?;
            if done {
                return Ok(());
            }
        }
    }
}

fn part_1(tape: &Vec<i64>) {
    let mut robot = Robot::new();
    robot.brain.load(&tape);
    let mut world: HashMap<Vec2, i8> = HashMap::with_capacity(1024);
    robot.run(&mut world).unwrap_or_else(|e| {
        eprintln!("error: simulation failed ==> ({:?})", e);
        robot.brain.dump();
    });
    println!("part 1: {}", world.len());
}

fn part_2(tape: &Vec<i64>) {
    let mut robot = Robot::new();
    robot.brain.load(&tape);
    let mut world: HashMap<Vec2, i8> = HashMap::with_capacity(1024);
    world.insert((0, 0), 1);
    robot.run(&mut world).unwrap_or_else(|e| {
        eprintln!("error: simulation failed ==> ({:?})", e);
        robot.brain.dump();
    });
    println!("part 2:");
    draw(&world);
}

pub fn day11(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    part_1(&tape);
    part_2(&tape);

    Ok(())
}
