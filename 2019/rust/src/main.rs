extern crate aoc;
use aoc::{day2, day5};
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
        _ => {
            eprintln!("invalid day given {}", args[1]);
            usage(&args[0]);
            process::exit(1);
        }
    }
}
