from z3 import *

with open("input/24.txt") as handle:
    instructions = [line.rstrip().split(" ") for line in handle.readlines()]

opt = Optimize()

inputs = []
for i in range(14):
    digit = BitVec(f"input{i}", 64)
    inputs.append(digit)
    opt.add(digit > 0, digit < 10)

input_ptr = 13

zero, one = BitVecVal(0, 64), BitVecVal(1, 64)

registers = {
    "x": zero,
    "y": zero,
    "z": zero,
    "w": zero,
}

for i, op in enumerate(instructions):
    intermediate = BitVec(f"intermediate_{i}", 64)

    if op[0] == "inp":
        registers[op[1]] = inputs[input_ptr]
        input_ptr -= 1
        continue

    a = registers[op[1]]
    b = registers[op[2]] if op[2] in "xyzw" else int(op[2])

    if op[0] == "add":
        opt.add(intermediate == a + b)
    elif op[0] == "mul":
        opt.add(intermediate == a * b)
    elif op[0] == "div":
        opt.add(intermediate == a / b)
    elif op[0] == "mod":
        opt.add(intermediate == a % b)
    elif op[0] == "eql":
        opt.add(intermediate == If(a == b, one, zero))

    registers[op[1]] = intermediate


opt.add(registers["z"] == 0)
digit_sum = sum(d * (10 ** i) for i, d in enumerate(inputs))

opt.push()

result = opt.maximize(digit_sum)
opt.check()
print(result.value())

opt.pop()

result = opt.minimize(digit_sum)
opt.check()
print(result.value())
