import re
from collections import defaultdict

with open("input/22.txt") as handle:
    matches = [
        re.match(
            r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
        ).groups()
        for line in handle.readlines()
    ]


instructions = [
    (
        m[0] == "on",
        (
            (int(m[1]), int(m[2])),
            (int(m[3]), int(m[4])),
            (int(m[5]), int(m[6])),
        ),
    )
    for m in matches
]


def part_one():
    reactor = defaultdict(bool)

    def restrict(start, end):
        return range(max(start, -50), min(end, 50) + 1)

    for state, (xs, ys, zs) in instructions:
        for x in restrict(*xs):
            for y in restrict(*ys):
                for z in restrict(*zs):
                    reactor[(x, y, z)] = state

    return sum(1 for v in reactor.values() if v)


def part_two():
    def cuboids_overlap(first, second):
        def ranges_overlap(first, second):
            a1, b1 = first
            a2, b2 = second

            return a2 <= b1 <= b2 or a1 <= b2 <= b1

        x1, y1, z1 = first
        x2, y2, z2 = second

        return (
            ranges_overlap(x1, x2) and ranges_overlap(y1, y2) and ranges_overlap(z1, z2)
        )

    def split(main, new):
        x1, y1, z1 = main
        x2, y2, z2 = new

        result = []

        # below
        if z1[0] < z2[0]:
            result.append((x1, y1, (z1[0], z2[0] - 1)))

        # above
        if z1[1] > z2[1]:
            result.append((x1, y1, (z2[1] + 1, z1[1])))

        # left
        if x1[0] < x2[0]:
            result.append(
                ((x1[0], x2[0] - 1), y1, (max(z2[0], z1[0]), min(z1[1], z2[1])))
            )

        # right
        if x1[1] > x2[1]:
            result.append(
                ((x2[1] + 1, x1[1]), y1, (max(z2[0], z1[0]), min(z1[1], z2[1])))
            )

        # forward
        if y1[0] < y2[0]:
            result.append(
                (
                    (max(x1[0], x2[0]), min(x1[1], x2[1])),
                    (y1[0], y2[0] - 1),
                    (max(z2[0], z1[0]), min(z1[1], z2[1])),
                )
            )

        # behind
        if y1[1] > y2[1]:
            result.append(
                (
                    (max(x1[0], x2[0]), min(x1[1], x2[1])),
                    (y2[1] + 1, y1[1]),
                    (max(z2[0], z1[0]), min(z1[1], z2[1])),
                )
            )

        return result

    cuboids = []

    for state, new in instructions:
        overlaps = [c for c in cuboids if cuboids_overlap(new, c)]
        cuboids = [c for c in cuboids if c not in overlaps]

        for overlap in overlaps:
            cuboids.extend(split(overlap, new))

        if state:
            cuboids.append(new)

    return sum(
        (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
        for (x1, x2), (y1, y2), (z1, z2) in cuboids
    )


print(part_one(), part_two())
