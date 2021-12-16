import re
from collections import defaultdict, Counter

with open("input/14.txt") as handle:
    template = handle.readline().rstrip()
    handle.readline()
    rules = dict(
        re.match(r"(.*) -> (.)", line.rstrip()).groups() for line in handle.readlines()
    )


def insert(template_pairs, rules):
    output = defaultdict(int)

    for pair, count in template_pairs.items():
        match = rules[pair]
        output[f"{pair[0]}{match}"] += count
        output[f"{match}{pair[1]}"] += count

    return output


def get_diff(template_pairs):
    counts = defaultdict(int)
    for pair, count in template_pairs.items():
        counts[pair[0]] += count
        counts[pair[1]] += count

    counts[template[0]] += 1
    counts[template[-1]] += 1

    for pair in counts:
        counts[pair] //= 2

    counts = Counter(counts).most_common()

    return counts[0][1] - counts[-1][1]


template_pairs = defaultdict(int)
for i in range(len(template) - 1):
    template_pairs[template[i : i + 2]] += 1

for i in range(10):
    template_pairs = insert(template_pairs, rules)
print(get_diff(template_pairs))

for i in range(30):
    template_pairs = insert(template_pairs, rules)
print(get_diff(template_pairs))
