import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, cast

with open("input/16.txt") as handle:
    hex_input = handle.readline().rstrip()

bin_data = bin(int(hex_input, 16))[2:].zfill(4 * len(hex_input))


@dataclass
class Packet:
    version: int
    type_id: int
    subpackets: List["Packet"]
    value: Optional[int] = None


def parse_packet(data: str) -> Packet:
    def inner(data: str) -> Tuple[Packet, str]:
        version = int(data[:3], 2)
        type_id = int(data[3:6], 2)

        if type_id == 4:
            raw_value = ""
            raw_contents = data[6:]

            while True:
                raw_value += raw_contents[1:5]
                if raw_contents[0] == "0":
                    break
                raw_contents = raw_contents[5:]
            value = int(raw_value, 2)

            return (
                Packet(version, type_id, value=value, subpackets=[]),
                data[6 + 5 * (len(raw_value) // 4) :],
            )

        else:
            length_id = int(data[6:7], 2)

            if length_id == 0:
                payload_length = int(data[7:22], 2)
                subpacket_data = data[22 : 22 + payload_length]
                subpackets = []

                while subpacket_data:
                    subpacket, subpacket_data = inner(subpacket_data)
                    subpackets.append(subpacket)

                remainder = data[22 + payload_length :]

            else:
                number_of_subpackets = int(data[7:18], 2)
                subpacket_data = data[18:]
                subpackets = []

                for _ in range(number_of_subpackets):
                    subpacket, subpacket_data = inner(subpacket_data)
                    subpackets.append(subpacket)

                remainder = subpacket_data

        return (
            Packet(version=version, type_id=type_id, subpackets=subpackets),
            remainder,
        )

    packet, _ = inner(data)
    return packet


def part_one(packet: Packet) -> int:
    return packet.version + sum(part_one(subpacket) for subpacket in packet.subpackets)


def part_two(packet: Packet) -> int:
    subvalues = [part_two(subpacket) for subpacket in packet.subpackets]
    operators = {
        0: sum,
        1: math.prod,
        2: min,
        3: max,
        4: lambda _: packet.value,
        5: lambda v: int(v[0] > v[1]),
        6: lambda v: int(v[0] < v[1]),
        7: lambda v: int(v[0] == v[1]),
    }

    return operators[packet.type_id](subvalues)


packets = parse_packet(bin_data)

print(part_one(packets))
print(part_two(packets))
