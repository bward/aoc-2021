with open("input/10.txt") as handle:
    lines = [l.rstrip() for l in handle.readlines()]

score = 0

pairs = {"(": ")", "[": "]", "<": ">", "{": "}"}
backward_pairs = {v: k for k, v in pairs.items()}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
remainder_scores = {")": 1, "]": 2, "}": 3, ">": 4}


def calculate_score(remainder: str) -> int:
    total = 0
    for char in remainder:
        total *= 5
        total += remainder_scores[char]
    return total


autocomplete_scores = []

for line in lines:
    stack = []
    for char in line:
        if char not in backward_pairs:
            stack.append(char)
        elif stack[-1] == backward_pairs[char]:
            stack.pop()
        else:
            score += scores[char]
            break
    else:
        completion = "".join(pairs[c] for c in stack[::-1])
        autocomplete_scores.append(calculate_score(completion))

print(score)
print(sorted(autocomplete_scores)[len(autocomplete_scores) // 2])
