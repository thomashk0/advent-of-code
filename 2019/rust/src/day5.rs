use crate::intcode::{dump_output, load_tape, IntCpu};
use std::io;

fn run_with_id(tape: &[i64], id: i64) -> IntCpu {
    let mut cpu = IntCpu::from_tape(tape);
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
    let mut s1 = run_with_id(&tape, 1);
    println!("part 1: {:?}", dump_output(&mut s1));
    let mut s2 = run_with_id(&tape, 5);
    println!("part 2: {}", s2.pop_output().unwrap());
    Ok(())
}
