#[macro_use] extern crate scan_fmt;
#[macro_use] extern crate itertools;

use std::io;
use std::env;
use std::collections::HashMap;
use std::process;
pub mod days;

type Solution = fn()->io::Result<()>;
static DAYS : &[(i32, Solution)] = &[
    (9, days::day9::run),
    (10, days::day10::run),
    (11, days::day11::run),
    (12, days::day12::run)];

pub fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("USAGE: ./{} [DAY_NUMBER]", args[0]);
        process::exit(1);
    }
    let day_num = args[1].parse::<i32>().unwrap();
    let days_map: HashMap<i32, fn()->io::Result<()>> = DAYS.iter().cloned().collect();
    match days_map.get(&day_num) {
        Some(&f) => {
            f()?;
        },
        None => {
            eprintln!("Day {} is not available", day_num);
            process::exit(1);
        }
    }
    Ok(())
}