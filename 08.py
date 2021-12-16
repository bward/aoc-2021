with open("input/08.txt") as handle:
    parts = (line.rstrip().split(" | ") for line in handle.readlines())
    signals = [(p[0].split(" "), p[1].split(" ")) for p in parts]

print(sum(len([x for x in s[1] if len(x) in [2, 4, 3, 7]]) for s in signals))

total = 0

for s in signals:
    inputs = [frozenset(x) for x in s[0]]
    outputs = [frozenset(x) for x in s[1]]

    forwards = {}
    backwards = {}

    # Find patterns with unique lengths first
    for signal in inputs:
        if len(signal) == 2:
            forwards[signal] = 1
            backwards[1] = signal
        elif len(signal) == 4:
            forwards[signal] = 4
            backwards[4] = signal
        elif len(signal) == 3:
            forwards[signal] = 7
            backwards[7] = signal
        elif len(signal) == 7:
            forwards[signal] = 8
            backwards[8] = signal

    # Figure out the rest based on how they overlap the ones we already know
    for signal in inputs:
        if len(signal) == 6:
            if len(signal.union(backwards[7])) == 7:
                forwards[signal] = 6
                backwards[6] = signal
            elif len(signal.union(backwards[4])) == 6:
                forwards[signal] = 9
                backwards[9] = signal
            else:
                forwards[signal] = 0
                backwards[0] = signal

        if len(signal) == 5:
            if len(signal.union(backwards[1])) == 5:
                forwards[signal] = 3
                backwards[3] = signal
            elif len(signal.union(backwards[4])) == 6:
                forwards[signal] = 5
                backwards[5] = signal
            else:
                forwards[signal] = 2
                backwards[2] = signal

    total += int("".join(str(forwards[signal]) for signal in outputs))

print(total)
