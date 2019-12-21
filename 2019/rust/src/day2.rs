use super::intcode;
use std::fs::File;
use std::io;
use std::io::Read;

pub fn day2(input: &str) -> io::Result<()> {
    let mut f = File::open(input)?;
    let mut tape_str = String::new();
    f.read_to_string(&mut tape_str)?;
    let mut cpu = intcode::IntCpu::from_str(tape_str.trim()).unwrap();
    cpu.tape_write(1, 12).unwrap();
    cpu.tape_write(2, 2).unwrap();

    println!(
        "part 1: {}",
        cpu.run().unwrap_or_else(|| {
            cpu.dump();
            0
        })
    );

    for verb in 0..100 {
        for noun in 0..100 {
            cpu.reset();
            cpu.tape_write(1, verb).unwrap();
            cpu.tape_write(2, noun).unwrap();
            if cpu.run().unwrap() == 19690720 {
                println!("part 2: {}", 100 * verb + noun)
            }
        }
    }

    Ok(())
}
