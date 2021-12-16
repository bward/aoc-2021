from typing import List, Tuple, Set


with open("input/11.txt") as handle:
    levels = [[int(l) for l in line.rstrip()] for line in handle.readlines()]


def increment(levels: List[List[int]]) -> List[List[int]]:
    return [[x + 1 for x in row] for row in levels]


def show(levels: List[List[int]]):
    for row in levels:
        print("".join(str(d) for d in row))
    print()


def flash(
    levels: List[List[int]], flashed: Set[Tuple[int, int]]
) -> Tuple[List[List[int]], Set[Tuple[int, int]]]:
    for y in range(len(levels)):
        for x in range(len(levels[0])):
            if levels[y][x] > 9:
                flashed.add((y, x))
                for (dy, dx) in [
                    (1, 0),
                    (0, 1),
                    (-1, 0),
                    (0, -1),
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1),
                ]:
                    if 0 <= y + dy < len(levels) and 0 <= x + dx < len(levels[0]):
                        levels[y + dy][x + dx] += 1

    for (y, x) in flashed:
        levels[y][x] = 0

    return levels, flashed


total_flashes = 0

for step in range(500):
    levels = increment(levels)
    flashed = set()
    while any(x > 9 for row in levels for x in row):
        levels, flashed = flash(levels, flashed)

    total_flashes += len(flashed)
    print(total_flashes)

    if len(flashed) == 100:
        print("All flashed on", step + 1)
        break
