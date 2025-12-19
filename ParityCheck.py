def ParityGen(hex_vector: str) -> int:
    hex_vector = hex_vector.replace("_", "")
    value = int(hex_vector, 16)
    return value.bit_count() & 1    #Inverse this for odd parity.

if __name__ == "__main__":
    print("Enter hex vectors (empty line to quit):")

    while True:
        try:
            line = input("> ").strip()
            if not line:
                break
            print("Even parity bit:", ParityGen(line))
        except ValueError:
            print("Invalid input. Format must be in HEX format")
