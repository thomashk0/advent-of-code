import copy
import itertools


def load_program(s):
    return dict(enumerate(map(int, s.split(','))))


def draw(tape):
    n = max(tape.keys()) + 1
    return ",".join(str(tape.get(i)) for i in range(n))


def run_and_draw(s):
    return draw(run(load_program(s))[1])


def run(tape):
    pc = 0
    while True:
        op = tape[pc]
        if op == 99:
            return pc, tape
        arg_1, arg_2, arg_3 = tape[pc + 1], tape[pc + 2], tape[pc + 3]
        op_1 = tape.get(arg_1, 0)
        op_2 = tape.get(arg_2, 0)
        if op == 1:
            tape[arg_3] = op_1 + op_2
        elif op == 2:
            tape[arg_3] = op_1 * op_2
        else:
            raise Exception(f"invalid opcode {op} (pc = {pc})")
        pc += 4


def main():
    # print(draw(load_program("1,0,0,0,99")))
    assert run_and_draw("1,0,0,0,99") == "2,0,0,0,99"
    assert run_and_draw("2,4,4,5,99,0") == "2,4,4,5,99,9801"
    assert run_and_draw("1,1,1,4,99,5,6,0,99") == "30,1,1,4,2,5,6,0,99"
    src = None
    with open('assets/day2-input') as f:
        src = load_program(f.readline().strip())
        tape = copy.copy(src)
        tape[1] = 12
        tape[2] = 2
        print("part 1:", run(tape)[1][0])

    for verb, noun in itertools.product(range(0, 100), range(0, 100)):
        tape = copy.copy(src)
        tape[1] = verb
        tape[2] = noun
        if run(tape)[1][0] == 19690720:
            print("part 2:", 100 * verb + noun)


if __name__ == '__main__':
    main()
