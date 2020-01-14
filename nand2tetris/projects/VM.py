name = input()
flag = 0
label_number = 0
val = 0
output = {
    "add":  "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M+D\n@SP\nM=M-1\n",
    "sub":  "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1\n",
    "and":  "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M&D\n@SP\nM=M-1\n",
    "or":   "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nM=M|D\n@SP\nM=M-1\n",
    "neg":  "@SP\nA=M\nA=A-1\nM=-M\n",
    "not":  "@SP\nA=M\nA=A-1\nM=!M\n",
    "eq":   "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@Label_{}\nD;JEQ\nD=0\n@Label_{}\n0;JMP\n"
            "(Label_{})\nD=-1\n(Label_{})\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n",
    "gt":   "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@Label_{}\nD;JGT\nD=0\n@Label_{}\n0;JMP\n"
            "(Label_{})\nD=-1\n(Label_{})\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n",
    "lt":   "@SP\nA=M\nA=A-1\nD=M\nA=A-1\nD=M-D\n@Label_{}\nD;JLT\nD=0\n@Label_{}\n0;JMP\n"
            "(Label_{})\nD=-1\n(Label_{})\n@SP\nM=M-1\nA=M\nA=A-1\nM=D\n",
}
push_pop = {
    "argument": "ARG",
    "local":    "LCL",
    "this":     "THIS",
    "that":     "THAT",
    "temp":     "5",
    "pointer":  "3",
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


def make_file():
    inp = open(name + ".vm", "r")
    out = open(name + ".txt", "w")
    line_count = 0
    for line in inp:
        new_line = remove(line)
        if new_line != "":
            line_count += 1
            out.write(new_line + "\n")
        else:
            out.write(new_line)
            line_count += 1


def print_call(b, c):
    global name, val
    s = ""
    s += f"@Label${name}${val}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    s += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    s += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    s += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    s += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    s += f"@SP\nD=M\n@{c}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n"
    s += "@SP\nD=M\n@LCL\nM=D\n"
    s += f"@{b}\n0;JMP\n"
    s += f"(Label${name}${val})\n"
    val += 1
    return s


def print_return():
    s = ""
    s += "@LCL\nD=M\n@R13\nM=D\n"
    s += "@5\nA=D-A\nD=M\n@R14\nM=D\n"
    s += "@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n"
    s += "@ARG\nD=M\nD=D+1\n@SP\nM=D\n"
    s += "@R13\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n"
    s += "@R13\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n"
    s += "@R13\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n"
    s += "@R13\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n"
    s += "@R14\nA=M\n0;JMP\n"
    return s


def print_func(b,c):
    s = ""
    s += f"({b})\n"
    while c:
        s += "@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        c -= 1
    return s


def print_operation(a, b, c):
    global name,val
    s = ""
    c = int(c)
    if a == "push":
        if b == "constant":
            s += f"@{c}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif b == "static":
            s += f"@{name}_{c}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        elif b in push_pop:
            if b == "temp" or b == "pointer":
                s += f"@{push_pop[b]}\nD=A\n@{c}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            else:
                s += f"@{push_pop[b]}\nD=M\n@{c}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    elif a == "pop":
        if b == "static":
            s += f"@SP\nA=M-1\nD=M\n@{name}_{c}\nM=D\n@SP\nM=M-1\n"
        elif b in push_pop:
            if b == "temp" or b == "pointer":
                s += f"@{push_pop[b]}\nD=A\n@{c}\nD=A+D\n@R13\nM=D\n@SP\nA=M\nA=A-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
            else:
                s += f"@{push_pop[b]}\nD=M\n@{c}\nD=A+D\n@R13\nM=D\n@SP\nA=M\nA=A-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
    elif a == "call":
        s += print_call(b,c)
    elif a == "function":
        s += print_func(b,c)
    return s


def print_label(a,b):
    if a == "label":
        return f"({b})\n"
    elif a == "goto":
        return f"@{b}\n0;JMP\n"
    elif a == "if-goto":
        return f"@SP\nM=M-1\nA=M\nD=M\n@{b}\nD;JNE\n"


def print_algebra(a):
    return output[a]


def read_file():
    global label_number
    label_number = 0
    inp = open(name + ".txt","r")
    out = open(name + ".asm","w")
    for line in inp:
        line_list = line[:-1].split()
        if len(line_list) == 3:
            out.write(print_operation(line_list[0], line_list[1], line_list[2]))
        elif len(line_list) == 1:
            if line_list[0] == "eq" or line_list[0] == "gt" or line_list[0] == "lt":
                out.write(print_algebra(line_list[0]).format(label_number,label_number+1,label_number,label_number+1))
                label_number += 2
            elif line_list[0] == "return":
                out.write(print_return())
            else:
                out.write(print_algebra(line_list[0]))
        elif len(line_list) == 2:
            out.write(print_label(line_list[0], line_list[1]))


make_file()
read_file()
