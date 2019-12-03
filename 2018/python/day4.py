import collections
import datetime
import re
import sys
import pprint


def main():
    regex = re.compile("\[([0-9\-: ]*)\] (.*)")
    log = []
    for l in sys.stdin:
        date_str, action = tuple(regex.match(l.strip()).groups())
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        minutes = int(date_str.split(':')[1])
        log.append((date, minutes, action))
    log.sort(key=lambda k: k[0])

    asleep = {}
    asleep_count = {}
    asleep_max = {}
    current = None
    for date, minutes, action in log:
        ws = action.split()
        if ws[0] == 'falls':
            asleep[current] = minutes
        elif ws[0] == 'wakes':
            if current not in asleep:
                continue
            start = asleep[current]
            elapsed = minutes - start
            if elapsed < 0:
                raise Exception("WTF")
            cnt = asleep_max.get(current, collections.Counter())
            cnt.update(list(range(start, minutes)))
            asleep_max[current] = cnt
            asleep_count[current] = asleep_count.get(current, 0) + elapsed
            del asleep[current]
        elif ws[0] == 'Guard':
            current = int(ws[1][1:])
            asleep.clear()
        else:
            raise NotImplementedError()

    best_id, _ = max(asleep_count.items(), key=lambda k: k[1])
    best_min, _ = asleep_max[best_id].most_common(1)[0]
    print("Part 1:", best_id * best_min)
    bests = [(gid, cnt.most_common(1)[0]) for gid, cnt in asleep_max.items()]
    best_id_2, (best_min_2, _) = max(bests, key=lambda k: k[1][1])
    print("Part 2:", best_id_2 * best_min_2)


if __name__ == '__main__':
    main()
