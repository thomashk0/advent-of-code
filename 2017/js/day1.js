'use strict';

const fs = require('fs');
const assert = require('assert').strict;

function compute_captcha_func(seq, step) {
    return seq
        .split('')
        .map((el, i, arr) => (el === arr[(i + step) % arr.length])? el: 0)
        .reduce((a, x) => a + +x, 0);
}

// Test cases
assert.equal(compute_captcha_func("1122", 1), 3);
assert.equal(compute_captcha_func("91212129", 1), 9);

let input = fs.readFileSync('assets/day1-input', 'utf-8').trim();

const aoc_solve = [
    (input) => compute_captcha_func(input, 1),
    (input) => compute_captcha_func(input, input.length / 2)];

aoc_solve.forEach((solver, i) => {
    let start = process.hrtime();
    let r = solver(input);
    let elapsed = process.hrtime(start);
    console.log(`part ${i}:`, r, `(elapsed=${elapsed})`);
});
