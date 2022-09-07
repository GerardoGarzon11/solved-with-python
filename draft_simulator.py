# TODO: add input validator
# TODO: FIX some names, add more names
# TODO: Change Defense codes
# TODO: Add K?

from collections import OrderedDict
import re

HEADER = "Pos,Player,FPS"

players = {
    "QB": OrderedDict(),
    "RB": OrderedDict(),
    "WR": OrderedDict(),
    "TE": OrderedDict(),
    "D": OrderedDict(),
}

counters = {
    "QB": 0,
    "RB": 0,
    "WR": 0,
    "TE": 0,
    "D": 0,
}


def insert_player(line: str) -> None:
    split_line = line.split(",")
    position = split_line[0]
    name = split_line[1]
    fps = float(split_line[2])
    code = split_line[4].strip()

    counters[position] += 1

    if "QB" in position:
        pct = ((counters[position] / 67) * 100) // 1
    elif "WR" in position or "RB" in position:
        pct = ((counters[position] / 108) * 100) // 1
    elif "TE" in position:
        pct = ((counters[position] / 90) * 100) // 1
    else:
        pct = ((counters[position] / 32) * 100) // 1

    if code not in players[position]:
        players[position][code] = {"name": name, "fps": fps, "pct": pct}
    else:
        print("error, code already exists" + code)


def format_print_name(to_print: str) -> str:
    str_length = len(to_print)
    if str_length > 20:
        return to_print[:20]

    return to_print + (" " * (20 - str_length))


def calc_pct(position):
    # TODO: 16 - change the number of turns to "wait"
    count = 0
    max_ = max(15, len(list(players[position].items())))
    for item in players[position].items():
        if count == 0:
            first = item[1]

        last = item[1]

        count += 1

        if count > 15:
            break
    return (((last["fps"] / first["fps"]) * 100) // 1, first["pct"])


def get_best_picks() -> None:
    print("Player and %")
    # how many of each position do we think will be picked in the next rounds
    for key in players.keys():
        pct, top = calc_pct(key)
        print(f"{key}\t{format_print_name(next(iter(players[key])))}\n\t{top}\t{pct}\n")


def make_pick(position: str, pick: str) -> None:
    pick = pick.upper()
    position = position.upper()

    if not pick:
        pick = next(iter(players[position]))

    print(f"Picked: {pick}")

    if pick in players[position]:
        del players[position][pick]
    else:
        print("Pick not found, it might not exist. Please try again if you want to.")


def check_input(pick: str) -> bool:
    pick = pick.upper()
    if pick.startswith("D "):
        p = re.compile("[D]\s[A-Z]")
        if p.match(pick):
            return True
    else:
        p = re.compile("[A-Z]+\s[A-Z]+\s[A-Z]\s[A-Z]+")
        if p.match(pick):
            # check positions
            if pick.split()[1] in players.keys():
                return True

    return False


# load data
with open("NFL2.csv", "r") as f:
    data = f.readlines()
    for line in data:
        if HEADER not in line:  # First
            insert_player(line)

while True:

    # present options
    print("Best possible picks for each position")
    get_best_picks()

    pick = input("Please make your selection: ")

    if check_input(pick):

        if pick.startswith("D "):  # defensive pick
            make_pick("D", pick)
        else:
            split_pick = pick.split()
            make_pick(split_pick[1], pick)

    else:
        print("Input format is not correct")
