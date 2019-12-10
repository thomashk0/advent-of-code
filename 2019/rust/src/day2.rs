use super::intcode;
use std::fs::File;
use std::io;
use std::io::Read;

pub fn day2(input: &str) -> io::Result<()> {
    let mut f = File::open(input)?;
    let mut tape_str = String::new();
    f.read_to_string(&mut tape_str)?;
    let mut cpu = intcode::IntCpu::new();
    let mut tape = intcode::parse_prog(tape_str.trim()).unwrap();
    tape[1] = 12;
    tape[2] = 2;
    cpu.load(tape.clone());

    println!(
        "part 1: {}",
        cpu.run().unwrap_or_else(|| {
            cpu.dump();
            0
        })
    );

    for verb in 0..100 {
        for noun in 0..100 {
            tape[1] = verb;
            tape[2] = noun;
            cpu.reset();
            cpu.load(tape.clone());
            if cpu.run().unwrap() == 19690720 {
                println!("part 2: {}", 100 * verb + noun)
            }
        }
    }

    Ok(())
}
