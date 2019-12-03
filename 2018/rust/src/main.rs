#![feature(drain_filter)]
#[macro_use] extern crate scan_fmt;
#[macro_use] extern crate itertools;
extern crate pathfinding;

use std::io;
use std::env;
use std::collections::HashMap;
use std::process;
pub mod days;

use crate::days::*;
type Solution = fn()->io::Result<()>;
static DAYS : &[(i32, Solution)] = &[
    (9, day9::run),
    (10, day10::run),
    (11, day11::run),
    (12, day12::run),
    (13, day13::run),
    (15, day15::run)];

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