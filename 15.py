import math
from functools import lru_cache
from heapq import *
from typing import Dict, Tuple

with open("input/15.txt") as handle:
    risk = [[int(r) for r in line.rstrip()] for line in handle.readlines()]


def part_one(risk):
    width = len(risk[0])
    height = len(risk)

    @lru_cache
    def inner(x, y):
        if y == height - 1 and x == width - 1:
            return risk[-1][-1]

        right = inner(x + 1, y) if x + 1 < width else math.inf
        down = inner(x, y + 1) if y + 1 < height else math.inf

        return risk[y][x] + min(right, down)

    return inner(0, 0) - risk[0][0]


def part_two(risk):
    width = len(risk[0])
    height = len(risk)

    def get_risk(x, y):
        x_quotient, x_remainder = divmod(x, width)
        y_quotient, y_remainder = divmod(y, height)

        return (risk[y_remainder][x_remainder] + x_quotient + y_quotient) % 9 or 9

    heap = []
    distances: Dict[Tuple[int, int], int] = {(0, 0): 0}

    for x in range(5 * width):
        for y in range(5 * width):
            if (x, y) != (0, 0):
                distances[(x, y)] = 1000000000
            heappush(heap, (distances[(x, y)], (x, y)))

    while heap:
        dist, (x, y) = heappop(heap)

        if dist > distances[(x, y)]:
            continue

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if 0 <= x + dx < 5 * width and 0 <= y + dy < 5 * width:
                new_dist = get_risk(x + dx, y + dy) + distances[(x, y)]
                if new_dist < distances[(x + dx, y + dy)]:
                    distances[(x + dx, y + dy)] = new_dist
                    heappush(heap, (new_dist, (x + dx, y + dy)))

    return distances[(5 * width - 1, 5 * height - 1)]


print(part_one(risk))
print(part_two(risk))
