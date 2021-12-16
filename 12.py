from collections import defaultdict, deque

with open("input/12.txt") as handle:
    edges = (line.rstrip().split("-") for line in handle.readlines())
    graph = defaultdict(set)

    for start, end in edges:
        graph[start].add(end)
        graph[end].add(start)


queue = deque([("start", ("start",))])
count = 0

while queue:
    cur, path = queue.popleft()

    for cave in graph[cur]:
        if cave.islower() and cave in path:
            continue
        elif cave == "end":
            count += 1
        else:
            queue.append((cave, path + (cave,)))

print(count)


queue = deque([("start", ("start",), False)])
count = 0

while queue:
    cur, path, double_visit = queue.popleft()

    for cave in graph[cur]:
        if cave.islower() and cave in path and double_visit:
            continue
        elif cave == "start":
            continue
        elif cave == "end":
            count += 1
        else:
            queue.append(
                (
                    cave,
                    path + (cave,),
                    double_visit or cave.islower() and cave in path,
                )
            )

print(count)
