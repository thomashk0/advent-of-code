/// Disassembling framework for IntCode
use crate::intcode::{load_tape, Op, Operand};
use colored::Colorize;
use std::collections::{HashMap, HashSet};
use std::io;

pub fn pp_sp_offset(o: i64) -> String {
    if o == 0 {
        format!("{}", "sp".yellow())
    } else {
        format!(
            "{} {} {}",
            "sp".yellow(),
            if o > 0 { "+" } else { "-" },
            o.abs()
        )
    }
}

struct IntCodeIt<'a> {
    tape: &'a [i64],
    pc: usize,
}

impl<'a> IntCodeIt<'a> {
    fn new(tape: &'a [i64]) -> Self {
        IntCodeIt { tape, pc: 0 }
    }
}

impl Iterator for IntCodeIt<'_> {
    type Item = (usize, Op);

    fn next(&mut self) -> Option<Self::Item> {
        if self.pc >= self.tape.len() {
            return None;
        }
        let pc = self.pc;
        let op = Op::decode(&self.tape[self.pc..]);
        match op {
            Ok((inc, op)) => {
                self.pc += inc;
                Some((pc, op))
            }
            Err(_) => {
                self.pc += 1;
                Some((pc, Op::Raw(self.tape[pc])))
            }
        }
    }
}

fn disassemble(tape: &[i64]) -> IntCodeIt {
    IntCodeIt::new(tape)
}

struct Disassembler {
    tape: Vec<i64>,
    insn: Vec<Op>,
    offset: Vec<usize>,
    annotation: HashMap<usize, String>,
    modified: HashSet<i64>,
    entries: HashSet<i64>,
}

impl Disassembler {
    pub fn disassemble(tape: &[i64]) -> Self {
        let c = tape.len() / 2;
        let mut b = Disassembler {
            tape: tape.iter().cloned().collect(),
            insn: Vec::with_capacity(c),
            offset: Vec::with_capacity(c),
            annotation: HashMap::with_capacity(c),
            modified: HashSet::default(),
            entries: HashSet::default(),
        };
        for (pc, op) in disassemble(&tape) {
            b.insn.push(op);
            b.offset.push(pc);
        }
        b
    }

    fn operand_value(&self, o: Operand) -> Option<i64> {
        match o {
            Operand::Imm(i) => Some(i),
            _ => None,
        }
    }

    /// Find (some) modified memory area
    fn analyze_modified(&mut self) {
        for insn in &self.insn {
            match insn.get_output_operand() {
                Some(Operand::Position(o)) => {
                    self.modified.insert(o);
                }
                _ => {}
            }
        }
    }

    fn analyze_branch(&mut self) {
        for insn in &self.insn {
            let v = match insn {
                Op::Bnz(_, o) => self.operand_value(*o),
                Op::Bez(_, o) => self.operand_value(*o),
                _ => None,
            };
            if let Some(i) = v {
                self.entries.insert(i);
            }
        }
    }

    fn simplify_insn(&self, op: &Op) -> Option<Op> {
        match op {
            Op::Add(_, _, _) => {}
            Op::Mul(_, _, _) => {}
            Op::Input(_) => {}
            Op::Output(_) => {}
            Op::Bnz(cond, o) => {
                if let Some(x) = self.operand_value(*cond) {
                    if x != 0 {
                        return Some(Op::Goto(*o));
                    } else {
                        return Some(Op::Nop());
                    }
                }
            }
            Op::Bez(cond, o) => {
                if let Some(x) = self.operand_value(*cond) {
                    if x == 0 {
                        return Some(Op::Goto(*o));
                    } else {
                        return Some(Op::Nop());
                    }
                }
            }
            Op::Slt(_, _, _) => {}
            Op::Seq(_, _, _) => {}
            Op::SetRelative(o) => {
                if let Some(0) = self.operand_value(*o) {
                    return Some(Op::Nop());
                }
            }
            _ => {}
        }
        None
    }

    fn simplify(&mut self) {
        for i in 0..self.insn.len() {
            if let Some(n) = self.simplify_insn(&self.insn[i]) {
                self.insn[i] = n;
            }
        }
    }

    pub fn dump_operand(&self, x: &Operand, pc: usize) -> String {
        let s = match x {
            Operand::Position(p) => format!("m[{}]", p),
            Operand::Imm(i) => format!("{}", i),
            Operand::Relative(o) => format!("m[{}]", pp_sp_offset(*o)),
        };
        let pc_i64 = pc as i64;
        if self.modified.contains(&pc_i64) {
            format!("{}", (&s[..]).on_blue())
        } else {
            s
        }
    }

    pub fn dump_insn(&self, op: &Op, pc: usize) -> String {
        let pp_operand =
            |x: &Operand, offset: usize| -> String { self.dump_operand(x, pc + offset + 1) };
        match op {
            Op::Add(x, y, o) => format!(
                "{:10} <- {:5} + {:5}",
                pp_operand(o, 0),
                pp_operand(x, 1),
                pp_operand(y, 2)
            ),
            Op::Mul(x, y, o) => format!(
                "{:10} <- {:5} * {:5}",
                pp_operand(o, 0),
                pp_operand(x, 1),
                pp_operand(y, 2)
            ),
            Op::Input(o) => format!("{:10} <- {}", pp_operand(o, 0), "INPUT".magenta()),
            Op::Output(s) => format!("{} {}", "OUTPUT".red(), pp_operand(s, 0)),
            Op::Bnz(x, off) => format!(
                "{} {}, {}",
                "bnz".bright_green(),
                pp_operand(x, 0),
                pp_operand(off, 1)
            ),
            Op::Bez(x, off) => format!(
                "{} {}, {}",
                "bez".bright_green(),
                pp_operand(x, 0),
                pp_operand(off, 1)
            ),
            Op::Slt(x, y, o) => format!(
                "{:10} <- {:5} < {:5}",
                pp_operand(o, 0),
                pp_operand(x, 1),
                pp_operand(y, 2)
            ),
            Op::Seq(x, y, o) => format!(
                "{:10} <- {:5} == {:5}",
                pp_operand(o, 0),
                pp_operand(x, 1),
                pp_operand(y, 2)
            ),
            Op::SetRelative(off) => format!("{:10} <- sp + {}", "sp", pp_operand(off, 0)),
            Op::Halt => format!("halt"),
            Op::Raw(value) => format!("[{}]", value),
            Op::Nop() => format!("nop"),
            Op::LoadImm(o, imm) => format!("{:10} <- {}", pp_operand(o, 0), imm),
            Op::Copy(o, x) => format!("{:10} <- {}", pp_operand(o, 0), pp_operand(o, 1)),
            Op::Goto(o) => format!("{} {}", "goto".bright_green(), pp_operand(o, 1)),
        }
    }

    pub fn dump(&self) {
        println!("Tape.size = {}\n", self.tape.len());
        for (op, pc) in self.insn.iter().zip(&self.offset) {
            if self.entries.contains(&(*pc as i64)) {
                println!("");
            }
            println!("  {:6}:   {}", pc, self.dump_insn(op, *pc));
        }
    }
}

pub fn disasm(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    let mut d = Disassembler::disassemble(&tape[..]);
    d.analyze_modified();
    d.analyze_branch();
    d.simplify();
    d.dump();
    Ok(())
}
