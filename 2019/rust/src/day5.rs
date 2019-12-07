use crate::intcode::{IntCodeState, load_tape};
use std::io;


fn run_with_id(tape: Vec<i64>, id: i64) -> IntCodeState {
    let mut cpu = IntCodeState::new();
    cpu.load(tape);
    cpu.add_input(id);
    match cpu.run() {
        None => {
            eprintln!("something went wrong...");
            cpu.dump();
        }
        _ => {}
    }
    cpu
}

pub fn day5(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    let mut s1 = run_with_id(tape.clone(), 1);
    print!("part 1: {} (output=[", s1.output.pop_front().unwrap());
    for p in s1.output {
        print!("{}, ", p);
    }
    println!("])");

    let mut s2 = run_with_id(tape.clone(), 5);
    print!("part 2: {} (output=[", s2.output.pop_front().unwrap());
    for p in s2.output {
        print!("{}, ", p);
    }
    println!("])");
    Ok(())
}
