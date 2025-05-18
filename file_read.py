## memoryfile.py
#
# @date 2025-04-20
# @author Sai Vishwesh
# @brief Loads the contents of the file from a hex format into a 4KB memory array.
# @param filename - The name of the file (Assumptions - hex format, one instruction per line).
# @return A list of integers representing the memory (each entry is a 32-bit word).
#
##

def file_read(filename):
    memory = [0] * 1024  # 4KB of memory (4 bytes per word), increase as necessary.
    with open(filename, 'r') as file:
        for address, line in enumerate(file):  # enumerate starts from 0 and gives the line number and the line content. 
            word = int(line.strip(), 16) # converting hex to int because the file is assumed to be in hex format.
            memory[address] = word
    return memory
