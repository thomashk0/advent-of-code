use aoc::intcode::{HaltCause, IntCpu};
use std::slice;

fn cause_id(cause: HaltCause) -> i32 {
    match cause {
        HaltCause::Exit => 1,
        HaltCause::InvalidPc => 2,
        HaltCause::MemoryError(_, _) => 3,
        HaltCause::DecodeError(_) => 4,
        HaltCause::NoMoreInput => 5,
    }
}

#[no_mangle]
pub extern "C" fn icpu_create() -> *mut IntCpu {
    let cpu = IntCpu::from_tape(&[]);
    Box::into_raw(Box::new(cpu))
}

#[no_mangle]
pub unsafe extern "C" fn icpu_clone(ptr: *mut IntCpu) -> *mut IntCpu {
    let other = &mut *ptr;
    let cpu = other.clone();
    Box::into_raw(Box::new(cpu))
}

#[no_mangle]
pub unsafe extern "C" fn icpu_reset(ptr: *mut IntCpu) {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    cpu.reset();
}

#[no_mangle]
pub unsafe extern "C" fn icpu_load_tape(ptr: *mut IntCpu, data: *const i64, len: usize) {
    let tape = slice::from_raw_parts(data, len);
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    cpu.reset_tape(tape);
}

#[no_mangle]
pub unsafe extern "C" fn icpu_pending_output(ptr: *const IntCpu) -> usize {
    assert!(!ptr.is_null());
    let cpu = &*ptr;
    cpu.pending_output()
}

#[no_mangle]
pub unsafe extern "C" fn icpu_pending_input(ptr: *const IntCpu) -> usize {
    assert!(!ptr.is_null());
    let cpu = &*ptr;
    cpu.pending_input()
}

#[no_mangle]
pub unsafe extern "C" fn icpu_pop_output(ptr: *mut IntCpu, dst: *mut i64) -> bool {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    if let Some(x) = cpu.pop_output() {
        *dst = x;
        return true;
    }
    return false;
}

#[no_mangle]
pub unsafe extern "C" fn icpu_add_input(ptr: *mut IntCpu, input: i64) {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    cpu.add_input(input);
}

#[no_mangle]
pub unsafe extern "C" fn icpu_mem_write(ptr: *mut IntCpu, addr: i64, value: i64) -> i32 {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    match cpu.tape_write(addr, value) {
        Err(e) => cause_id(e),
        Ok(_) => 0,
    }
}

#[no_mangle]
pub unsafe extern "C" fn icpu_mem_read(ptr: *const IntCpu, addr: i64, value: *mut i64) -> i32 {
    assert!(!ptr.is_null());
    let cpu = &*ptr;
    match cpu.tape_read(addr) {
        Err(e) => cause_id(e),
        Ok(v) => {
            *value = v;
            0
        }
    }
}

#[no_mangle]
pub unsafe extern "C" fn icpu_dump(ptr: *const IntCpu) {
    assert!(!ptr.is_null());
    let cpu = &*ptr;
    cpu.dump();
}

#[no_mangle]
pub unsafe extern "C" fn icpu_step(ptr: *mut IntCpu) -> i32 {
    assert!(!ptr.is_null());
    let cpu_ref = &mut *ptr;
    let halted = cpu_ref.step();
    if !halted {
        return 0;
    }
    cause_id(cpu_ref.cause().unwrap())
}

#[no_mangle]
pub unsafe extern "C" fn icpu_run(ptr: *mut IntCpu) -> i32 {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    while !cpu.step() {}
    match cpu.cause() {
        Some(e) => cause_id(e),
        _ => 0,
    }
}

#[no_mangle]
pub unsafe extern "C" fn icpu_resume(ptr: *mut IntCpu) {
    assert!(!ptr.is_null());
    let cpu = &mut *ptr;
    cpu.resume();
}

#[no_mangle]
pub unsafe extern "C" fn icpu_destroy(p: *mut IntCpu) {
    if p.is_null() {
        return;
    }
    Box::from_raw(p);
}
