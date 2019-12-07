use crate::intcode;
use crate::intcode::IntCodeState;
use std::fs::File;
use std::io;
use std::io::Read;

pub fn load_tape(input: &str) -> io::Result<Vec<i64>> {
    let mut f = File::open(input)?;
    let mut tape_str = String::new();
    f.read_to_string(&mut tape_str)?;
    Ok(intcode::parse_prog(tape_str.trim()).unwrap())
}

fn run_with_id(tape: Vec<i64>, id: i64) -> IntCodeState {
    let mut cpu = intcode::IntCodeState::new();
    cpu.load(tape);
    cpu.input.push_front(id);
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
