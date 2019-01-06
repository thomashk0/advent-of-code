use std::io;

const W: usize = 300;
const SERIAL: i32 = 2568;

fn solve(n: usize, power_map: &[i32]) -> ((usize, usize), i32) {
    let score = |coords: (usize, usize)| -> i32 {
        let (x, y) = coords;
        let mut tot = 0;
        for dy in 0..n {
            for dx in 0..n {
                tot += power_map[(y + dy) * W + (x + dx)];
            }
        }
        tot
    };
    itertools::iproduct!(0..W - n, 0..W - n)
        .map(|coords| (coords, score(coords)))
        .max_by_key(|x| x.1)
        .unwrap()
}

pub fn run() -> io::Result<()> {
    let power_map: Vec<i32> = (0..((W as i32) * (W as i32)))
        .map(|id| {
            let x = (id % (W as i32)) + 1;
            let y = (id / (W as i32)) + 1;
            let rack_id = x + 10;
            (((((rack_id * y) + SERIAL) * rack_id) / 100) % 10) - 5
        })
        .collect();

    {
        let ((x, y), _) = solve(3, &power_map);
        println!("Part 1: {},{}", x + 1, y + 1);
    }
    // Quite inefficient, lucky the answer lies in small n values, could be drastically improved
    // by combining summed squared into bigger ones.
    {
        let ((x, y, n), _) = (3..50).map(|i| {
            let ((x, y), score) = solve(i, &power_map);
            ((x, y, i), score)
        }).max_by_key(|x| x.1).unwrap();
        println!("Part 2: {},{},{}", x + 1, y + 1, n);
    }

    Ok(())
}