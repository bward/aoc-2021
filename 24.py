from z3 import *

with open("input/24.txt") as handle:
    instructions = [line.rstrip().split(" ") for line in handle.readlines()]

optimize = Optimize()

inputs = []
for i in range(14):
    digit = BitVec(f"digit{i}", 64)
    inputs.append(digit)
    optimize.add(digit > 0, digit < 10)

next_input = len(inputs) - 1
zero, one = BitVecVal(0, 64), BitVecVal(1, 64)
registers = {
    "x": zero,
    "y": zero,
    "z": zero,
    "w": zero,
}

for i, op in enumerate(instructions):
    if op[0] == "inp":
        registers[op[1]] = inputs[next_input]
        next_input -= 1
    else:
        a = registers[op[1]]
        registers[op[1]] = BitVec(f"step{i}", 64)
        b = registers[op[2]] if op[2] in "xyzw" else int(op[2])

        if op[0] == "add":
            optimize.add(registers[op[1]] == a + b)
        elif op[0] == "mul":
            optimize.add(registers[op[1]] == a * b)
        elif op[0] == "div":
            optimize.add(registers[op[1]] == a / b)
        elif op[0] == "mod":
            optimize.add(registers[op[1]] == a % b)
        elif op[0] == "eql":
            optimize.add(registers[op[1]] == If(a == b, one, zero))


optimize.add(registers["z"] == 0)
digit_sum = sum(d * (10 ** i) for i, d in enumerate(inputs))

optimize.push()

result = optimize.maximize(digit_sum)
optimize.check()
print(result.value())

optimize.pop()

result = optimize.minimize(digit_sum)
optimize.check()
print(result.value())
