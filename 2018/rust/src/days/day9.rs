use std::io;
use std::iter;
use std::collections::HashMap;

#[derive(Debug)]
struct CircularBuffer
{
    pred : HashMap<i32, i32>,
    succ : HashMap<i32, i32>
}

impl CircularBuffer
{
    pub fn new(elt : i32) -> CircularBuffer {
        let m : HashMap<i32, i32> = [(elt, elt)].iter().cloned().collect();
        CircularBuffer {
            pred: m.clone(),
            succ: m
        }
    }

    pub fn insert_after(&mut self, el : i32, v : i32) {
        let s : i32 = self.succ[&el];
        self.succ.insert(el, v);
        self.succ.insert(v, s);
        self.pred.insert(v, el);
        self.pred.insert(s, v);
    }

    pub fn remove(&mut self, el : i32) -> i32 {
        let succ : i32 = self.succ[&el];
        let pred : i32 = self.pred[&el];
        self.pred.insert(succ, pred);
        self.succ.insert(pred, succ);
        self.succ.remove(&el);
        self.pred.remove(&el);
        succ
    }

    pub fn left(&self, x : i32) -> Option<i32> {
        self.pred.get(&x).cloned()
    }

    pub fn left_n(&self, x : i32, n : usize) -> i32 {
        let mut loc = x;
        for _ in 0..n {
            loc = self.left(loc).unwrap();
        }
        loc
    }

    pub fn right(&self, x : i32) -> Option<i32> {
        self.succ.get(&x).cloned()
    }
}

#[derive(Debug)]
struct State {
    current_player: i32,
    head: i32, // The marble we insert after
    max_marbles : i32,
    num_players : i32,
    scores : Vec<i64>,
    marbles : CircularBuffer
}

impl State {
    pub fn new(n: i32, p: i32) -> State {
        let mut m = HashMap::with_capacity(1024);
        m.insert(0, 0);
        State {
            current_player: 0,
            head: 0,
            max_marbles: p,
            num_players: n,
            scores: iter::repeat(0).take(n as usize).collect(),
            marbles: CircularBuffer::new(0)
        }
    }
}

fn solve(n: i32, p: i32) -> i64 {
    let mut s = State::new(n, p);
    for marble in 1..=p {
        if marble % 23 == 0 {
            s.scores[s.current_player as usize] += i64::from(marble);
            let j = s.marbles.left_n(s.head, 7);
            s.scores[s.current_player as usize] += i64::from(j);
            s.head = s.marbles.remove(j);
        } else {
            s.marbles.insert_after(s.marbles.right(s.head).unwrap(), marble);
            s.head = marble;
        }
        s.current_player = (s.current_player + 1) % s.num_players;
    }
    *s.scores.iter().max().unwrap()
}

pub fn run() -> io::Result<()> {
    let (n, p) = {
        match scanln_fmt!("{d} players; last marble is worth {d} points", i32, i32) {
            (Some(n), Some(p)) => Ok((n, p)),
            _ => Err("Unable to parse input")
        }
    }.unwrap();
    println!("Part 1: {}", solve(n, p));
    println!("Part 2: {}", solve(n, p * 100));
    Ok(())
}


