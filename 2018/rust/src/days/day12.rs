use std::io;
use std::io::prelude::*;
use std::collections::HashMap;

const EMPTY : u8 = '.' as u8;
const FLOWER : u8 = '#' as u8;
const W : i32 = 2;

pub fn slice_at(i: i32, data: &[u8], dst: &mut [u8]) {
    for j in 0..5 {
        let idx = i + j - W;
        if idx >= 0 && idx < (data.len() as i32) {
            dst[j as usize] = data[idx as usize];
        } else {
            dst[j as usize] = EMPTY;
        }
    }
}

pub fn step(rules: &HashMap<Vec<u8>, u8>, data: &[u8], dst: &mut Vec<u8>) -> i32 {
    let mut tmp = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY];
    let mut min_match : Option<i32> = None;
    dst.clear();
    for offset in -W..=(data.len() as i32) + W {
        slice_at(offset, &data, &mut tmp[0..]);
        let new_val =
            if let Some(&u) = rules.get(&mut tmp[0..]) {
                u
            } else {
                tmp[2]
            };
        if min_match.is_none() && new_val == FLOWER {
            min_match = Some(offset);
        }
        if min_match.is_some() {
            dst.push(new_val);
        }
    }
    let cut : usize =
        dst.iter().rev().take_while(|&&x| {x == EMPTY}).count();
    dst.resize(dst.len() - cut, EMPTY);
    min_match.unwrap()
}

pub fn score(v : &[u8], start_offset: i32) -> i32 {
    (start_offset..).zip(v.iter()).filter_map(|(i, &x)| {
        if x == FLOWER {
            Some(i)
        } else {
            None
        }
    }).sum()
}

pub fn arith_progression(v : &[i32]) -> Option<i32> {
    if v.len() <= 2 { return None; }

    if v.iter().zip(v[1..].iter()).map(|(x, y)| {y - x}).all(|x| x == (v[1] - v[0])) {
        Some(v[1] - v[0])
    } else {
        None
    }
}

pub fn run() -> io::Result<()> {
    let mut buff = String::with_capacity(1024);
    let input: String = {
        io::stdin().read_line(&mut buff)?;
        format!("{}", buff.split(": ").nth(1).unwrap().trim())
    };
    io::stdin().read_line(&mut buff)?;

    let mut rules : HashMap<Vec<u8>, u8> = HashMap::with_capacity(128);
    for line in io::stdin().lock().lines() {
        let l = line.unwrap();
        let v : Vec<&str> = l.split(" => ").collect();
        rules.insert(v[0].as_bytes().iter().cloned().collect(),
                     v[1].as_bytes().iter().cloned().next().unwrap());
    }

    let mut bytes = input.into_bytes();
    let mut tmp: Vec<u8> = Vec::with_capacity(bytes.len());
    let mut shift_left: i32 = 0;
    let mut part_1 = 0;
    let mut part_2 = 0;
    let mut scores : Vec<i32> = Vec::with_capacity(1024);
    for i in 1..=100 {
        shift_left += step(&rules, &bytes, &mut tmp);
        std::mem::swap(&mut bytes, &mut tmp);
        let s = score(&bytes, shift_left);
        if i == 20 {
            part_1 = s;
        }
        scores.push(s);
        if let Some(q) = arith_progression(&scores) {
            println!("Loop found i={} q={}", i, q);
            part_2 =  (50000000000 - i as i64) * (q as i64) + s as i64;

            break;
        }
        if scores.len() > 4 {
            scores.drain(0..1);
        }
        // println!("{} {} {}", i, shift_left, s);
    }
    println!("Part 1: {}", part_1);
    println!("Part 2: {}", part_2);
    Ok(())
}

