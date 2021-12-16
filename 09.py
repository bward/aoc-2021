with open("input/09.txt") as handle:
    heights = [[int(d) for d in row.rstrip()] for row in handle.readlines()]

risk_sum = 0
low_points = set()
deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]

for y, row in enumerate(heights):
    for x, height in enumerate(row):
        for dx, dy in deltas:
            if 0 <= x + dx < len(row) and 0 <= y + dy < len(heights):
                if heights[y + dy][x + dx] <= heights[y][x]:
                    break
        else:
            risk_sum += 1 + height
            low_points.add((x, y))

print(risk_sum)

not_seen = set(
    (x, y)
    for y, row in enumerate(heights)
    for x, height in enumerate(row)
    if height != 9
)

basin_sizes = []
width = len(heights[0])
height = len(heights)

while low_points:
    start = low_points.pop()
    seen = set()
    boundary = set([start])

    while boundary:
        new_boundary = set()

        for x, y in boundary:
            if (x, y) in seen:
                continue
            seen.add((x, y))

            for dx, dy in deltas:
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    if (
                        heights[y + dy][x + dx] >= heights[y][x]
                        and (x + dx, y + dy) not in seen
                        and heights[y + dy][x + dx] != 9
                    ):
                        new_boundary.add((x + dx, y + dy))

        boundary = new_boundary

    basin_sizes.append(len(seen))


basin_sizes.sort()
print(basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3])
