r_format_bitmask_dict = {
    "op": 0b11111100000000000000000000000000,
    "rs": 0b00000011111000000000000000000000,
    "rt": 0b00000000000111110000000000000000,
    "rd": 0b00000000000000001111100000000000,
    "shamt": 0b00000000000000000000011111000000,
    "funct": 0b00000000000000000000000000111111,
}

i_format_bitmask_dict = {
    "op": 0b11111100000000000000000000000000,
    "rs": 0b00000011111000000000000000000000,
    "rt": 0b00000000000111110000000000000000,
    "off": 0b00000000000000001111111111111111,
}

funct_dict = {
    0b100000: "add",
    0b100010: "sub",
    0b100100: "and",
    0b011010: "div",
    0b100101: "or",
    0b101010: "slt",
    0b100011: "lw",
    0b101011: "sw",
    0b000100: "beq",
    0b000101: "bne",
}


def disassemble(instructions: [], start_address: int) -> []:
    result = []
    current_address = start_address - 4  # Adjusting for incrementing at the start of the loop

    for instruction in instructions:
        current_address += 4

        # Extracting fields from the instruction
        op: int = (instruction & r_format_bitmask_dict["op"]) >> 32 - 6
        rs: int = (instruction & r_format_bitmask_dict["rs"]) >> 32 - 11
        rt: int = (instruction & r_format_bitmask_dict["rt"]) >> 32 - 16
        rd: int = (instruction & r_format_bitmask_dict["rd"]) >> 32 - 21
        funct: int = (instruction & r_format_bitmask_dict["funct"])

        # R-Format instruction
        if op == 0:
            assembly_string = f"{hex(current_address)} {funct_dict[funct]} ${rd}, ${rs}, ${rt}"

        # I-Format instruction
        else:
            off: int = (instruction & i_format_bitmask_dict["off"])
            # Offset is a signed 16-bit integer, this is not natively supported in python
            # Check if the number is negative by checking if the most significant bit is 1
            if off & 0b1000000000000000:
                off -= 0b10000000000000000  # Subtract range of a signed 16-bit integer (2^16) to get the negative val
            assembly_string = f"{hex(current_address)} {funct_dict[op]} ${rt}, {off}(${rs})"

            # Branch instructions
            if funct_dict[op] in ["beq", "bne"]:
                # Calculate target address, add 4 since instructions are relative to next instruction and *4 to
                # covert from word offset to byte offset
                target = current_address + 4 + (off * 4)
                assembly_string = f"{hex(current_address)} {funct_dict[op]} ${rs}, ${rt}, address {hex(target)}"

        result.append(assembly_string)

    return result


def my_test():
    r = disassemble([0x00A63820, 0x8E870004], 0x9A040)
    assert (r == ["0x9a040 add $7, $5, $6", "0x9a044 lw $7, 4($20)"])
    print("Test Passed")


if __name__ == "__main__":
    # my_test()

    project_start_address = 0x9A040
    project_instructions = [0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4,
                            0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0]

    print("Disassembled " + str(len(project_instructions)) + " instructions :")
    print()
    for i in disassemble(project_instructions, project_start_address):
        print(i)