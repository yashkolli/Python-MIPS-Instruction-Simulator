# Python-MIPS-Instruction-Simulator
Microprocessor Without Iinterlocked Pipeline Stages (MIPS) is a RISC instruction set architecture devleoped in the 80's and still in use today. The implementation here includes only some of the instructions in each format for convenience only.<br />
MIPS contains instructions in 3 formats
  1. **R-Format**
  2. **I-Format**
  3. **J-Format**
<br />
The MIPS.py is the main driver file. The instruction_table.py file contains all the instructions that the simulator supports. The register.py file contains the memory addresses of all the 32 registers.<br />
<br/>
The simulator.py is the main backbone of this simulator. This file contains all functions defined for parsing several instructions.<br />
To run the simulator just run<br />
<br/>
python MIPS.py<br/>
<br/>
When prompted to enter the path for the file containing the assembly language program, enter the path and wait for the simulator to ask you for checking the register values after your program is executed.<br />
<br/>
The main advanatge of MIPS is, it executes most of the instructions only with the help of the 32 registers. This simulator is made to take care of most of the instructions which only need registers to work!
