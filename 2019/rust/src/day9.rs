use crate::intcode::{load_tape, IntCpu};
use std::{io, process};

fn run_or_die(cpu: &mut IntCpu) {
    match cpu.run() {
        None => {
            eprintln!("Simulation failed...");
            cpu.dump();
            process::exit(1);
        }
        _ => {}
    }
}

pub fn day9(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    let mut cpu = IntCpu::new();
    cpu.load(tape.clone());
    cpu.add_input(1);
    run_or_die(&mut cpu);
    println!("part 1: {}", cpu.pop_output().unwrap());

    cpu.reset();
    cpu.load(tape.clone());
    cpu.add_input(2);
    run_or_die(&mut cpu);
    println!("part 2: {}", cpu.pop_output().unwrap());
    Ok(())
}
