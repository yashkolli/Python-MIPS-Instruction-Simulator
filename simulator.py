z = [0] * 32

naccr =  [0, 1, 26, 27, 28, 29, 30, 31]

def add(a, b, c):
    z[a] = z[b] + z[c]

def andf(a, b, c):
    z[a] = z[b] & z[c]

def orf(a, b, c):
    z[a] = z[b] | z[c]

def nor(a, b, c):
    z[a] = ~(z[b] | z[c])

def slt(a, b, c):
    if (z[b] < z[c]):
        z[a] = 1
    else:
        z[a] = 0

def sll(a, b, value):
    z[a] = z[b] << value

def srl(a, b, value):
    z[a] = z[b] >> value

def sub(a, b, c):
    z[a] = z[b] - z[c]


def beq(a ,b):
    if (z[a] == z[b]):
        return True

def bne(a, b):
    if (z[a] != z[b]):
        return True

def addi(a, b, value):
    z[a] = z[b] + value

def andi(a, b, value):
    z[a] = z[b] & value

def ori(a, b, value):
    z[a] = z[b] | value

def stli(a, b, value):
    if (z[b] < value):
        z[a] = 1
    else:
        z[a] = 0

def lui(a, value):
    z[a] = value << 16

def instruction_to_function(instruction, rd, rs, rt):

    rdp = rd
    rsp =rs
    rtp = rt

    switcher = {'add': add,
    'addu':add,
    'and':andf,
    'or':orf,
    'nor':nor,
    'slt':slt,
    'sltu':slt,
    'sll':sll,
    'srl':srl,
    'sub':sub,
    'subu':sub,
    'addi':addi,
    'addiu':addi,
    'andi':andi,
    'ori':ori,
    'stli':stli,
    'sltiu':stli }

    func = switcher.get(instruction)
    func(rdp, rsp, rtp)

class mips_simulator(object):

    symbol_table = {}

    current_location = 0

    default_mem_loc  = 0

    instruction_table = {}

    register_table = {}

    def __init__(self, default_memory_location, instruction_table, register_table):

        self.default_mem_loc    = default_memory_location
        self.instruction_table  = instruction_table
        self.register_table     = register_table

    def first_pass(self, lines):

        self.current_location = self.default_mem_loc

        for line in lines:

            if "#" in line:
                line = line[ 0: line.find("#") ]
            line = line.strip()
            if not len(line):
                continue

            if ":" in line:
                label = line[0:line.find(':')]
                self.symbol_table[label] = str(self.current_location)
                line = line[line.find(':') + 1:].strip()

            self.current_location += 1

    def second_pass(self, lines):

        self.current_location = self.default_mem_loc

        k = 0
        while k < len(lines):

            line = lines[k]

            if "#" in line:
                line = line[ 0: line.find("#") ]
            line = line.strip()
            if not len(line):
                continue

            if ":" in line:
                label = line[0:line.find(':')]
                line = line[line.find(':') + 1:].strip()

            instruction = line[0:line.find(' ')].strip()
            args        = line[line.find(' ') + 1:].replace(' ', '').split(',')

            if not instruction:
                break

            acount = 0
            for arg in args:
                if arg not in self.symbol_table.keys():
                    if arg[-1] == 'H':
                        args[acount] = str(int(arg[:-1], 16))
                    elif arg[-1] == 'B':
                        args[acount] = str(int(arg[:-1], 2))
                acount += 1

            kp = k
            if instruction in self.instruction_table.keys():
                k = self.parse_instruction(instruction, args, kp)

            else:
                print("INSTRUCTION:" + instruction + "IS INVALID! ABORT")
                exit()

        status = True
        while status:
            print("\nWhich register you want to check for the output?\n")
            registerno = int(input())
            print(z[registerno])
            print("\n Do you want to check more registers?\nPress y or n!")
            ans = input()
            if ans=='n' or ans=='N':
                status = False

    def parse_instruction(self, instruction, raw_args, k):

        instruction_type = self.instruction_table[instruction]
        kp = k
        arg_count = 0
        args = raw_args[:]

        for arg in args:

            if arg in self.register_table.keys():
                args[arg_count] = int(self.register_table[arg])

            elif arg in self.symbol_table:
                args[arg_count] = self.symbol_table[arg] + "L"

            arg_count += 1

        if instruction_type == "r":

            rs = '0'
            rt = '0'
            rd = '0'

            if len(args) == 1:
                rv = int(a[args[0]])
                return rv
            else:
                rs = int(args[1])
                rt = int(args[2])
                rd = int(args[0])
                if not rd in naccr:
                    instruction_to_function(instruction, rd, rs, rt)
                return int(kp+1)

        elif instruction_type == "i":

            rs  = int(args[1])
            rt  = int(args[0])
            if len(args) > 2:
                if args[2][-1]=="L":
                    if instruction == "beq":
                        status = beq(rs, rt)
                    else:
                        status = bne(rs, rt)
                    if status:
                        rv = int(args[2][:-1])
                        return rv
                    else:
                        return int(kp+1)
                else:
                    imm = int(args[2])
                    if not rt in naccr:
                        instruction_to_function(instruction, rt, rs, imm)
                    return int(kp+1)

            else:
                if not rt in naccr:
                    lui(rt, rs)
                return int(kp+1)

        else:

            rv = int(args[0][:-1])
            if instruction == "jal":
                z[31] = kp + 1
            return rv


