use crate::intcode::{Op, Operand};

/// Disassembling framework for IntCode

pub fn pp_sp_offset(o: i64) -> String {
    if o == 0 {
        format!("sp")
    } else {
        format!("sp {} {}", if o > 0 { "+" } else { "-" }, o.abs())
    }
}

pub fn pp_operand(x: &Operand) -> String {
    match x {
        Operand::Position(p) => format!("mem[{}]", p),
        Operand::Imm(i) => format!("{}", i),
        Operand::Relative(o) => format!("mem[{}]", pp_sp_offset(*o)),
    }
}

pub fn pp_op(op: &Op) -> String {
    match op {
        Op::Add(x, y, o) => format!(
            "{:10} <- {:5} + {:5}",
            pp_operand(o),
            pp_operand(x),
            pp_operand(y)
        ),
        Op::Mul(x, y, o) => format!(
            "{:10} <- {:5} * {:5}",
            pp_operand(o),
            pp_operand(x),
            pp_operand(y)
        ),
        Op::Input(o) => format!("{:10} <- read", pp_operand(o)),
        Op::Output(s) => format!("write {}", pp_operand(s)),
        Op::Bnz(x, off) => format!("bnz {}, {}", pp_operand(x), pp_operand(off)),
        Op::Bez(x, off) => format!("bez {}, {}", pp_operand(x), pp_operand(off)),
        Op::Slt(x, y, o) => format!(
            "{:10} <- {:5} < {:5}",
            pp_operand(o),
            pp_operand(x),
            pp_operand(y)
        ),
        Op::Seq(x, y, o) => format!(
            "{:10} <- {:5} == {:5}",
            pp_operand(o),
            pp_operand(x),
            pp_operand(y)
        ),
        Op::SetRelative(off) => format!("{:10} <- sp + {}", "sp", pp_operand(off)),
        Op::Halt => format!("halt"),
        Op::Raw(value) => format!("[{:5}]", value),
    }
}

struct Disassembler<'a> {
    tape: &'a [i64],
    pc: usize,
}

impl<'a> Disassembler<'a> {
    fn new(tape: &'a [i64]) -> Self {
        Disassembler { tape, pc: 0 }
    }
}

impl Iterator for Disassembler<'_> {
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
                Some((1, Op::Raw(self.tape[pc])))
            }
        }
    }
}

//#[derive(Debug, Default)]
//pub struct Context {
//    sp_in: Option<i64>,
//}
//
//impl Context {
//    //    fn analyze_modified(&mut self, tape: &[i64]) {
//    //        for (_, insn) in Disassembler::new(tape) {
//    //            match insn.get_output_operand() {
//    //                Some(Operand::Position(o)) => {
//    //                    self.modified.insert(o);
//    //                }
//    //                _ => {}
//    //            }
//    //        }
//    //    }
//    //
//    //    fn operand_value(&self, o: Operand, tape: &[i64]) -> Option<i64> {
//    //        match o {
//    //            Operand::Position(p) => {
//    //                if !self.modified.contains(&p) {
//    //                    Some(tape[p as usize])
//    //                } else {
//    //                    None
//    //                }
//    //            }
//    //            Operand::Imm(i) => Some(i),
//    //            _ => None,
//    //        }
//    //    }
//    //
//    //    fn analyze_branch(&mut self, tape: &[i64]) {
//    //        for (_, insn) in Disassembler::new(tape) {
//    //            let v = match insn {
//    //                Op::Bnz(_, o) => self.operand_value(o, tape),
//    //                Op::Bez(_, o) => self.operand_value(o, tape),
//    //                _ => None,
//    //            };
//    //            v.map(|i| {
//    //                self.branch_entries.insert(i);
//    //            });
//    //        }
//    //    }
//}
//
//struct InsnBlock {
//    tape: Vec<i64>,
//    insn: Vec<Op>,
//    offset: Vec<usize>,
//    context: Context,
//}
//
//impl InsnBlock {
//    pub fn disassemble(tape: &[i64], context: Context) -> Self {
//        let c = tape.len() / 2;
//        let mut b = InsnBlock {
//            tape: tape.iter().cloned().collect(),
//            insn: Vec::with_capacity(c),
//            offset: Vec::with_capacity(c),
//            context,
//        };
//        for (pc, op) in Disassembler::new(&tape) {
//            b.insn.push(op);
//            b.offset.push(pc);
//            if op.is_branch() {
//                break;
//            }
//        }
//        b
//    }
//
//    fn operand_value(&self, o: Operand, tape: &[i64]) -> Option<i64> {
//        match o {
//            Operand::Position(p) => {
//                if !self.context.modified.contains(&p) {
//                    Some(tape[p as usize])
//                } else {
//                    None
//                }
//            }
//            Operand::Imm(i) => Some(i),
//            _ => None,
//        }
//    }
//
//    pub fn dump(&self) {
//        for (op, pc) in self.insn.iter().zip(&self.offset) {
//            println!("    {:3}: {}", pc, pp_op(op));
//        }
//    }
//}
//
//pub fn disassemble(tape: &[i64]) {
//    let mut info = Context::default();
//
//    //    info.analyze_modified(&tape);
//    //    info.analyze_branch(&tape);
//    let mut b = InsnBlock::disassemble(&tape, info);
//    b.dump();
//
//    //    let mut pc = 0;
//    //    loop {
//    //        let pci = pc as i64;
//    //        if info.branch_entries.contains(&pci) {
//    //            println!("\n~~~>")
//    //        }
//    //        match Op::decode(&tape[pc..]) {
//    //            Ok((inc, op)) => {
//    //                println!("    {:3}: {}", pc, pp_op(&op)); // &tape[pc..(pc + inc)]
//    //                pc += inc;
//    //            }
//    //            Err(e) => {
//    //                println!("    {:3}: {} ({:?}) ", pc, tape[pc], e);
//    //                pc += 1;
//    //            }
//    //        }
//    //        if pc >= tape.len() {
//    //            break;
//    //        }
//    //    }
//}
