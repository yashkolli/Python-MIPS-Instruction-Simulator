from simulator import mips_simulator
from instruction_table import instruction_table
from register_table import register_table

print("Hello User! Welcome to the instruction format simulator for MIPS.\n")
print("This simulator can simulate some of the instructions from each format.\n")
print("You can enter the path for a file consisting of single line assembly language instructions or also enter a whole program.\n")
print("So here go the instructions.\n\n")
print("1. You are requested to enter the path for the file\n")
print("2. Wait for the simulator to show the output\n")
print("\n Go ahead and start with entering the path for your file\n")

path = input()

asm = open(path, "r")
lines = asm.readlines()
simulator = mips_simulator(0, instruction_table, register_table)
simulator.first_pass(lines)
simulator.second_pass(lines)
