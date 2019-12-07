use std::collections::VecDeque;
use std::num::ParseIntError;
use std::io;
use std::fs::File;
use std::io::Read;

#[derive(Debug, Copy, Clone)]
pub enum HaltCause {
    Exit,
    InvalidPc,
    MemoryError(bool, i64),
    DecodingFailed(i64, usize),
}

#[derive(Debug)]
pub struct IntCodeState {
    pub tape: Vec<i64>,
    input: VecDeque<i64>,
    pub output: VecDeque<i64>,
    pc: i64,
    pub halt_cause: Option<HaltCause>,
    pub cycle: u64,
}

#[derive(Debug, Copy, Clone)]
pub struct Opcode {
    code: u8,
    param_mode_0: u8,
    param_mode_1: u8,
    param_mode_2: u8,
}

impl Opcode {
    pub fn decode(v: i64) -> Self {
        Opcode {
            code: (v % 100) as u8,
            param_mode_0: ((v / 100) % 10) as u8,
            param_mode_1: ((v / 1000) % 10) as u8,
            param_mode_2: ((v / 10_000) % 10) as u8,
        }
    }

    pub fn check(&self) -> Result<(), usize> {
        match self.code {
            1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 99 => Ok(()),
            _ => Err(0usize),
        }?;
        for (i, w) in [self.param_mode_0, self.param_mode_1, self.param_mode_2]
            .iter()
            .enumerate()
        {
            if *w >= 2 {
                return Err(i + 1);
            }
        }
        Ok(())
    }
}

pub fn parse_prog(data: &str) -> Result<Vec<i64>, ParseIntError> {
    data.split(|c: char| c == ',')
        .map(|x: &str| x.parse::<i64>())
        .collect()
}

impl IntCodeState {
    pub fn new() -> Self {
        IntCodeState {
            tape: Vec::with_capacity(2048),
            input: VecDeque::with_capacity(128),
            output: VecDeque::with_capacity(128),
            pc: 0,
            halt_cause: None,
            cycle: 0,
        }
    }

    pub fn reset(&mut self) {
        self.pc = 0;
        self.halt_cause = None;
        self.cycle = 0;
        self.input.clear();
        self.output.clear();
    }

    pub fn load(&mut self, tape: Vec<i64>) {
        self.tape = tape;
    }

    pub fn load_str(&mut self, tape: &str) -> Result<(), ParseIntError> {
        let v = parse_prog(tape)?;
        self.load(v);
        Ok(())
    }

    pub fn halted(&self) -> bool {
        self.halt_cause.is_some()
    }

    fn access(&self, addr: i64) -> Result<(), HaltCause> {
        if addr < 0 || addr > self.tape.len() as i64 {
            return Err(HaltCause::MemoryError(true, addr));
        }
        Ok(())
    }

    pub fn add_input(&mut self, x: i64) {
        self.input.push_front(x);
    }

    pub fn pop_output(&mut self) -> Option<i64> {
        self.output.pop_back()
    }

    fn read_arg(&self, mode: u8, idx: i64) -> Result<i64, HaltCause> {
        match mode {
            0 => self.tape_read(idx),
            1 => Ok(idx),
            _ => panic!("invalid mode"),
        }
    }

    fn tape_read(&self, idx: i64) -> Result<i64, HaltCause> {
        self.access(idx)?;
        Ok(self.tape[idx as usize])
    }

    fn tape_write(&mut self, idx: i64, value: i64) -> Result<(), HaltCause> {
        self.access(idx)?;
        self.tape[idx as usize] = value;
        Ok(())
    }

    fn get_operand(&self, op: Opcode, i: usize) -> Result<i64, HaltCause> {
        assert!(i >= 1 && i <= 3);
        let mode = match i {
            1 => op.param_mode_0,
            2 => op.param_mode_1,
            3 => op.param_mode_2,
            _ => unreachable!(),
        };
        let idx = self.tape_read(self.pc + i as i64)?;
        self.read_arg(mode, idx)
    }

    fn _step(&mut self) -> Result<(), HaltCause> {
        if self.pc < 0 || self.pc > self.tape.len() as i64 {
            return Err(HaltCause::InvalidPc);
        }
        let pc = self.pc as usize;
        let insn = self.tape[pc];
        let op = Opcode::decode(insn);
        op.check().map_err(|e| HaltCause::DecodingFailed(insn, e))?;
        //let opcode = self.tape[pc];
        if op.code == 99 {
            return Err(HaltCause::Exit);
        }

        match op.code {
            1 => {
                let out = self.tape_read(self.pc + 3)?;
                self.tape_write(out, self.get_operand(op, 1)? + self.get_operand(op, 2)?)?;
                self.pc += 4;
            }
            2 => {
                let out = self.tape_read(self.pc + 3)?;
                self.tape_write(out, self.get_operand(op, 1)? * self.get_operand(op, 2)?)?;
                self.pc += 4;
            }
            3 => {
                let out = self.tape_read(self.pc + 1)?;
                let w = self.input.pop_back().unwrap();
                self.tape_write(out, w)?;
                self.pc += 2;
            }
            4 => {
                self.output.push_front(self.get_operand(op, 1)?);
                self.pc += 2;
            }
            6 => {
                if self.get_operand(op, 1)? == 0 {
                    self.pc = self.get_operand(op, 2)?;
                } else {
                    self.pc += 3;
                }
            }
            5 => {
                if self.get_operand(op, 1)? != 0 {
                    self.pc = self.get_operand(op, 2)?;
                } else {
                    self.pc += 3;
                }
            }
            7 => {
                let out = self.tape_read(self.pc + 3)?;
                let result = if self.get_operand(op, 1)? < self.get_operand(op, 2)? {
                    1
                } else {
                    0
                };
                self.tape_write(out, result)?;
                self.pc += 4;
            }
            8 => {
                let out = self.tape_read(self.pc + 3)?;
                let result = if self.get_operand(op, 1)? == self.get_operand(op, 2)? {
                    1
                } else {
                    0
                };
                self.tape_write(out, result)?;
                self.pc += 4;
            }
            _ => panic!("code not implemented: {}", op.code),
        }
        self.cycle += 1;
        Ok(())
    }

    pub fn step(&mut self) -> bool {
        if self.halted() {
            return true;
        }
        self._step()
            .map_err(|e| {
                self.halt_cause = Some(e);
                e
            })
            .is_err()
    }

    pub fn exit_code(&self) -> i64 {
        self.tape[0]
    }

    pub fn run(&mut self) -> Option<i64> {
        while !self.step() {}
        match self.halt_cause {
            Some(HaltCause::Exit) => Some(self.exit_code()),
            _ => None,
        }
    }

    pub fn dump(&self) {
        eprintln!("cycle: {}", self.cycle);
        eprintln!("pc:    {}", self.pc);
        eprintln!("err:   {:?}", self.halt_cause);
    }
}

pub fn load_tape(input: &str) -> io::Result<Vec<i64>> {
    let mut f = File::open(input)?;
    let mut tape_str = String::new();
    f.read_to_string(&mut tape_str)?;
    Ok(parse_prog(tape_str.trim()).unwrap())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_tape() {
        assert_eq!(parse_prog("1,0,0,0,99"), Ok([1i64, 0, 0, 0, 99].to_vec()));
        assert!(parse_prog("1,xx,0").is_err());
    }

    #[test]
    fn basic_simulations() {
        for (&v, &r) in ["1,0,0,0,99", "2,4,4,5,99,0", "1,1,1,4,99,5,6,0,99"]
            .iter()
            .zip([2i64, 2, 30].iter())
        {
            let mut cpu = IntCodeState::new();
            cpu.load_str(v).unwrap();
            assert_eq!(cpu.run(), Some(r));
        }
    }

    #[test]
    fn decoding() {
        let opcode = Opcode::decode(1002);
        assert_eq!(opcode.code, 2);
        assert_eq!(opcode.param_mode_0, 0);
        assert_eq!(opcode.param_mode_1, 1);
        assert_eq!(opcode.param_mode_2, 0);
        assert!(Opcode::decode(99).check().is_ok());
        assert!(Opcode::decode(0).check().is_err());
    }
}
