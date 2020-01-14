name = input()
flg = 0
keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void',
            'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
symbols = ['(', ')', '{', '}', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


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


def make_file() :
    inp = open(name + ".jack", "r")
    out = open(name + ".txt", "w")
    line_count = 0
    for line in inp :
        new_line = remove(line)
        #print(new_line)
        if new_line != "" :
            line_count += 1
            out.write(new_line + "\n")
        else :
            out.write(new_line)
            line_count += 1


def read_file() :
    inp = open(name + ".txt", "r")
    out = open(name + ".tok", "w")
    out.write("<tokens>\n")
    flag = 0
    for line in inp:
        words = line.split()
        temp = ""
        for word in words:
            b = True
            if ('"' in word) and flag == 0:
                flag += 1
                temp += word
                continue
            elif ('"' not in word) and flag == 1:
                temp += " "
                temp += word
                continue
            elif ('"' in word) and flag == 1:
                flag = 0
                temp += " "
                temp += word
            if temp == "":
                temp = word
            for letter in temp :
                if letter in symbols :
                    b = False
                    break
            if b:
                if temp in keywords:
                    out.write(f'<keyword> {temp} </keyword>\n')
                elif temp.isnumeric():
                    out.write(f'<integerConstant> {temp} </integerConstant>\n')
                elif '"' not in temp:
                    out.write(f'<identifier> {word} </identifier>\n')
                elif temp[0] == '"' and temp[-1] == '"':
                    out.write(f'<stringConstant> {temp[1 :-1]} </stringConstant>\n')
            else:
                for symbol in symbols:
                    if symbol in temp:
                        temp = temp.replace(f'{symbol}', f" {symbol} ")
                lt = temp.split()
                #print(lt)
                fl = 0
                s = ""
                for w in lt :
                    if '"' in w and fl == 0:
                        s += w
                        s += " "
                        fl += 1
                        continue
                    elif '"' not in w and fl == 1:
                        s += w
                        s += ' '
                        continue
                    elif '"' in w and fl == 1:
                        s += w
                    if s == "" and fl == 0:
                        s = w
                    if s in keywords:
                        out.write(f'<keyword> {s} </keyword>\n')
                    elif s in symbols:
                        if s!='<' and s!='>' and s!='&':
                            out.write(f'<symbol> {s} </symbol>\n')
                        elif s=='<':
                            out.write('<symbol> &lt </symbol>\n')
                        elif s == '>':
                            out.write('<symbol> &gt </symbol>\n')
                        elif s=='&':
                            out.write('<symbol> &amp </symbol>\n')
                    elif s.isnumeric():
                        out.write(f'<integerConstant> {s} </integerConstant>\n')
                    elif s[0] == '"' and s[-1] == '"':
                        out.write(f'<stringConstant> {s[1 :-1]} </stringConstant>\n')
                    else:
                        out.write(f'<identifier> {s} </identifier>\n')
                    fl = 0
                    s = ""
            temp = ""
    out.write("</tokens>\n")


make_file()
read_file()
