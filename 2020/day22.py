from copy import copy, deepcopy


def score(deck):
    return sum(c * i for c, i in zip(deck, reversed(range(len(deck) + 1))))


def serialize(decks):
    p_0, p_1 = decks
    p_0 = ','.join(map(str, p_0))
    p_1 = ','.join(map(str, p_1))
    return f"{p_0}|{p_1}"


def parse(lines):
    import re
    PLAYER_RE = re.compile("Player (\d+):")

    players = {}
    while lines:
        player_id = int(PLAYER_RE.match(lines[0]).group(1))
        lines = lines[1:]
        cards = []
        while True:
            if not lines or len(lines[0].strip()) == 0:
                players[player_id] = cards
                lines = lines[1:]
                break
            cards.append(int(lines[0]))
            lines = lines[1:]
    return players


def play(decks):
    p0_deck, p1_deck = decks
    while True:
        if len(p0_deck) == 0:
            return 1, p1_deck
        if len(p1_deck) == 0:
            return 0, p0_deck

        p0_card = p0_deck.pop(0)
        p1_card = p1_deck.pop(0)
        if p0_card > p1_card:
            p0_deck.append(p0_card)
            p0_deck.append(p1_card)
        else:
            # p1_card > p0_card
            p1_deck.append(p1_card)
            p1_deck.append(p0_card)


def play_rec(decks):
    p0_deck, p1_deck = decks
    known_config = set()
    while True:
        cfg = serialize((p0_deck, p1_deck))
        if cfg in known_config:
            return 0, copy(p0_deck)
        known_config.add(cfg)

        p0_card = p0_deck.pop(0)
        p1_card = p1_deck.pop(0)
        if len(p0_deck) >= p0_card and len(p1_deck) >= p1_card:
            new_deck = copy(p0_deck[:p0_card]), copy(p1_deck[:p1_card])
            winner, w_deck = play_rec(new_deck)
        else:
            if p0_card > p1_card:
                winner = 0
            else:
                winner = 1
        if winner == 0:
            p0_deck.append(p0_card)
            p0_deck.append(p1_card)
        else:
            p1_deck.append(p1_card)
            p1_deck.append(p0_card)

        if len(p0_deck) == 0:
            return 1, copy(p1_deck)
        elif len(p1_deck) == 0:
            return 0, copy(p0_deck)


def aoc_run(input_path):
    lines = list(open(input_path))
    player_decks = parse(lines)
    decks = player_decks[1], player_decks[2]
    winner, final_deck = play(deepcopy(decks))
    print("part 1:", score(final_deck))

    winner, final_deck = play_rec(decks)
    print("part 2:", score(final_deck))


if __name__ == '__main__':
    aoc_run('assets/day22-input-1')
