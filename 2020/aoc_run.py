import argparse


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-c', '--check')
    parser.add_argument('-i', '--input', help="input file to supply")
    parser.add_argument('day')
    args = parser.parse_args()

    m = __import__(args.day)
    if args.input:
        m.aoc_run(args.input)
    else:
        m.aoc_run()


if __name__ == '__main__':
    main()
