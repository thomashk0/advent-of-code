use crate::intcode::{load_tape, HaltCause, IntCpu};
use std::collections::HashMap;
use std::fs::File;
use std::io;
use std::io::{Read, Write};

type Vec2 = (i64, i64);
type World = HashMap<(i64, i64), i8>;

pub fn limits(world: &World) -> (Vec2, Vec2) {
    let coords: Vec<Vec2> = world.iter().map(|(coords, _)| *coords).collect();
    assert!(coords.len() == world.len());
    let xmin = coords.iter().map(|p| p.0).min().unwrap();
    let xmax = coords.iter().map(|p| p.0).max().unwrap();
    let ymin = coords.iter().map(|p| p.1).min().unwrap();
    let ymax = coords.iter().map(|p| p.1).max().unwrap();
    ((xmin, xmax), (ymin, ymax))
}

pub fn draw(world: &World) {
    let ((xmin, xmax), (ymin, ymax)) = limits(world);
    //    println!("world.len() = {:?}", world.len());
    //    println!("{:?}", limits(world));
    for y in (ymin..=ymax).rev() {
        for x in xmin..=xmax {
            let c = world.get(&(x, y)).cloned().unwrap_or(0);
            let tile = match c {
                0 => " ",
                1 => "#",
                2 => "*",
                3 => "=",
                4 => "o",
                _ => "?",
            };
            print!("{}", tile);
        }
        println!();
    }
}

pub fn query_dir() -> i64 {
    let mut line = String::new();
    let _ = std::io::stdin()
        .read_line(&mut line)
        .expect("Failed to read line");
    match line.as_bytes()[0] {
        b'l' | b'L' => -1,
        b'r' | b'R' => 1,
        _ => 0,
    }
}

struct Arcade {
    pub cpu: IntCpu,
    pub score: i64,
    pub inputs: Vec<i8>,
    pub move_history: Vec<i8>,
}

impl Arcade {
    pub fn new(tape: &[i64], inputs: &[i8]) -> Self {
        Arcade {
            cpu: IntCpu::from_tape(&tape),
            score: 0,
            inputs: inputs.iter().rev().cloned().collect(),
            move_history: Vec::with_capacity(2048),
        }
    }

    pub fn pop_draw_primitive(&mut self) -> Option<((i64, i64), i64)> {
        if self.cpu.pending_output() < 3 {
            return None;
        }
        let x = self.cpu.pop_output().unwrap();
        let y = self.cpu.pop_output().unwrap();
        let d = self.cpu.pop_output().unwrap();
        Some(((x, y), d))
    }

    fn get_next_dir(&mut self) -> i64 {
        if let Some(x) = self.inputs.pop() {
            return x as i64;
        }
        query_dir()
    }

    pub fn step(&mut self, world: &mut World) -> Result<bool, HaltCause> {
        if self.cpu.step() {
            match self.cpu.cause() {
                Some(HaltCause::Exit) => {
                    return Ok(true);
                }
                Some(HaltCause::NoMoreInput) => {
                    println!("Score: {}", self.score);
                    draw(world);
                    let input = self.get_next_dir();
                    self.move_history.push(input as i8);
                    println!("Moving dir: {}", input);
                    self.cpu.add_input(input);
                    self.cpu.resume();
                }
                Some(e) => {
                    return Err(e);
                }
                _ => {}
            }
        }
        if let Some((pos, c)) = self.pop_draw_primitive() {
            if pos.0 == -1 && pos.1 == 0 {
                self.score = c;
            } else {
                world.insert(pos, c as i8);
            }
        }
        Ok(false)
    }

    pub fn run(&mut self, world: &mut World) -> Result<(), HaltCause> {
        loop {
            let done = self.step(world)?;
            if done {
                return Ok(());
            }
        }
    }
}

pub fn part_1(tape: &Vec<i64>) {
    let mut world: World = HashMap::with_capacity(1024);
    let mut arcade = Arcade::new(&tape, &[]);
    arcade.run(&mut world).unwrap_or_else(|e| {
        eprintln!("simulation failed => {:?}", e);
        arcade.cpu.dump();
    });
    println!("part 1: {}", world.iter().filter(|p| *(p.1) == 2).count());
}

fn load_history(path: &str) -> Vec<i8> {
    let mut f = File::open(path).expect("unable to open file");
    let mut tape_str = String::new();
    f.read_to_string(&mut tape_str).expect("read error");
    tape_str
        .trim()
        .as_bytes()
        .iter()
        .map(|c| match c {
            b'l' => -1,
            b'r' => 1,
            b'-' => 0,
            _ => unreachable!("invalid char"),
        })
        .collect()
}

pub fn part_2(tape: &Vec<i64>) {
    let history = load_history("history.txt");
    let mut world: World = HashMap::with_capacity(1024);
    let mut arcade = Arcade::new(&tape, &history[..]);
    arcade.cpu.tape_write(0, 2).unwrap();
    arcade.run(&mut world).unwrap_or_else(|e| {
        eprintln!("simulation failed => {:?}", e);
        arcade.cpu.dump();
    });
    println!("part 2: {}", arcade.score);
    let mut f = File::create("history-out.txt").unwrap();
    let hist_out: Vec<u8> = arcade
        .move_history
        .iter()
        .map(|b| match b {
            -1 => b'l',
            1 => b'r',
            0 => b'-',
            _ => unreachable!(),
        })
        .collect();
    f.write_all(&hist_out[..]).unwrap();
}

pub fn day13(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    part_1(&tape);
    part_2(&tape);
    Ok(())
}
