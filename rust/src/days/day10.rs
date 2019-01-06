use std::io;
use std::io::prelude::*;
use std::collections::HashSet;

type Point = (i32, i32);
type Velocity = (i32, i32);

struct State {
    points : Vec<Point>,
    velocity : Vec<Velocity>
}

impl State {
    pub fn with_capacity(n : usize) -> Self {
        State {
            points : Vec::with_capacity(n),
            velocity : Vec::with_capacity(n)
        }
    }

    pub fn step(&mut self) {
        for i in 0..self.points.len() {
            let p = &mut self.points[i];
            let v = &self.velocity[i];
            p.0 += v.0;
            p.1 += v.1;
        }
    }

    pub fn limits(&self) -> ((i32, i32), (i32, i32)) {
        let xmin = self.points.iter().min_by_key(|p| p.0).unwrap().0;
        let xmax = self.points.iter().max_by_key(|p| p.0).unwrap().0;
        let ymin = self.points.iter().min_by_key(|p| p.1).unwrap().1;
        let ymax = self.points.iter().max_by_key(|p| p.1).unwrap().1;
        ((xmin, xmax), (ymin, ymax))
    }

    pub fn draw(&self) -> bool {
        let ((xmin, xmax), (ymin, ymax)) = self.limits();
        if (xmax - xmin) >= 200 && (ymax - ymin) >= 200 {
            return false;
        }
        let s : HashSet<Point> = self.points.iter().cloned().collect();
        for y in ymin..=ymax {
            for x in xmin..=xmax {
                let tile = if s.contains(&(x, y)) { "#" } else { "." };
                print!("{}", tile);
            }
            println!();
        }
        println!("{:?}", s);
        true
    }
}

pub fn run() -> io::Result<()> {
    use std::process;
    let mut s = State::with_capacity(256);
    for line in io::stdin().lock().lines() {
        match scan_fmt!(&line.unwrap(), "position=< {d}, {d}> velocity=< {d}, {d}>", i32, i32, i32, i32) {
            (Some(x), Some(y), Some(vx), Some(vy)) => {
                s.points.push((x, y));
                s.velocity.push((vx, vy));
            },
            _ => {
                eprintln!("parsing failed");
                process::exit(1);
            }
        };
    }
    for i in 0..=100_000 {
        println!("=== State after {} seconds ===", i);
        if s.draw() {
            for j in 1..20 {
                println!("=== State after {} seconds ===", i + j);
                s.step();
                s.draw();
            }
            break;
        }
        s.step();
    }
    Ok(())
}