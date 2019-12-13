extern crate aoc;
use aoc::{day11, day13, day2, day5, day7, day9};
use std::{env, process};

pub fn usage(prog_name: &str) {
    eprintln!("USAGE: ./{} [DAY_NUMBER]", prog_name);
}

pub fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        usage(&args[0]);
        process::exit(1);
    }
    match args[1].trim() {
        "2" => {
            day2::day2("assets/day2-input").unwrap_or_else(|e| {
                eprintln!("error: {:?}", e);
            });
        }
        "5" => {
            day5::day5("assets/day5-input").unwrap_or_else(|e| {
                eprintln!("error: {:?}", e);
            });
        }
        "7" => day7::day7(&args[2]).unwrap_or_else(|e| {
            eprintln!("error: {:?}", e);
        }),
        "9" => day9::day9(&args[2]).unwrap_or_else(|e| {
            eprintln!("error: {:?}", e);
        }),
        "11" => day11::day11(&args[2]).unwrap_or_else(|e| {
            eprintln!("error: {:?}", e);
        }),
        "13" => day13::day13(&args[2]).unwrap_or_else(|e| {
            eprintln!("error: {:?}", e);
        }),
        _ => {
            eprintln!("invalid day given {}", args[1]);
            usage(&args[0]);
            process::exit(1);
        }
    }
}
