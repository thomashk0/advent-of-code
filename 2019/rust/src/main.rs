extern crate aoc;
use aoc::day2;

pub fn main() {
    day2::day2("assets/day2-input").unwrap_or_else(|e| {
        eprintln!("error: {:?}", e);
    });
}
