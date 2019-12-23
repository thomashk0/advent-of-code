/// Disassembling framework for IntCode
use crate::intcode::{from_bool, load_tape, Op, Operand};
use colored::Colorize;
use std::collections::{HashMap, HashSet};
use std::io;

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
    type Item = (usize, usize, Op);

    fn next(&mut self) -> Option<Self::Item> {
        if self.pc >= self.tape.len() {
            return None;
        }
        let pc = self.pc;
        let op = Op::decode(&self.tape[self.pc..]);
        match op {
            Ok((inc, op)) => {
                self.pc += inc;
                Some((pc, inc, op))
            }
            Err(_) => {
                self.pc += 1;
                Some((pc, 1, Op::Raw(self.tape[pc])))
            }
        }
    }
}

fn disassemble(tape: &[i64]) -> IntCodeIt {
    IntCodeIt::new(tape)
}

#[derive(Debug, Clone, Copy)]
pub enum BinOp {
    Add,
    Mul,
    Slt,
    Seq,
}

#[derive(Debug, Clone, Copy)]
pub enum BranchCond {
    Bez,
    Bnz,
}

#[derive(Debug, Clone, Copy)]
pub enum AsmInsn {
    BinOp(BinOp, Operand, Operand, Operand),
    Branch(BranchCond, Operand, Operand),
    Input(Operand),
    Output(Operand),
    SetRelative(Operand),
    Halt,
    Goto(Operand),
    Data(i64),
    Load(Operand, Operand),
    Nop,
}

impl From<Op> for AsmInsn {
    fn from(op: Op) -> Self {
        match op {
            Op::Add(x, y, o) => AsmInsn::BinOp(BinOp::Add, x, y, o),
            Op::Mul(x, y, o) => AsmInsn::BinOp(BinOp::Mul, x, y, o),
            Op::Input(o) => AsmInsn::Input(o),
            Op::Output(o) => AsmInsn::Output(o),
            Op::Bnz(x, o) => AsmInsn::Branch(BranchCond::Bnz, x, o),
            Op::Bez(x, o) => AsmInsn::Branch(BranchCond::Bez, x, o),
            Op::Slt(x, y, o) => AsmInsn::BinOp(BinOp::Slt, x, y, o),
            Op::Seq(x, y, o) => AsmInsn::BinOp(BinOp::Seq, x, y, o),
            Op::SetRelative(o) => AsmInsn::SetRelative(o),
            Op::Halt => AsmInsn::Halt,
            Op::Raw(v) => AsmInsn::Data(v),
            o => unreachable!("unsupported IntCode instructions {:?}", o),
        }
    }
}

impl AsmInsn {
    pub fn get_operand(&self, idx: usize) -> Option<(bool, Operand)> {
        let is_output = idx == 2;
        match self.clone() {
            AsmInsn::BinOp(_, x, y, o) => [x, y, o].get(idx).map(|w| (is_output, *w)),
            AsmInsn::Branch(_, x, y) => [x, y].get(idx).map(|w| (false, *w)),
            AsmInsn::Input(o) => [o].get(idx).map(|w| (true, *w)),
            AsmInsn::Output(x) | AsmInsn::SetRelative(x) => [x].get(idx).map(|w| (false, *w)),
            _ => None,
        }
    }

    pub fn set_operand(&mut self, idx: usize, value: Operand) {
        let is_output = idx == 0;
        match self {
            AsmInsn::BinOp(_, x, y, o) => match idx {
                0 => *x = value,
                1 => *y = value,
                2 => *o = value,
                _ => {}
            },
            AsmInsn::Branch(_, x, o) => match idx {
                0 => *x = value,
                1 => *o = value,
                _ => {}
            },
            AsmInsn::Input(x) | AsmInsn::Output(x) | AsmInsn::SetRelative(x) => {
                if idx == 0 {
                    *x = value
                }
            }
            _ => {}
        }
    }

    pub fn rewrite_operands(&mut self, offset: usize, ctx: &mut Context) {
        for j in 0..3 {
            let addr = (offset + j + 1) as i64;
            if let Some(value) = ctx.mem_value.get(&addr) {
                self.set_operand(j, *value);
            } else {
                match self.get_operand(j) {
                    Some((false, op)) => {
                        ctx.mem_value.insert(addr, op);
                    }
                    Some((true, op)) => match op {
                        Operand::Position(p) => {
                            let v = Operand::Variable(ctx.add_variable());
                            self.set_operand(j, v);
                            ctx.mem_value.insert(p, v);
                        }
                        _ => {}
                    },
                    _ => {}
                }
            }
        }
    }

    pub fn rewrite_sp_operands(&mut self, ctx: &mut Context) {
        for j in 0..3 {
            match self.get_operand(j) {
                Some((_, Operand::Relative(r))) => {
                    ctx.sp_operand(r).map(|op| {
                        self.set_operand(j, op);
                    });
                }
                _ => {}
            }
        }
    }

    pub fn dump(&self, ctx: &Context) -> String {
        let pp_operand = |op: &Operand| dump_operand(op, ctx);
        match self {
            AsmInsn::BinOp(k, x, y, o) => {
                let op_str = match k {
                    BinOp::Add => "+",
                    BinOp::Mul => "*",
                    BinOp::Slt => "<",
                    BinOp::Seq => "==",
                };
                format!(
                    "{} <- {} {} {}",
                    pp_operand(&o),
                    pp_operand(&x),
                    op_str,
                    pp_operand(&y)
                )
            }
            AsmInsn::Branch(k, x, o) => {
                let cond_str = match k {
                    BranchCond::Bez => "bez",
                    BranchCond::Bnz => "bnz",
                }
                .bright_green();
                format!("{} {} {}", cond_str, pp_operand(&x), pp_operand(&o))
            }
            AsmInsn::Load(o, v) => format!("{} <- {}", pp_operand(o), pp_operand(v)),
            AsmInsn::Goto(o) => format!("{} {}", "goto".bright_green(), pp_operand(&o)),
            AsmInsn::Input(o) => format!("{} <- {}", pp_operand(o), "input".red()),
            AsmInsn::Output(i) => format!("{} {}", "output".red(), pp_operand(i)),
            AsmInsn::SetRelative(o) => format!("{} <- sp + {}", "sp", pp_operand(o)),
            AsmInsn::Halt => format!("halt"),
            AsmInsn::Data(x) => {
                if (*x >= 0i64) && (*x < 128) && (*x != 10) {
                    format!("[{:3}] '{}' ", x, ((*x as u8) as char))
                } else {
                    format!("[{}]", x)
                }
            }
            AsmInsn::Nop => format!("nop"),
        }
    }

    pub fn simplify_binary_with(b: BinOp, x: Operand, y: i64, o: Operand) -> Option<AsmInsn> {
        match b {
            BinOp::Add => {
                if y == 0 {
                    return Some(AsmInsn::Load(o, x));
                }
            }
            BinOp::Mul => {
                if y == 0 {
                    return Some(AsmInsn::Load(o, Operand::Imm(0)));
                } else if y == 1 {
                    return Some(AsmInsn::Load(o, x));
                }
            }
            _ => {}
        };
        None
    }

    pub fn simplify_bop(
        ctx: &Context,
        b: BinOp,
        x: Operand,
        y: Operand,
        o: Operand,
    ) -> Option<AsmInsn> {
        let x_v = ctx.operand_value(&x);
        let y_v = ctx.operand_value(&y);
        match (x_v, y_v) {
            (Some(x), Some(y)) => {
                let r = match b {
                    BinOp::Add => x + y,
                    BinOp::Mul => x * y,
                    BinOp::Slt => from_bool(x < y),
                    BinOp::Seq => from_bool(x == y),
                };
                Some(AsmInsn::Load(o, Operand::Imm(r)))
            }
            (Some(i), _) => AsmInsn::simplify_binary_with(b, y, i, o),
            (_, Some(i)) => AsmInsn::simplify_binary_with(b, x, i, o),
            _ => None,
        }
    }

    pub fn simplify(&mut self, ctx: &Context) -> bool {
        let v = match self.clone() {
            AsmInsn::BinOp(b, x, y, o) => AsmInsn::simplify_bop(&ctx, b, x, y, o),
            AsmInsn::Branch(k, cond, offset) => {
                if let Some(dst) = ctx.operand_value(&cond) {
                    match k {
                        BranchCond::Bez => Some(if dst == 0 {
                            AsmInsn::Goto(offset)
                        } else {
                            AsmInsn::Nop
                        }),
                        BranchCond::Bnz => Some(if dst != 0 {
                            AsmInsn::Goto(offset)
                        } else {
                            AsmInsn::Nop
                        }),
                    }
                } else {
                    None
                }
            }
            _ => None,
        };
        if let Some(replace) = v {
            *self = replace;
            true
        } else {
            false
        }
    }
}

fn dump_operand(x: &Operand, ctx: &Context) -> String {
    match x {
        Operand::Position(p) => format!("m[{}]", p),
        Operand::Imm(i) => format!("{}", i),
        Operand::Relative(o) => format!("m[{}]", dump_offset(*o)),
        Operand::Variable(idx) => ctx
            .var_names
            .get(idx)
            .cloned()
            .unwrap_or(format!("v_{}", idx)),
    }
}

pub fn dump_offset(o: i64) -> String {
    let sp_str = "sp".bright_yellow();
    if o == 0 {
        format!("{}", sp_str)
    } else {
        format!("{} {} {}", sp_str, if o > 0 { "+" } else { "-" }, o.abs())
    }
}

#[derive(Debug, Default)]
pub struct Context {
    mem_value: HashMap<i64, Operand>,
    sp_values: HashMap<i64, Operand>,
    mem_inputs: HashMap<i64, Operand>,
    var_id: usize,
    entries: HashSet<i64>,
    var_names: HashMap<usize, String>,
    sp_value: Option<i64>,
}

impl Context {
    pub fn operand_value(&self, op: &Operand) -> Option<i64> {
        match op {
            Operand::Imm(i) => Some(*i),
            Operand::Position(p) => {
                self.mem_value.get(p).and_then(
                    |w| {
                        if w == op {
                            None
                        } else {
                            self.operand_value(w)
                        }
                    },
                )
            }
            _ => None,
        }
    }

    pub fn sp_operand(&self, offset: i64) -> Option<Operand> {
        self.sp_value
            .and_then(|v| self.sp_values.get(&(v + offset)).cloned())
    }

    pub fn update_sp(&mut self, insn: &AsmInsn) {
        match insn {
            AsmInsn::SetRelative(o) => {
                let v = self.sp_value.clone();
                self.sp_value = v.and_then(|old| self.operand_value(o).map(|value| old + value));
            }
            _ => {}
        }
    }

    pub fn operand_at(&self, addr: i64) -> Option<Operand> {
        self.mem_value.get(&addr).cloned()
    }

    pub fn has_value(&self, v: i64, op: &Operand) -> bool {
        return self.operand_value(op).map_or(false, |w| w == v);
    }

    pub fn add_variable(&mut self) -> usize {
        let v_id = self.var_id;
        self.var_id += 1;
        v_id
    }

    pub fn add_named_variable(&mut self, name: &str) -> usize {
        let v_id = self.add_variable();
        self.var_names.insert(v_id, name.to_string());
        v_id
    }

    pub fn add_sp_ref(&mut self, shift: i64, name: &str) -> usize {
        let v_id = self.add_named_variable(name);
        self.sp_values.insert(shift, Operand::Variable(v_id));
        v_id
    }
}

#[derive(Debug, Default)]
struct InsnBlock {
    data: Vec<i64>,
    insn: Vec<AsmInsn>,
    offset: Vec<usize>,
    successors: Vec<Operand>,
}

impl InsnBlock {
    fn new(tape: &[i64]) -> Self {
        let mut b = InsnBlock::default();
        for (pc, _, op) in disassemble(&tape) {
            b.insn.push(AsmInsn::from(op));
            b.offset.push(pc);
        }
        b
    }

    fn scan(tape: &[i64], offset: usize, ctx: &mut Context) -> (Self, usize) {
        let mut b = InsnBlock::default();
        for (pc, incr, op) in disassemble(&tape) {
            let mut i = AsmInsn::from(op);
            ctx.update_sp(&i);
            i.rewrite_operands(pc + offset, ctx);
            i.rewrite_sp_operands(ctx);
            i.simplify(ctx);
            b.insn.push(i);
            b.offset.push(offset + pc);
            match i {
                AsmInsn::Branch(_, _, dst) => {
                    b.successors.push(dst);
                }
                AsmInsn::Goto(dst) => {
                    b.successors.push(dst);
                    ctx.operand_value(&dst)
                        .map(|target| ctx.entries.insert(target));
                    return (b, pc + incr);
                }
                _ => {}
            }
        }
        (b, tape.len())
    }

    pub fn dump(&self, ctx: &Context) {
        for (pc, insn) in self.offset.iter().zip(&self.insn) {
            if ctx.entries.contains(&(*pc as i64)) {
                println!();
            }
            println!("    {:8}: {}", pc, insn.dump(&ctx));
        }
    }

    pub fn simplify(&mut self, ctx: &Context) {
        self.insn.iter_mut().for_each(|w| {
            w.simplify(ctx);
        });
    }

    pub fn analyze(&self, ctx: &mut Context) {}
}

pub fn disasm(input: &str) -> io::Result<()> {
    let tape = load_tape(input)?;
    {
        let mut d = InsnBlock::new(&tape[..]);
        let ctx = Context::default();
        d.simplify(&ctx);
        d.dump(&ctx);
    }

    println!("~~~~ Scan ~~~~");
    {
        let mut ctx = Context::default();
        ctx.sp_value = Some(0);
        ctx.add_sp_ref(1, "arg_0");
        ctx.add_sp_ref(2, "i");
        ctx.add_sp_ref(3, "n");
        let (mut d, n) = InsnBlock::scan(&tape[1378..], 1378, &mut ctx);
        println!("PC is now at {}", n);
        d.simplify(&ctx);
        d.dump(&ctx);
        println!("{:?}", d.successors);
        println!("{:?}", ctx.mem_value);
    }
    Ok(())
}
