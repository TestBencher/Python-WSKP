## decoder.py
#
# @date 2025-04-20
# @author Sai Vishwesh 
# @brief Decodes a 32-bit MIPS instruction into R-type, I-type or J-type format.
# @param inst - A 32-bit integer representing the instruction.
# @return Type of instruction (R, I or J), Opcode, rs, rt, rd, shamt and funct. 
#
##

def decode_instruction(inst):
    opcode = (inst >> 26) & 0x3F  # Right shift by 26 and masked with 00111111 to get the opcode
    if opcode == 0x00:  # R-type
        rs = (inst >> 21) & 0x1F # Source Register
        rt = (inst >> 16) & 0x1F # Target Register
        rd = (inst >> 11) & 0x1F # Destination Register
        shamt = (inst >> 6) & 0x1F # Shift Number
        funct = inst & 0x3F
        return {'type': 'R', 'opcode': opcode, 'rs': rs, 'rt': rt, 'rd': rd, 'shamt': shamt, 'funct': funct}
    elif opcode in [0x02, 0x03]:  # J-type
        address = inst & 0x03FFFFFF
        return {'type': 'J', 'opcode': opcode, 'address': address}
    else:  # I-type
        rs = (inst >> 21) & 0x1F
        rt = (inst >> 16) & 0x1F
        immediate = inst & 0xFFFF
        if immediate & 0x8000:  # Sign extend if negative so that it doesn't misinterpret the immediate value. For example, if immediate is 0xFFFF, it should be interpreted as -1 and not as 65535.
            immediate -= 0x10000
        return {'type': 'I', 'opcode': opcode, 'rs': rs, 'rt': rt, 'immediate': immediate}
