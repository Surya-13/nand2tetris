var_value = 16
flag = 0
ac = 0
name = input()
alu_input = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "1+D": "0011111",
    "A+1": "0110111",
    "1+A": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "1+M": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101"
    }
destination = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }
jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15

}


def remove(line) :
    global flg
    if line == '' :
        return ''
    else :
        s = line[0]
    if line[0 :2] == "//" :
        return ""
    elif line[0 :2] == "*/" :
        flg = 0
        return line[line.index("*/") + 3 :]
    elif line[0 :2] == "/*" or flg == 1 :
        flg = 1
        if "*/" not in line :
            return ""
        else :
            flg = 0
            return line[line.index("*/") + 3 :]
    elif s == "\n" :
        return ""
    else :
        return s + remove(line[1 :])


def first_pass():
    inp = open(name + '.asm', 'r')
    out = open(name + '.txt', 'w')
    line_count = 0
    for line in inp:
        new_line = remove(line)
        if new_line != "":
            if new_line[0] == "(":
                label = new_line[1:-1]
                table[label] = line_count
                #new_line = ""
            else:
                line_count += 1
                out.write(new_line + "\n")
    inp.close()
    out.close()


def add_variable(var):
    global var_value
    if var not in table:
        table[var] = var_value
        var_value += 1
        return table[var]


def a_instruction(line):
    if line[0].isalpha():
        label = line[:]
        avalue = table.get(label, -1)
        if avalue == -1:
            avalue = add_variable(label)
    else:
        avalue = int(line[:])
    bvalue = str(bin(avalue)[2:].zfill(16))
    return bvalue


def c_instruction(line):
    if "=" not in line:
        dest = "null"
        temp = line.split(";")
        alu = temp[0]
        jmp = temp[1]
    elif ";" not in line:
        jmp = "null"
        temp = line.split("=")
        alu = temp[1]
        dest = temp[0]
    if (dest not in destination) or (jmp not in jump) or (alu not in alu_input):
        print("Error in c instruction")
    else:
        return "111" + alu_input[alu] + destination[dest] + jump[jmp]


def second_pass():
    global ac
    inp = open(name + '.txt', 'r')
    out = open(name + '.hack', 'w')
    for line in inp:
        if line[0] == "@" and ac == 0:
            out.write(a_instruction(line[1:-1]) + "\n")
            ac += 1
        elif line[0] != "@" and ac == 1:
            out.write(c_instruction(line[:-1]) + "\n")
            ac -= 1
        else:
            print("Error in Input")
            out.close()
            out = open(name + '.hack', 'w')
            out.close()
            break
    inp.close()
    out.close()


first_pass()
second_pass()
