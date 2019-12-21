use std::cmp;
use std::collections::{HashMap, HashSet, VecDeque};
use std::fs::File;
use std::io;
use std::io::Read;
use std::num::ParseIntError;

#[derive(Debug, Copy, Clone)]
pub enum HaltCause {
    Exit,
    InvalidPc,
    MemoryError(bool, i64),
    DecodeError(DecodeError),
    NoMoreInput,
}

impl From<DecodeError> for HaltCause {
    fn from(e: DecodeError) -> Self {
        HaltCause::DecodeError(e)
    }
}

#[derive(Debug, Copy, Clone)]
pub enum DecodeError {
    UnknownOpcode,
    UnknownMode,
    BadMode,
    MissingData,
}

#[derive(Debug, Copy, Clone)]
pub enum Operand {
    Position(CpuWord),
    Imm(CpuWord),
    Relative(CpuWord),
}

impl Operand {
    fn new(mode: u8, value: CpuWord) -> Option<Self> {
        match mode {
            0 => Some(Operand::Position(value)),
            1 => Some(Operand::Imm(value)),
            2 => Some(Operand::Relative(value)),
            _ => None,
        }
    }

    pub fn as_position(&self) -> Result<CpuWord, DecodeError> {
        match self {
            Operand::Position(v) => Ok(*v),
            _ => Err(DecodeError::BadMode),
        }
    }
}

#[derive(Debug, Copy, Clone)]
pub enum Op {
    Add(Operand, Operand, Operand),
    Mul(Operand, Operand, Operand),
    Input(Operand),
    Output(Operand),
    Bnz(Operand, Operand),
    Bez(Operand, Operand),
    Slt(Operand, Operand, Operand),
    Seq(Operand, Operand, Operand),
    SetRelative(Operand),
    Halt,
    Raw(i64),
    Nop(),
    LoadImm(Operand, i64),
    Copy(Operand, Operand),
    Goto(Operand),
}

impl Op {
    pub fn decode(insn: &[i64]) -> Result<(usize, Op), DecodeError> {
        let get_idx = |i| insn.get(i).copied().ok_or(DecodeError::MissingData);

        let i = get_idx(0)?;
        let code = (i % 100) as u8;
        let params = [
            ((i / 100) % 10) as u8,
            ((i / 1000) % 10) as u8,
            ((i / 10_000) % 10) as u8,
        ];
        let get_arg = |i| {
            get_idx(i).and_then(|value| {
                Operand::new(params[i - 1], value).ok_or(DecodeError::UnknownMode)
            })
        };
        let arg = [get_arg(1), get_arg(2), get_arg(3)];
        match code {
            1 => Ok((4, Op::Add(arg[0]?, arg[1]?, arg[2]?))),
            2 => Ok((4, Op::Mul(arg[0]?, arg[1]?, arg[2]?))),
            3 => Ok((2, Op::Input(arg[0]?))),
            4 => Ok((2, Op::Output(arg[0]?))),
            5 => Ok((3, Op::Bnz(arg[0]?, arg[1]?))),
            6 => Ok((3, Op::Bez(arg[0]?, arg[1]?))),
            7 => Ok((4, Op::Slt(arg[0]?, arg[1]?, arg[2]?))),
            8 => Ok((4, Op::Seq(arg[0]?, arg[1]?, arg[2]?))),
            9 => Ok((2, Op::SetRelative(arg[0]?))),
            99 => Ok((1, Op::Halt)),
            _ => Err(DecodeError::UnknownOpcode),
        }
    }

    pub fn get_output_operand(&self) -> Option<Operand> {
        match self {
            Op::Add(o, _, _) => Some(*o),
            Op::Mul(o, _, _) => Some(*o),
            Op::Input(o) => Some(*o),
            Op::Slt(o, _, _) => Some(*o),
            Op::Seq(o, _, _) => Some(*o),
            _ => None,
        }
    }

    pub fn get_operand(&self, idx: usize) -> Option<Operand> {
        match self.clone() {
            Op::Add(_, x, y) => [x, y].get(idx).cloned(),
            Op::Mul(_, x, y) => [x, y].get(idx).cloned(),
            Op::Output(x) => [x].get(idx).cloned(),
            Op::Bnz(x, y) => [x, y].get(idx).cloned(),
            Op::Bez(x, y) => [x, y].get(idx).cloned(),
            Op::Slt(_, x, y) => [x, y].get(idx).cloned(),
            Op::Seq(_, x, y) => [x, y].get(idx).cloned(),
            Op::SetRelative(x) => [x].get(idx).cloned(),
            _ => None,
        }
    }

    pub fn is_branch(&self) -> bool {
        match self {
            Op::Bnz(_, _) => true,
            Op::Bez(_, _) => true,
            _ => false,
        }
    }
}

pub fn parse_prog(data: &str) -> Result<Vec<i64>, ParseIntError> {
    data.split(|c: char| c == ',')
        .map(|x: &str| x.parse::<i64>())
        .collect()
}

type CpuWord = i64;

#[derive(Debug, Clone)]
pub struct IntCpu {
    original_tape: Vec<i64>,
    tape: Vec<CpuWord>,
    memory: HashMap<CpuWord, CpuWord>,
    input: VecDeque<CpuWord>,
    output: VecDeque<CpuWord>,
    pc: CpuWord,
    relative_base: CpuWord,
    halt_cause: Option<HaltCause>,
    cycle: u64,
}

fn from_bool(b: bool) -> CpuWord {
    if b {
        1
    } else {
        0
    }
}

impl IntCpu {
    pub fn from_tape(tape: &[i64]) -> Self {
        IntCpu {
            original_tape: tape.iter().cloned().collect(),
            tape: tape.iter().map(|x| CpuWord::from(*x)).collect(),
            memory: HashMap::with_capacity(cmp::max(32, tape.len())),
            input: VecDeque::with_capacity(16),
            output: VecDeque::with_capacity(16),
            pc: 0,
            relative_base: 0,
            halt_cause: None,
            cycle: 0,
        }
    }

    pub fn from_str(tape: &str) -> Result<Self, ParseIntError> {
        let v = parse_prog(tape)?;
        Ok(IntCpu::from_tape(&v[..]))
    }

    pub fn reset(&mut self) {
        *self = IntCpu::from_tape(&self.original_tape[..]);
    }

    pub fn reset_tape(&mut self, tape: &[i64]) {
        *self = IntCpu::from_tape(&tape);
    }

    pub fn halted(&self) -> bool {
        self.halt_cause.is_some()
    }

    fn access(&self, addr: CpuWord) -> Result<Option<usize>, HaltCause> {
        if addr < 0 {
            return Err(HaltCause::MemoryError(true, addr as i64));
        }
        if addr < self.tape.len() as CpuWord {
            return Ok(Some(addr as usize));
        }
        Ok(None)
    }

    pub fn add_input(&mut self, x: i64) {
        self.input.push_front(CpuWord::from(x));
    }

    pub fn pop_output(&mut self) -> Option<i64> {
        self.output.pop_back().map(|x| x as i64)
    }

    pub fn pending_output(&self) -> usize {
        self.output.len()
    }

    pub fn tape_read(&self, idx: CpuWord) -> Result<CpuWord, HaltCause> {
        match self.access(idx)? {
            Some(offset) => Ok(self.tape[offset]),
            None => Ok(*self.memory.get(&idx).unwrap_or(&(0 as CpuWord))),
        }
    }

    pub fn tape_write(&mut self, idx: CpuWord, value: CpuWord) -> Result<(), HaltCause> {
        match self.access(idx)? {
            Some(offset) => {
                self.tape[offset] = value;
            }
            None => {
                self.memory.insert(idx, value);
            }
        }
        Ok(())
    }

    fn query(&self, op: Operand) -> Result<CpuWord, HaltCause> {
        match op {
            Operand::Position(addr) => self.tape_read(addr),
            Operand::Imm(imm) => Ok(imm),
            Operand::Relative(addr) => self.tape_read(self.relative_base + addr),
        }
    }

    fn write(&mut self, dst: Operand, value: CpuWord) -> Result<(), HaltCause> {
        match dst {
            Operand::Position(addr) => self.tape_write(addr, value),
            Operand::Imm(_) => Err(HaltCause::DecodeError(DecodeError::BadMode)),
            Operand::Relative(addr) => self.tape_write(self.relative_base + addr, value),
        }
    }

    fn _step(&mut self) -> Result<(), HaltCause> {
        self.cycle += 1;

        if self.pc < 0 || self.pc > self.tape.len() as CpuWord {
            return Err(HaltCause::InvalidPc);
        }
        let pc = self.pc as usize;
        let (pc_step, op) = Op::decode(&self.tape[pc..])?;
        let pc_next = self.pc + pc_step as CpuWord;
        let mut pc_branch: Option<i64> = None;
        match op {
            Op::Add(x, y, o) => {
                self.write(o, self.query(x)? + self.query(y)?)?;
            }
            Op::Mul(x, y, o) => {
                self.write(o, self.query(x)? * self.query(y)?)?;
            }
            Op::Input(o) => {
                let w = self.input.pop_back().ok_or(HaltCause::NoMoreInput)?;
                self.write(o, w)?;
            }
            Op::Output(x) => self.output.push_front(self.query(x)?),
            Op::Bnz(x, off) => {
                if self.query(x)? != 0 {
                    pc_branch = Some(self.query(off)?);
                }
            }
            Op::Bez(x, off) => {
                if self.query(x)? == 0 {
                    pc_branch = Some(self.query(off)?);
                }
            }
            Op::Slt(x, y, o) => {
                self.write(o, from_bool(self.query(x)? < self.query(y)?))?;
            }
            Op::Seq(x, y, o) => {
                self.write(o, from_bool(self.query(x)? == self.query(y)?))?;
            }
            Op::SetRelative(off) => {
                self.relative_base += self.query(off)?;
            }
            Op::Halt => {
                return Err(HaltCause::Exit);
            }
            op => {
                unreachable!(
                    "Instructions of type {:?} are not supposed to exists in executable programs",
                    op
                );
            }
        }

        self.pc = pc_branch.unwrap_or(pc_next);
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

    pub fn cause(&self) -> Option<HaltCause> {
        self.halt_cause
    }

    pub fn exit_code(&self) -> i64 {
        self.tape[0] as i64
    }

    pub fn resume(&mut self) {
        self.halt_cause = None;
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

pub fn dump_output(cpu: &mut IntCpu) {
    let mut is_first = true;
    loop {
        match cpu.pop_output() {
            Some(w) => {
                if is_first {
                    is_first = false;
                } else {
                    print!(",")
                }
                print!("{}", w);
            }
            None => break,
        }
    }
    println!();
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
            let mut cpu = IntCpu::from_str(v).unwrap();
            assert_eq!(cpu.run(), Some(r));
        }
    }
}
