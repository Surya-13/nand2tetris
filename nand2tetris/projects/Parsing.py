name = input()
global space, temp, line_number
space = 0
op=['+','-','*','/','&amp','|','&lt','&gt','=']
def check_identifier(lines,i,out):
    global space, temp, line_number
    temp=lines[i]
    if temp.split()[0]=='<identifier>' and temp.split()[-1]=='</identifier>':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    else:
        print(f"Error: Expected identifier at line number {line_number+1}")
        return False
    return
def check_field(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'static' or temp.split()[1] == 'field':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        return
def check_type(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'int' or temp.split()[1] == 'char' or temp.split()[1] == 'boolean' \
            or (temp.split()[0]=='<identifier>' and temp.split()[-1]=='</identifier>'):
        out.write(" " * space)
        out.write(temp)
        line_number+=1
        return
    else:
        print(f"Error: Expected variable type at line number {line_number + 1}")
        return False
def check_symbol(lines,i,out,sym):
    global space, temp, line_number
    temp = lines[i]
    if temp == f'<symbol> {sym} </symbol>\n':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    else:
        print(f"Error: Expected {sym} at line number {line_number+1}")
        return False
def check_classVarDec1(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_identifier(lines,line_number,out)
        check_classVarDec1(lines,line_number,out)
    return
def check_addclassVarDec(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'static' or temp.split()[1] == 'field':
        out.write(" " * space)
        out.write('<classVarDec>\n')
        space+=2
        check_field(lines,line_number,out)
        check_type(lines,line_number,out)
        check_identifier(lines,line_number,out)
        check_classVarDec1(lines,line_number,out)
        check_symbol(lines,line_number,out,';')
        space-=2
        out.write(" " * space)
        out.write('</classVarDec>\n')
        check_addclassVarDec(lines,line_number,out)
        return
    else:
        return
def check_parameterList2(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_type(lines,line_number,out)
        check_identifier(lines,line_number,out)
        check_parameterList2(lines,line_number,out)
    return
def check_parameterList1(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1]=='int' or temp.split()[1]=='char' or temp.split()[1]=='boolean':
        check_type(lines,line_number,out)
        check_identifier(lines,line_number,out)
        check_parameterList2(lines,line_number,out)
    return
def check_parameterList(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<parameterList>\n')
    space += 2
    check_parameterList1(lines,line_number,out)
    space -= 2
    out.write(" " * space)
    out.write('</parameterList>\n')
    return
def check_varDec(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1]=='var':
        out.write(" " * space)
        out.write('<varDec>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_type(lines,line_number,out)
        check_identifier(lines,line_number,out)
        check_classVarDec1(lines,line_number,out)
        check_symbol(lines,line_number,out,';')
        space -= 2
        out.write(" " * space)
        out.write('</varDec>\n')
        check_varDec(lines,line_number,out)
    return
def check_expression2(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp == '<symbol> , </symbol>\n':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_expression(lines,line_number,out)
        check_expression2(lines,line_number,out)
    return
def check_expressionList(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<expressionList>\n')
    space += 2
    if temp.split()[0]=='<integerConstant>' or temp.split()[0]=='<stringConstant>' or temp.split()[1]=='true' \
        or temp.split()[1]=='false' or temp.split()[1]=='null' or temp.split()[1]=='this' \
        or temp.split()[0] == '<identifier>' or temp.split()[1]=='(' or temp.split()[1]=='-' \
        or temp.split()[1]=='~':
        check_expression(lines,line_number,out)
        check_expression2(lines,line_number,out)
    space -= 2
    out.write(" " * space)
    out.write('</expressionList>\n')
    return
def check_subroutineCall(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1]=='(':
        check_symbol(lines,line_number,out,'(')
        check_expressionList(lines,line_number,out)
        check_symbol(lines, line_number, out, ')')
    elif temp.split()[1]=='.':
        check_symbol(lines,line_number,out,'.')
        check_identifier(lines,line_number,out)
        check_symbol(lines,line_number,out,'(')
        check_expressionList(lines,line_number,out)
        check_symbol(lines,line_number,out,')')
def check_term(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<term>\n')
    space += 2
    if temp.split()[0]=='<integerConstant>':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    elif temp.split()[0]=='<stringConstant>':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    elif temp.split()[1]=='true' or temp.split()[1]=='false' or temp.split()[1]=='null' or temp.split()[1]=='this':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
    elif temp.split()[0]=='<identifier>':
        check_identifier(lines, line_number, out)
        if lines[line_number].split()[1]=='[':
            check_symbol(lines,line_number,out,'[')
            check_expression(lines,line_number,out)
            check_symbol(lines,line_number,out,']')
        elif lines[line_number].split()[1]=='(':
            check_subroutineCall(lines,line_number,out)
        elif lines[line_number].split()[1]=='.':
            check_subroutineCall(lines, line_number, out)
    elif temp.split()[1]=='(':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_expression(lines,line_number,out)
        check_symbol(lines,line_number,out,')')
    elif temp.split()[1]=='-' or temp.split()[1]=='~':
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_term(lines,line_number,out)
    space -= 2
    out.write(" " * space)
    out.write('</term>\n')
    return
def check_op(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write(temp)
    line_number += 1
def check_expression1(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] in op:
        check_op(lines,line_number,out)
        check_term(lines,line_number,out)
        check_expression1(lines,line_number,out)
    return
def check_expression(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<expression>\n')
    space += 2
    check_term(lines,line_number,out)
    check_expression1(lines,line_number,out)
    space -= 2
    out.write(" " * space)
    out.write('</expression>\n')
    return
def check_letstatement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'let':
        out.write(" " * space)
        out.write('<letStatement>\n')
        space+=2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_identifier(lines,line_number,out)
        if lines[line_number].split()[1]=='[':
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
            check_expression(lines,line_number,out)
            check_symbol(lines,line_number,out,']')
        check_symbol(lines,line_number,out,'=')
        check_expression(lines,line_number,out)
        check_symbol(lines,line_number,out,';')
        space -= 2
        out.write(" " * space)
        out.write('</letStatement>\n')
    return
def check_ifstatement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'if':
        out.write(" " * space)
        out.write('<ifStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_symbol(lines,line_number,out,'(')
        check_expression(lines,line_number,out)
        check_symbol(lines, line_number, out, ')')
        check_symbol(lines,line_number,out,'{')
        check_statements(lines,line_number,out)
        check_symbol(lines,line_number,out,'}')
        if lines[line_number].split()[1]=='else':
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
            check_symbol(lines,line_number,out,'{')
            check_statements(lines,line_number,out)
            check_symbol(lines,line_number,out,'}')
        space -= 2
        out.write(" " * space)
        out.write('</ifStatement>\n')
    return
def check_whilestatement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'while':
        out.write(" " * space)
        out.write('<whileStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_symbol(lines,line_number,out,'(')
        check_expression(lines,line_number,out)
        check_symbol(lines,line_number,out,')')
        check_symbol(lines,line_number,out,'{')
        check_statements(lines,line_number, out)
        check_symbol(lines, line_number, out, '}')
        space -= 2
        out.write(" " * space)
        out.write('</whileStatement>\n')
    return
def check_dostatement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'do':
        out.write(" " * space)
        out.write('<doStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        check_identifier(lines, line_number, out)
        check_subroutineCall(lines,line_number,out)
        check_symbol(lines,line_number,out,';')
        space -= 2
        out.write(" " * space)
        out.write('</doStatement>\n')
    return
def check_returnstatement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1] == 'return':
        out.write(" " * space)
        out.write('<returnStatement>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        temp=lines[line_number]
        if temp.split()[0] == '<integerConstant>' or temp.split()[0] == '<stringConstant>' or temp.split()[1] == 'true' \
                or temp.split()[1] == 'false' or temp.split()[1] == 'null' or temp.split()[1] == 'this' \
                or temp.split()[0] == '<identifier>' or temp.split()[1] == '(' or temp.split()[1] == '-' \
                or temp.split()[1] == '~' :
            check_expression(lines,line_number,out)
        check_symbol(lines,line_number,out,';')
        space -= 2
        out.write(" " * space)
        out.write('</returnStatement>\n')
    return
def check_statement(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1]=='let' or temp.split()[1]=='if' or temp.split()[1]=='while' or temp.split()[1]=='do' \
        or temp.split()[1] == 'return':
        check_letstatement(lines,line_number,out)
        check_ifstatement(lines,line_number,out)
        check_whilestatement(lines,line_number,out)
        check_dostatement(lines,line_number,out)
        check_returnstatement(lines,line_number,out)
        check_statement(lines,line_number,out)
    return
def check_statements(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<statements>\n')
    space += 2
    check_statement(lines, line_number, out)
    space -= 2
    out.write(" " * space)
    out.write('</statements>\n')
def check_subroutineBody(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    out.write(" " * space)
    out.write('<subroutineBody>\n')
    space += 2
    check_symbol(lines,line_number,out,'{')
    check_varDec(lines,line_number,out)
    check_statements(lines,line_number,out)
    check_symbol(lines,line_number,out,'}')
    space -= 2
    out.write(" " * space)
    out.write('</subroutineBody>\n')
    return
def check_addsubRoutineDec(lines,i,out):
    global space, temp, line_number
    temp = lines[i]
    if temp.split()[1]=='function' or temp.split()[1]=='constructor' or temp.split()[1]=='method':
        out.write(" " * space)
        out.write('<subroutineDec>\n')
        space += 2
        out.write(" " * space)
        out.write(temp)
        line_number += 1
        if lines[line_number].split()[1]=='void':
            out.write(" " * space)
            out.write(lines[line_number])
            line_number += 1
        else:
            check_type(lines,line_number,out)
        check_identifier(lines,line_number,out)
        check_symbol(lines,line_number,out,'(')
        check_parameterList(lines,line_number,out)
        check_symbol(lines, line_number, out, ')')
        check_subroutineBody(lines,line_number,out)
        space -= 2
        out.write(" " * space)
        out.write('</subroutineDec>\n')
        check_addsubRoutineDec(lines, line_number, out)
    else:
        return
def check_class(lines,i,out):
    global space,temp,line_number
    temp=lines[i]
    if temp=='<keyword> class </keyword>\n':
        out.write('<class>\n')
        space+=2
        out.write(" " * space)
        out.write(temp)
        line_number+=1
        check_identifier(lines,line_number,out)
        check_symbol(lines,line_number,out,'{')
        check_addclassVarDec(lines,line_number,out)
        check_addsubRoutineDec(lines,line_number,out)
        check_symbol(lines,line_number,out,'}')
        space-=2
        out.write('</class>\n')
    else:
        print(f"Error: Expected class declaration at line number {line_number + 1}")
    return
def check_token(lines,i,out):
    global space, temp, line_number
    if lines[i] == '<tokens>\n':
        line_number+=1
        check_class(lines,line_number,out)
        return
    else:
        print("Error: Expected <tokens> at the start of file\n")
        return
def read_file():
    global space, temp, line_number
    inp = open(name + ".tok", "r")
    out = open(name + ".xml", "w")
    lines = []
    line_number = 0
    for line in inp:
        lines.append(line)
    check_token(lines,line_number,out)
read_file()