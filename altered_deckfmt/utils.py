import base64
from collections import defaultdict


def parse_decklist(string: str, separator) -> dict[str, list[tuple[int, str]]]:
    card_sets = defaultdict(list)
    for line in string.split(separator):
        if content := line.strip():
            quantity, reference = content.split()
            card_set = reference.split("_")[1]
            card_sets[card_set].append((int(quantity), reference))

    return card_sets


def string_to_base64(binary_string: str) -> str:
    num_bytes = (len(binary_string) + 7) // 8 * 8
    binary_string = binary_string.ljust(num_bytes, "0")
    binary_bytes = bytes(
        int(binary_string[i : i + 8], 2) for i in range(0, num_bytes, 8)
    )

    return str(base64.b64encode(binary_bytes))[2:-1]


def base64_to_string(encoded_string: str) -> str:
    decoded = base64.b64decode(encoded_string)
    binary_string = bin(int.from_bytes(decoded))[2:]
    num_bytes = (len(binary_string) + 7) // 8 * 8

    return binary_string.zfill(num_bytes)


def encode_chunk(value: int, size: int) -> str:
    return format(value, f"0{size}b")

def decode_chunk(string: str, start: int, size: int) -> int:
    return int(string[start:(start + size)], 2)
