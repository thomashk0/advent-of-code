use crate::intcode::{load_tape, IntCpu};
use itertools;
use itertools::Itertools;
use std::collections::VecDeque;
use std::convert::TryInto;
use std::io;

type Cpu = IntCpu;

pub struct Amp {
    stages: [Cpu; 5],
    pub input: VecDeque<i64>,
}

fn run_stage(cpu: &mut Cpu) -> Option<i64> {
    loop {
        cpu.step();
        if let Some(x) = cpu.pop_output() {
            return Some(x);
        }
        if cpu.halted() {
            return None;
        }
    }
}

impl Amp {
    pub fn new(tape: &[i64]) -> Self {
        Self {
            stages: [
                Cpu::from_tape(&tape),
                Cpu::from_tape(&tape),
                Cpu::from_tape(&tape),
                Cpu::from_tape(&tape),
                Cpu::from_tape(&tape),
            ],
            input: VecDeque::with_capacity(128),
        }
    }

    pub fn reset_phase(&mut self, phase: &[i64; 5]) {
        for (cpu, phase) in self.stages.iter_mut().zip(phase.iter()) {
            cpu.reset();
            cpu.add_input(*phase);
        }
    }

    pub fn run(&mut self, x: i64) -> Option<i64> {
        self.stages[0].add_input(x);
        for i in 0usize..4 {
            run_stage(&mut self.stages[i]).map(|w| {
                self.stages[i + 1].add_input(w);
            });
        }
        run_stage(&mut self.stages[4])
    }

    pub fn run_loop(&mut self) -> i64 {
        let mut w = 0i64;
        loop {
            match self.run(w) {
                Some(x) => {
                    w = x;
                }
                None => break,
            }
        }
        w
    }
}

pub fn day7(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    let mut amp = Amp::new(&tape[..]);

    {
        let perms = (0i64..=4).permutations(5);
        let part_1 = perms
            .map(|p| {
                amp.reset_phase(p.as_slice().try_into().unwrap());
                amp.run(0).unwrap()
            })
            .max()
            .unwrap();
        println!("part 1: {}", part_1);
    }

    {
        let perms = (5i64..=9).permutations(5);
        let part_2 = perms
            .map(|p| {
                amp.reset_phase(p.as_slice().try_into().unwrap());
                amp.run_loop()
            })
            .max()
            .unwrap();
        println!("part 2: {}", part_2);
    }

    Ok(())
}
