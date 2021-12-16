import re

with open("input/13.txt") as handle:
    points = set()
    folds = []

    lines = (line.rstrip() for line in handle.readlines())

    for line in lines:
        if not line:
            break
        vals = [int(x) for x in line.split(",")]
        points.add((vals[0], vals[1]))

    for line in lines:
        matches = re.match(r"fold along (y|x)=(\d+)", line).groups()
        folds.append((matches[0], int(matches[1])))

for axis, val in folds:
    new_points = set()
    for (x, y) in points:
        if axis == "x" and x >= val:
            new_points.add((2 * val - x, y))
        elif axis == "y" and y >= val:
            new_points.add((x, 2 * val - y))
        else:
            new_points.add((x, y))

    points = new_points
    print(len(points))

x_max = max(x for x, _ in points)
y_max = max(y for _, y in points)

for y in range(y_max + 1):
    out = ""
    for x in range(x_max + 1):
        if (x, y) in points:
            out += "#"
        else:
            out += "."
    print(out)
