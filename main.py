def disassemble(instructions: [], start_address: int) -> []:
    bitmask_dict = {
        "op": 0b11111100000000000000000000000000,
        "rs": 0b00000011111000000000000000000000,
        "rt": 0b00000000000111110000000000000000,
        "rd": 0b00000000000000001111100000000000,
        "shamt": 0b00000000000000000000011111000000,
        "funct": 0b00000000000000000000000000111111,
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

    result = []

    pc = start_address  # Setting Program counter

    for instruction in instructions:
        # Instructions are fetched and pc is incremented by 4 since each instruction is 4 bytes long
        pc += 4

        # The current instruction address is the address of the instruction that is being disassembled
        # subtract 4 to account for the increment at the start of the loop
        current_instruction_address = pc - 4

        # Extracting fields from the instruction
        op: int = (instruction & bitmask_dict["op"]) >> 32 - 6
        rs: int = (instruction & bitmask_dict["rs"]) >> 32 - 11
        rt: int = (instruction & bitmask_dict["rt"]) >> 32 - 16
        rd: int = (instruction & bitmask_dict["rd"]) >> 32 - 21
        # funct and offset do not need to be shifted
        funct: int = (instruction & bitmask_dict["funct"])
        off: int = (instruction & bitmask_dict["off"])

        # R-Format instruction
        if op == 0:
            assembly_string = f"{hex(current_instruction_address)} {funct_dict[funct]} ${rd}, ${rs}, ${rt}"

        # I-Format instruction
        else:
            # Offset is a signed 16-bit integer, this is not natively supported in python
            # Check if offset is negative by checking if the most significant bit is 1
            if off & 0b1000000000000000:
                off -= 0b10000000000000000  # Subtract range of a signed 16-bit integer (2^16) to get the negative val

            # load and store instructions (lw, sw)
            assembly_string = f"{hex(current_instruction_address)} {funct_dict[op]} ${rt}, {off}(${rs})"

            # Branch instructions
            if funct_dict[op] in ["beq", "bne"]:
                # Target address is calculated by adding the offset to the PC,
                # offset is bit shifted left by 2 to account for the fact that the offset is in
                # words and each word is 4 bytes long, i.e. multiply by 4
                target = pc + (off << 2)
                assembly_string = f"{hex(current_instruction_address)} {funct_dict[op]} ${rs}, ${rt}, address {hex(target)}"

        result.append(assembly_string)
        # print(assembly_string)

    return result


def my_test():
    res = disassemble([0x00A63820, 0x8E870004], 0x9A040)
    assert res == ["0x9a040 add $7, $5, $6", "0x9a044 lw $7, 4($20)"], "Test Failed"
    print("Test Passed")


if __name__ == "__main__":
    my_test()

    project_start_address = 0x9A040
    project_instructions = [0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4,
                            0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0]
    result_assembly: [] = disassemble(project_instructions, project_start_address)

    print(f"Disassembled {len(result_assembly)} Instructions")
    for assembly in result_assembly:
        print(assembly)
