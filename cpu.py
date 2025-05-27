## cpu.py
#
# @date 2025-04-20
# @author Sai Vishwesh
# @brief Simulates the MIPS-Lite CPU with 32 registers, memory, PC, and instruction execution.
# @details Right now handles only ADD, SUB, ADDI, BEQ, LW, SW, and J instructions. Should we consider adding other instructions like AND, OR, etc.?
##
from decoder import decode_instruction

#@brief Initializes the CPU with 32 registers, a program counter (PC), and a memory reference.
#@param memory A list representing the loaded instruction memory.
#@return None

class CPU:
    def __init__(self, memory):
        self.registers = [0] * 32 # 32 Registers
        self.memory = memory 
        self.pc = 0  # Program Counter
        self.running = True 
        self.instruction_count = {}

#@brief Fetches the instruction at the current program counter (PC).
#@return 32-bit instruction at PC.

    def fetch(self):
        return self.memory[self.pc // 4]
    
#@brief Decodes and dispatches the instruction for execution.
#@param instruction A 32-bit integer instruction.

    def execute(self, inst):
        Type = decode_instruction(inst)
        inst_type = Type['type']
        
        if inst_type == 'R':
            self.execute_r_type(Type)
        elif inst_type == 'I':
            self.execute_I_type(Type)
        elif inst_type == 'J':
            self.execute_J_type(Type)
        else:
            raise Exception("Unknown instruction type")

   def execute_r_type(self, instr):
    funct = instr['funct']
    rs = instr['rs']
    rt = instr['rt']
    rd = instr['rd']
    shamt = instr.get('shamt', 0)  # Shift amount is used for sll and srl

    if funct == 0x20:  # ADD
        self.registers[rd] = self.registers[rs] + self.registers[rt]
    elif funct == 0x22:  # SUB
        self.registers[rd] = self.registers[rs] - self.registers[rt]
    elif funct == 0x24:  # AND
        self.registers[rd] = self.registers[rs] & self.registers[rt]
    elif funct == 0x25:  # OR
        self.registers[rd] = self.registers[rs] | self.registers[rt]
    elif funct == 0x2A:  # SLT (Set on Less Than)
        self.registers[rd] = int(self.registers[rs] < self.registers[rt])
    elif funct == 0x00:  # SLL (Shift Left Logical)
        self.registers[rd] = self.registers[rt] << shamt
    elif funct == 0x02:  # SRL (Shift Right Logical)
        self.registers[rd] = (self.registers[rt] & 0xFFFFFFFF) >> shamt
    elif funct == 0x0C:  # HALT (assuming HALT is a custom R-type funct code)
        self.running = False
    else:
        raise Exception(f"Unsupported R-type funct code: {hex(funct)}")

    self.pc += 4
    self.instruction_count[funct] = self.instruction_count.get(funct, 0) + 1


    def execute_I_type(self, instr):
    opcode = instr['opcode']
    rs = instr['rs']
    rt = instr['rt']
    imm = instr['immediate']

    if opcode == 0x08:  # ADDI
        self.registers[rt] = self.registers[rs] + imm
    elif opcode == 0x0C:  # ANDI
        self.registers[rt] = self.registers[rs] & (imm & 0xFFFF)
    elif opcode == 0x0D:  # ORI
        self.registers[rt] = self.registers[rs] | (imm & 0xFFFF)
    elif opcode == 0x0A:  # SLTI
        self.registers[rt] = int(self.registers[rs] < imm)
    elif opcode == 0x05:  # BNE
        if self.registers[rs] != self.registers[rt]:
            self.pc += 4 + (imm << 2)
            return
    elif opcode == 0x0F:  # LUI
        self.registers[rt] = (imm & 0xFFFF) << 16
    elif opcode == 0x04:  # BEQ
        if self.registers[rs] == self.registers[rt]:
            self.pc += 4 + (imm << 2)
            return
    elif opcode == 0x23:  # LW
        address = self.registers[rs] + imm
        self.registers[rt] = self.memory[address // 4]
    elif opcode == 0x2B:  # SW
        address = self.registers[rs] + imm
        self.memory[address // 4] = self.registers[rt]
    else:
        raise Exception(f"Unsupported I-type opcode: {hex(opcode)}")

    self.pc += 4
    self.instruction_count[opcode] = self.instruction_count.get(opcode, 0) + 1


    def execute_J_type(self, instr):
        opcode = instr['opcode']
        address = instr['address']

        if opcode == 0x02:  # J
            self.pc = (self.pc & 0xF0000000) | (address << 2)
        else:
            raise Exception(f"Unsupported J-type opcode: {hex(opcode)}")

        self.instruction_count[opcode] = self.instruction_count.get(opcode, 0) + 1

    def Print_statements(self):
        print("Registers:")
        for i in range(32):
            print(f"R{i}: {self.registers[i]}")
        
        print("\nNon-zero Memory:")
        for i, word in enumerate(self.memory):
            if word != 0:
                print(f"Memory[{i * 4}]: {hex(word)}")
        
        print("\nInstruction Count:")
        for instr, count in self.instruction_count.items():
            print(f"Instruction {hex(instr)} executed {count} times")
