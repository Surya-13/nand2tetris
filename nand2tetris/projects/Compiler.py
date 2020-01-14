####################################
##                                ##
##  NAME: B.V.S SUDHEENDRA        ##
##  ROLL NO: CS18B006             ##
##  COMPILER CODE                 ##
##  COMPLETED ON: 12-11-19        ##
##  LAST MODIFIED: 14-01-20       ##
####################################

# Declaring Global Variables
global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, out, err, fin

# Initializing some of the global variables
flg = 0
space = 0
label_number = 0

#  Dictionary for Operations
op = {
    '+' : 'add\n',
    '-' : 'sub\n',
    '*' : 'call Math.multiply 2\n',
    '/' : 'call Math.divide 2\n',
    '|' : 'or\n',
    '&amp' : 'and\n',
    '&lt' : 'lt\n',
    '&gt' : 'gt\n',
    '=' : 'eq\n'
}
# List of Keywords and Symbols
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void',
            'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbols = ['(', ')', '{', '}', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


# Creating Class for Classes and Subroutines
class Class_Table() :
    def __init__(self, name) :
        self.static_count = 0  #
        self.field_count = 0  # Initializing the variables
        self.total_count = 0  #
        self.name = name  #
        self.classtable = {}  # Initializing the Class Table to NULL

    def get_name(self) :  # Function to get the name of the present Class
        return self.name


class SubRoutineDec() :
    def __init__(self, name) :
        self.local_count = 0  #
        self.argument_count = 0  # Initializing the variables
        self.total_count = 0  #
        self.name = name  #
        self.subroutine_table = {}  # Initializing the Subroutine table to NULL

    def get_name(self) :  # Function to get the name of the present Subroutine
        return self.name


# Function to Effectively remove white spaces and all types of comments
# for each line passing into this
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


# The Function which removes all the comments and useless lines from the
# .jack file and creates a .txt file.
def make_file_txt(name) :
    inp = open(name + ".jack", "r")
    out = open(name + ".txt", "w")
    line_count = 0
    for line in inp :
        new_line = remove(line)
        if new_line != "" :
            line_count += 1
            out.write(new_line + "\n")
        else :
            out.write(new_line)
            line_count += 1


# Tokenizer function which creates the token for each line in the .txt file
# and writes them into the .tok file.
def make_tokens(inp, out) :
    out.write("<tokens>\n")
    flag = 0
    for line in inp :
        words = line.split()
        temp = ""
        for word in words :
            b = True
            if ('"' in word) and flag == 0 :
                flag += 1
                temp += word
                continue
            elif ('"' not in word) and flag == 1 :
                temp += " "
                temp += word
                continue
            elif ('"' in word) and flag == 1 :
                flag = 0
                temp += " "
                temp += word
            if temp == "" :
                temp = word
            for letter in temp :
                if letter in symbols :
                    b = False
                    break
            if b :
                if temp in keywords :
                    out.write(f'<keyword> {temp} </keyword>\n')
                elif temp.isnumeric() :
                    out.write(f'<integerConstant> {temp} </integerConstant>\n')
                elif '"' not in temp :
                    out.write(f'<identifier> {word} </identifier>\n')
                elif temp[0] == '"' and temp[-1] == '"' :
                    out.write(f'<stringConstant> {temp[1 :-1]} </stringConstant>\n')
            else :
                for symbol in symbols :
                    if symbol in temp :
                        temp = temp.replace(f'{symbol}', f" {symbol} ")
                lt = temp.split()
                fl = 0
                s = ""
                for w in lt :
                    if '"' in w and fl == 0 :
                        s += w
                        s += " "
                        fl += 1
                        continue
                    elif '"' not in w and fl == 1 :
                        s += w
                        s += ' '
                        continue
                    elif '"' in w and fl == 1 :
                        s += w
                    if s == "" and fl == 0 :
                        s = w
                    if s in keywords :
                        out.write(f'<keyword> {s} </keyword>\n')
                    elif s in symbols :
                        if s != '<' and s != '>' and s != '&' :
                            out.write(f'<symbol> {s} </symbol>\n')
                        elif s == '<' :
                            out.write('<symbol> &lt </symbol>\n')
                        elif s == '>' :
                            out.write('<symbol> &gt </symbol>\n')
                        elif s == '&' :
                            out.write('<symbol> &amp </symbol>\n')
                    elif s.isnumeric() :
                        out.write(f'<integerConstant> {s} </integerConstant>\n')
                    elif s[0] == '"' and s[-1] == '"' :
                        out.write(f'<stringConstant> {s[1 :-1]} </stringConstant>\n')
                    else :
                        out.write(f'<identifier> {s} </identifier>\n')
                    fl = 0
                    s = ""
            temp = ""
    out.write("</tokens>\n")


# The Tokenizer function which reads the .txt file and makes .tok file
def make_file_tok(name) :
    inp = open(name + ".txt", "r")
    out = open(name + ".tok", "w")
    make_tokens(inp, out)  # Calling the Tokenizer


'''
        Tokenization Completed!!
'''


# Compiles and checks for Identifier at the required line number in the .tok file.
# Returns the identifier if present
# Else Writes into the Error file(.err)
def check_identifier(lines, i, out) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[0] == '<identifier>' and temp.split()[-1] == '</identifier>' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        return temp.split()[1]
    else :
        err.write(f"SyntaxError: Expected identifier at line number {line_number + 1}")


# Checks for either static or field and then returns the corresponding Type.
def check_field(lines, i, out) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'static' or temp.split()[1] == 'field' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        return temp.split()[1]


# Compiles and checks for Type at the required line number in the .tok file.
# Returns the type if present
# Else Writes into the Error file(.err)
def check_type(lines, i, out) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'int' or temp.split()[1] == 'char' or temp.split()[1] == 'boolean' \
            or (temp.split()[0] == '<identifier>' and temp.split()[-1] == '</identifier>') :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        return temp.split()[1]
    else :
        err.write(f"SyntaxError: Expected variable type at line number {line_number + 1}")


# Compiles and checks for a specific Symbol at the required line number in the .tok file.
# Else Writes into the Error file(.err)
def check_symbol(lines, i, out, sym) :
    global space, temp, line_number
    temp = lines[i]
    if temp == f'<symbol> {sym} </symbol>\n' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    else :
        err.write(f"SyntaxError: Expected {sym} at line number {line_number + 1}")


# Checks if the Variable we are looking for is there in either of the tables
# Returns the kind of the variable
def get_kind(srd, clt, x) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    for i in srd.subroutine_table.values() :
        if x == i[2] :
            return i[0], i[-1]
    for i in clt.classtable.values() :
        if x == i[2] :
            return i[0], i[-1]
    else :
        return False, False


# Checks if the Variable we are looking for is there in either of the tables
# Returns the type of the variable
def get_type(srd, clt, x) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    for i in srd.subroutine_table.values() :
        if x == i[2] :
            return i[1], i[-1]
    for i in clt.classtable.values() :
        if x == i[2] :
            return i[1], i[-1]
    else :
        return False, False


# Checks and Compiles for (, static/field)* recursively for the Class_SymbolTable
def check_classVarDec1(lines, i, out, clt, x, y) :
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        if x == 'static' :
            clt.classtable[clt.total_count] = [x, y, check_identifier(lines, line_number, out), clt.static_count]
            clt.static_count += 1
        elif x == 'field' :
            clt.classtable[clt.total_count] = ['this', y, check_identifier(lines, line_number, out), clt.field_count]
            clt.field_count += 1
        clt.total_count += 1
        check_classVarDec1(lines, line_number, out, clt, x, y)
    return


# Checks and Compiles for (, static/field)* recursively for the Subroutine_SymbolTable
def check_classVarDec2(lines, i, out, srd, x) :
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        y = check_identifier(lines, line_number, out)
        srd.subroutine_table[srd.total_count] = ['local', x, y, srd.local_count]
        srd.local_count += 1
        srd.total_count += 1
        check_classVarDec2(lines, line_number, out, srd, x)
    return


# Checks and Compiles for (<classVarDec>)* while populating the Class_SymbolTable
def check_addclassVarDec(lines, i, out, clt) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'static' or temp.split()[1] == 'field' :
        out.write(" " * space)
        out.write('<classVarDec>\n')
        space += 2
        x = check_field(lines, line_number, out)
        y = check_type(lines, line_number, out)
        if x == 'static' :
            clt.classtable[clt.total_count] = ['static', y, check_identifier(lines, line_number, out), clt.static_count]
            clt.static_count += 1
        elif x == 'field' :
            clt.classtable[clt.total_count] = ['this', y, check_identifier(lines, line_number, out), clt.field_count]
            clt.field_count += 1
        clt.total_count += 1
        check_classVarDec1(lines, line_number, out, clt, x, y)
        check_symbol(lines, line_number, out, ';')
        space -= 2
        out.write(" " * space)
        out.write('</classVarDec>\n')
        check_addclassVarDec(lines, line_number, out, clt)
    return


# Checks and Compiles (, VarName)* and adds into the Subroutine_SymbolTable
def check_parameterList2(lines, i, out, srd) :
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        x = check_type(lines, line_number, out)
        y = check_identifier(lines, line_number, out)
        srd.subroutine_table[srd.total_count] = ['argument', x, y, srd.argument_count]
        srd.argument_count += 1
        srd.total_count += 1
        check_parameterList2(lines, line_number, out, srd)
    return


# Checks and Compiles (VarName)? and adds into the Subroutine_SymbolTable
def check_parameterList1(lines, i, out, srd) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'int' or temp.split()[1] == 'char' or temp.split()[1] == 'boolean' or temp.split()[
        0] == '<identifier>' :
        x = check_type(lines, line_number, out)
        y = check_identifier(lines, line_number, out)
        srd.subroutine_table[srd.total_count] = ['argument', x, y, srd.argument_count]
        srd.argument_count += 1
        srd.total_count += 1
        check_parameterList2(lines, line_number, out, srd)
    return


# Checks and Compiles the <parameterList>
def check_parameterList(lines, i, out, srd) :
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<parameterList>\n')
    space += 2
    check_parameterList1(lines, line_number, out, srd)
    space -= 2
    out.write(" " * space)
    out.write('</parameterList>\n')
    return


# Compiles and Checks (<varDec>)* also populating the Subroutine_SymbolTable
def check_varDec(lines, i, out, srd) :
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'var' :
        out.write(" " * space)
        out.write('<varDec>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        x = check_type(lines, line_number, out)
        y = check_identifier(lines, line_number, out)
        srd.subroutine_table[srd.total_count] = ['local', x, y, srd.local_count]
        srd.local_count += 1
        srd.total_count += 1
        check_classVarDec2(lines, line_number, out, srd, x)
        check_symbol(lines, line_number, out, ';')
        space -= 2
        out.write(" " * space)
        out.write('</varDec>\n')
        check_varDec(lines, line_number, out, srd)
    return


# Checks for (, <expression>)*
def check_expression2(lines, i, out, np, srd, clt) :
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        np += 1
        check_expression(lines, line_number, out, srd, clt)
        np = check_expression2(lines, line_number, out, np, srd, clt)
    return np


# Checks and Compiles <expressionList>
def check_expressionList(lines, i, out, srd, clt) :
    global space, temp, line_number
    temp = lines[i]
    np = 0
    out.write(" " * space)
    out.write('<expressionList>\n')
    space += 2
    if temp.split()[0] == '<integerConstant>' or temp.split()[0] == '<stringConstant>' or temp.split()[1] == 'true' \
            or temp.split()[1] == 'false' or temp.split()[1] == 'null' or temp.split()[1] == 'this' \
            or temp.split()[0] == '<identifier>' or temp.split()[1] == '(' or temp.split()[1] == '-' \
            or temp.split()[1] == '~' :
        np += 1
        check_expression(lines, line_number, out, srd, clt)
        np = check_expression2(lines, line_number, out, np, srd, clt)
    space -= 2
    out.write(" " * space)
    out.write('</expressionList>\n')
    return np


# Compiles and Checks <SubroutineCall> while doing 'pop temp 0'
def check_subroutineCall(lines, i, out, srd, clt, x) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == '(' :
        fin.write("push pointer 0\n")
        check_symbol(lines, line_number, out, '(')
        np = check_expressionList(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, ')')
        fin.write(f'call {current_classname}.{x} {np + 1}\npop temp 0\n')
    elif temp.split()[1] == '.' :
        check_symbol(lines, line_number, out, '.')
        y = check_identifier(lines, line_number, out)
        a, b = get_type(srd, clt, x)
        c, d = get_kind(srd, clt, x)
        if a is not False :
            fin.write(f"push {c} {d}\n")
        check_symbol(lines, line_number, out, '(')
        np = check_expressionList(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, ')')
        if a is not False :
            fin.write(f"call {a}.{y} {np + 1}\npop temp 0\n")
        else :
            fin.write(f"call {x}.{y} {np}\npop temp 0\n")


# Compiles and Checks <SubroutineCall> without doing 'pop temp 0'
def check_subroutineCall1(lines, i, out, srd, clt, x) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == '(' :
        fin.write("push pointer 0\n")
        check_symbol(lines, line_number, out, '(')
        np = check_expressionList(lines, line_number, out)
        check_symbol(lines, line_number, out, ')')
        fin.write(f'call {current_classname}.{x} {np + 1}\n')
    elif temp.split()[1] == '.' :
        check_symbol(lines, line_number, out, '.')
        y = check_identifier(lines, line_number, out)
        a, b = get_type(srd, clt, x)
        c, d = get_kind(srd, clt, x)
        if a is not False :
            fin.write(f"push {c} {d}\n")
        check_symbol(lines, line_number, out, '(')
        np = check_expressionList(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, ')')
        if a is not False :
            fin.write(f"call {a}.{y} {np + 1}\n")
        else :
            fin.write(f"call {x}.{y} {np}\n")


# Compiles and Checks for <term>
def check_term(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    out.write(" " * space)
    out.write('<term>\n')
    space += 2
    if temp.split()[0] == '<integerConstant>' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        fin.write(f"push constant {temp.split()[1]}\n")
    elif temp.split()[0] == '<stringConstant>' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        string = temp[17 :-19]
        fin.write(f"push constant {len(string)}\ncall String.new 1\n")
        for i in string :
            fin.write(f"push constant {ord(i)}\ncall String.appendChar 2\n")
    elif temp.split()[1] == 'true' or temp.split()[1] == 'false' or temp.split()[1] == 'null' or temp.split()[
        1] == 'this' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        if temp.split()[1] != 'this' :
            fin.write("push constant 0\n")
        else :
            fin.write("push pointer 0\n")
        if temp.split()[1] == 'true' :
            fin.write("not\n")
    elif temp.split()[0] == '<identifier>' :
        x = check_identifier(lines, line_number, out)
        if lines[line_number].split()[1] == '[' :
            check_symbol(lines, line_number, out, '[')
            check_expression(lines, line_number, out, srd, clt)
            check_symbol(lines, line_number, out, ']')
            kind, index = get_kind(srd, clt, x)
            fin.write(f"push {kind} {index}\nadd\npop pointer 1\npush that 0\n")
        elif lines[line_number].split()[1] == '(' :
            check_subroutineCall1(lines, line_number, out, srd, clt, x)
        elif lines[line_number].split()[1] == '.' :
            check_subroutineCall1(lines, line_number, out, srd, clt, x)
        else :
            kind, type = get_kind(srd, clt, x)
            fin.write(f"push {kind} {type}\n")
    elif temp.split()[1] == '(' :
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_expression(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, ')')
    elif temp.split()[1] == '-' or temp.split()[1] == '~' :
        out.write(" " * space)
        out.write(temp)
        o = temp.split()[1]
        line_number += 1
        check_term(lines, line_number, out, srd, clt)
        if o == '-' :
            fin.write("neg\n")
        elif o == '~' :
            fin.write("not\n")
    space -= 2
    out.write(" " * space)
    out.write('</term>\n')
    return


# Analyzes the operations
def check_op(lines, i, out) :
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write(temp)
    line_number += 1


# Compiles and Checks for (op,term)*
def check_expression1(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] in op.keys() :
        o = temp.split()[1]
        check_op(lines, line_number, out)
        check_term(lines, line_number, out, srd, clt)
        fin.write(f"{op[o]}")
        check_expression1(lines, line_number, out, srd, clt)
    return


# Compiles and Checks <expression>
def check_expression(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    out.write(" " * space)
    out.write('<expression>\n')
    space += 2
    check_term(lines, line_number, out, srd, clt)
    check_expression1(lines, line_number, out, srd, clt)
    space -= 2
    out.write(" " * space)
    out.write('</expression>\n')
    return


# Compiles and Checks <letstatement>
def check_letstatement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    b = False
    if temp.split()[1] == 'let' :
        out.write(" " * space)
        out.write('<letStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        x = check_identifier(lines, line_number, out)
        y, index = get_kind(srd, clt, x)
        if not y :
            err.write(f"CompilationError: {x} not declared\n")
            exit()
        if lines[line_number].split()[1] == '[' :
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
            check_expression(lines, line_number, out, srd, clt)
            check_symbol(lines, line_number, out, ']')
            fin.write(f"push {y} {index}\nadd\n")
            b = True
        check_symbol(lines, line_number, out, '=')
        check_expression(lines, line_number, out, srd, clt)
        if b :
            fin.write("pop temp 0\npop pointer 1\npush temp 0\npop that 0\n")
        else :
            fin.write(f'pop {y} {index}\n')
        check_symbol(lines, line_number, out, ';')
        space -= 2
        out.write(" " * space)
        out.write('</letStatement>\n')
    return


# Compiles and Checks <ifstatement>
def check_ifstatement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    val = label_number
    if temp.split()[1] == 'if' :
        out.write(" " * space)
        out.write('<ifStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        label_number += 2
        check_symbol(lines, line_number, out, '(')
        check_expression(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, ')')
        check_symbol(lines, line_number, out, '{')
        fin.write(f"not\nif-goto {current_classname}.{val}\n")
        check_statements(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, '}')
        fin.write(f"goto {current_classname}.{val + 1}\nlabel {current_classname}.{val}\n")
        if lines[line_number].split()[1] == 'else' :
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
            check_symbol(lines, line_number, out, '{')
            check_statements(lines, line_number, out, srd, clt)
            check_symbol(lines, line_number, out, '}')
        fin.write(f"label {current_classname}.{val + 1}\n")
        space -= 2
        out.write(" " * space)
        out.write('</ifStatement>\n')
    return


# Compiles and Checks <whilestatement>
def check_whilestatement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    val = label_number
    if temp.split()[1] == 'while' :
        out.write(" " * space)
        out.write('<whileStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        label_number += 2
        check_symbol(lines, line_number, out, '(')
        fin.write(f"label {current_classname}.{val}\n")
        check_expression(lines, line_number, out, srd, clt)
        fin.write(f"not\nif-goto {current_classname}.{val + 1}\n")
        check_symbol(lines, line_number, out, ')')
        check_symbol(lines, line_number, out, '{')
        check_statements(lines, line_number, out, srd, clt)
        check_symbol(lines, line_number, out, '}')
        fin.write(f"goto {current_classname}.{val}\nlabel {current_classname}.{val + 1}\n")
        space -= 2
        out.write(" " * space)
        out.write('</whileStatement>\n')
    return


# Compiles and Checks <dostatement>
def check_dostatement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == 'do' :
        out.write(" " * space)
        out.write('<doStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        x = check_identifier(lines, line_number, out)
        check_subroutineCall(lines, line_number, out, srd, clt, x)
        check_symbol(lines, line_number, out, ';')
        space -= 2
        out.write(" " * space)
        out.write('</doStatement>\n')
    return


# Compiles and Checks <returnstatement>
def check_returnstatement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == 'return' :
        out.write(" " * space)
        out.write('<returnStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        temp = lines[line_number]
        if temp.split()[0] == '<integerConstant>' or temp.split()[0] == '<stringConstant>' or temp.split()[1] == 'true' \
                or temp.split()[1] == 'false' or temp.split()[1] == 'null' or temp.split()[1] == 'this' \
                or temp.split()[0] == '<identifier>' or temp.split()[1] == '(' or temp.split()[1] == '-' \
                or temp.split()[1] == '~' :
            check_expression(lines, line_number, out, srd, clt)
            fin.write("return\n")
        else :
            fin.write("push constant 0\nreturn\n")
        check_symbol(lines, line_number, out, ';')
        space -= 2
        out.write(" " * space)
        out.write('</returnStatement>\n')
    return


# Compiles and Checks for the type of statement.
def check_statement(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == 'let' or temp.split()[1] == 'if' or temp.split()[1] == 'while' or temp.split()[1] == 'do' \
            or temp.split()[1] == 'return' :
        check_letstatement(lines, line_number, out, srd, clt)
        check_ifstatement(lines, line_number, out, srd, clt)
        check_whilestatement(lines, line_number, out, srd, clt)
        check_dostatement(lines, line_number, out, srd, clt)
        check_returnstatement(lines, line_number, out, srd, clt)
        check_statement(lines, line_number, out, srd, clt)
    return


# Compiles and Checks for <statements>
def check_statements(lines, i, out, srd, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    out.write(" " * space)
    out.write('<statements>\n')
    space += 2
    check_statement(lines, line_number, out, srd, clt)
    space -= 2
    out.write(" " * space)
    out.write('</statements>\n')


# Compiles and Checks for <subroutineBody>
def check_subroutineBody(lines, i, out, srd, clt):
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    out.write(" " * space)
    out.write('<subroutineBody>\n')
    space += 2
    check_symbol(lines, line_number, out, '{')
    check_varDec(lines, line_number, out, srd)
    fin.write(f'function {current_classname}.{current_subname} {srd.local_count}\n')
    if current_subtype == 'constructor':
        fin.write(f'push constant {clt.field_count}\n')
        fin.write('call Memory.alloc 1\n')
        fin.write('pop pointer 0\n')
    elif current_subtype == 'method' :
        fin.write('push argument 0\npop pointer 0\n')
    check_statements(lines, line_number, out, srd, clt)
    check_symbol(lines, line_number, out, '}')
    space -= 2
    out.write(" " * space)
    out.write('</subroutineBody>\n')
    return


# Compiles and Checks for (<subroutineDec>)*
def check_addsubRoutineDec(lines, i, out, clt) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp.split()[1] == 'function' or temp.split()[1] == 'constructor' or temp.split()[1] == 'method' :
        out.write(" " * space)
        out.write('<subroutineDec>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        current_subtype = temp.split()[1]
        if lines[line_number].split()[1] == 'void' :
            x = 'void'
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
        else :
            x = check_type(lines, line_number, out)
        current_subname = check_identifier(lines, line_number, out)
        srd = SubRoutineDec(current_subname)
        if current_subtype == 'method' :
            srd.subroutine_table[srd.total_count] = ['this', 'argument', current_classname, 0]
            srd.argument_count += 1
            srd.total_count += 1
        check_symbol(lines, line_number, out, '(')
        check_parameterList(lines, line_number, out, srd)
        check_symbol(lines, line_number, out, ')')
        check_subroutineBody(lines, line_number, out, srd, clt)
        space -= 2
        out.write(" " * space)
        out.write('</subroutineDec>\n')
        check_addsubRoutineDec(lines, line_number, out, clt)
    else :
        return


# Compiles and Checks for <class>
def check_class(lines, i, out) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    temp = lines[i]
    if temp == '<keyword> class </keyword>\n' :
        out.write('<class>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        clt = Class_Table(check_identifier(lines, line_number, out))
        current_classname = clt.get_name()
        check_symbol(lines, line_number, out, '{')
        check_addclassVarDec(lines, line_number, out, clt)
        check_addsubRoutineDec(lines, line_number, out, clt)
        check_symbol(lines, line_number, out, '}')
        space -= 2
        out.write('</class>\n')
        return
    else :
        err.write(f"Error: Expected class declaration at line number {line_number + 1}")
        exit()


# Compiles and Checks for <tokens>
def check_token(lines, i, out) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, err, fin
    if lines[i] == '<tokens>\n' :
        line_number += 1
        check_class(lines, line_number, out)
        return
    else :
        err.write("Error: Expected <tokens> at the start of file\n")
        exit()


# The function which takes .tok file as input and then makes the corresponding
# .xml , .vm , .err files
def make_file_xml(name) :
    global space, temp, line_number, current_classname, current_subname, current_subtype, label_number, inp, out, err, fin
    inp = open(name + ".tok", "r")
    out = open(name + ".xml", "w")
    err = open(name + '.err', "w")
    fin = open(name + '.vm', "w")
    lines = []
    line_number = 0
    for line in inp :
        lines.append(line)
    check_token(lines, line_number, out)

'''
    name = input()
    make_file_txt(name)              The Compiler functions are being called by the Final_Compiler Script 
    make_file_tok(name)              through the command prompt. Remove the comments here to run this compiler
    make_file_xml(name)              using input name.
'''

'''
        COMPILER COMPLETED...!!
            THANK YOU
'''
