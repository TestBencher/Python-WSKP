# main.py

from file_read import file_read
from cpu import CPU

def main():
    filename = input("Enter filename with .txt extension please: ")
    memory = file_read(filename)
    cpu = CPU(memory)
    while cpu.running:
        instruction = cpu.fetch()
        cpu.execute(instruction)
    cpu.Print_statements()

if __name__ == "__main__":
    main()
