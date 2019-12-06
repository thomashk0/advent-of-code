use std::num::ParseIntError;

#[derive(Debug, Copy, Clone)]
pub enum HaltCause {
    Exit,
    InvalidPc,
    MemoryError(bool, i64),
}

#[derive(Debug)]
pub struct IntCodeState {
    pub tape: Vec<i64>,
    pc: i64,
    pub halt_cause: Option<HaltCause>,
    pub cycle: u64,
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
            pc: 0,
            halt_cause: None,
            cycle: 0,
        }
    }

    pub fn reset(&mut self) {
        self.pc = 0;
        self.halt_cause = None;
        self.cycle = 0;
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

    fn tape_read(&self, idx: i64) -> Result<i64, HaltCause> {
        self.access(idx)?;
        Ok(self.tape[idx as usize])
    }

    fn tape_write(&mut self, idx: i64, value: i64) -> Result<(), HaltCause> {
        self.access(idx)?;
        self.tape[idx as usize] = value;
        Ok(())
    }

    fn _step(&mut self) -> Result<(), HaltCause> {
        if self.pc < 0 || self.pc > self.tape.len() as i64 {
            return Err(HaltCause::InvalidPc);
        }
        let pc = self.pc as usize;
        let opcode = self.tape[pc];
        self.cycle += 1;
        if opcode == 99 {
            return Err(HaltCause::Exit);
        }
        let arg_0 = self.tape_read(self.pc + 1)?;
        let arg_1 = self.tape_read(self.pc + 2)?;
        let arg_2 = self.tape_read(self.pc + 3)?;
        let op_1 = self.tape_read(arg_0)?;
        let op_2 = self.tape_read(arg_1)?;
        match opcode {
            1 => self.tape_write(arg_2, op_1 + op_2)?,
            2 => self.tape_write(arg_2, op_1 * op_2)?,
            _ => {}
        }
        self.pc += 4;
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
        eprintln!("PC: {}", self.pc);
        eprintln!("Err: {:?}", self.halt_cause);
    }
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
    fn simple_sim() {
        for (&v, &r) in ["1,0,0,0,99", "2,4,4,5,99,0", "1,1,1,4,99,5,6,0,99"]
            .iter()
            .zip([2i64, 2, 30].iter())
        {
            let mut cpu = IntCodeState::new();
            cpu.load_str(v).unwrap();
            assert_eq!(cpu.run(), Some(r));
        }
    }
}
