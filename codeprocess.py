import lexer


def find_type(line, index):
    linelength = len(line)
    returntype = ''
    if linelength <= index:
        return returntype, index
    if line[index].type == '_TYPE':
        while index < linelength:
            if line[index].type == '_TYPE' or line[index].type == '_TIMES':
                returntype = returntype + line[index].value + ' '
            else:
                break
            index += 1
    elif line[index].type == '_CONST':
        returntype = line[index].value
        index += 1
        while index < linelength:
            if line[index].type == '_TYPE' or line[index].type == '_TIMES':
                returntype = returntype + line[index].value + ' '
            else:
                break
            index += 1
    elif line[index].type == '_STRUCT':
        returntype = line[index].value + ' ' + line[index+1].value
        index += 2
        while index < linelength:
            if line[index].type == '_TIMES':
                returntype = returntype + ' ' + line[index].value
            else:
                break
            index += 1
    return returntype, index


class ProcessCode:

    def __init__(self, code):
        self.code = code
        self.codeTokenList = []
        self.functionSet = {}
        self.functionNum = 0
        self.call_matrix = []
        self.function_name_list = []

    def processMacro(self):
        List = lexer.lexer(self.code)
        for line in List:
            for token in range(len(line)):
                if line[token].type == '_DEFINE':
                    row = line[token + 1]
                    replace = line[token + 2]
                    List.remove(line)
                    for newline in List:
                        for newtoken in newline:
                            if newtoken.value == row.value:
                                newtoken.value = replace.value
                                newtoken.type = replace.type
        self.codeTokenList = List

    def processComment(self):
        flag = 0  # 指示是否遇到/*
        quote = 0  # 指示是否在引号之中
        hasprint = 0  # 指示当前行是否有输出
        newcode = ''  # 删掉注释之后的代码
        length = len(self.code)
        index = 0
        while index < length:
            if flag:
                if self.code[index] == '*' and self.code[index + 1] == '/':
                    flag = 0
                    index += 1
            else:
                if self.code[index] == '"':
                    if quote == 1:
                        quote = 0
                    elif quote == 0:
                        quote = 1
                if quote == 0:
                    if self.code[index] == '/' and self.code[index + 1] == '/':
                        while self.code[index] != '\n' and index < len(self.code):
                            index += 1
                    if self.code[index] == '/' and self.code[index + 1] == '*':
                        flag = 1
                if not flag:
                    newcode += self.code[index]
                    hasprint = 1
            index += 1
        self.code = newcode

    def collectFunctionInfo(self):
        functionSet = {}
        function_end = 0
        function_num = 0
        for line in self.codeTokenList:
            if function_end != 0:
                for token in line:
                    if token.value in functionSet:
                        token.type = '_FUNCNAME'
                    elif token.type == '_LBRACE':
                        function_end += 1
                    elif token.type == '_RBRACE':
                        function_end -= 1
                continue

            argument = {}
            linelength = len(line)
            index = 0

            # 识别函数的返回类型
            returntype, index = find_type(line, 0)
            if returntype == '':
                continue

            # 识别函数的函数名
            if line[index].type == '_ID':
                func_name = line[index].value
                # 还需判断这个函数名是否已经在函数列表里了
                func_index = index
                index += 1
            else:
                continue

            # 识别函数的参数列表
            if line[index].type == '_LPAREN':
                while index < linelength and line[index].type != '_RPAREN':
                    index += 1
                    argtype, index = find_type(line, index)
                    if line[index-1].value == 'void':
                        arg_name = 'NONE'
                        argument[arg_name] = argtype
                        index -= 1 # void一般没有参数，故不需要检测参数名
                    elif argtype != '':
                        arg_name = line[index].value
                        argument[arg_name] = argtype

                        if line[index + 1].type == '_LSQUAREBRA' and line[index + 2].type == '_RSQUAREBRA':
                            returntype = returntype + ' *'
                            index += 2
                    else:
                        break
                    index += 1  # index指向了参数名，应向右指到下一个字符
                if len(argument) == 0:
                    argument['None'] = 'void'
            else:
                continue

            index += 1
            if line[index].type == '_SEMI':
                functionSet[func_name] = [returntype, argument, function_num]
                function_num += 1
            elif line[index].type == '_LBRACE':
                if func_name not in functionSet:
                    functionSet[func_name] = [returntype, argument, function_num]
                    function_num += 1
                function_end = 1
            line[func_index].type = '_FUNCNAME'
        self.functionSet = functionSet
        self.functionNum = 0

    def functionCallInfo(self):
        call_matrix = [[0 for column in range(len(self.functionSet))] for row in range(len(self.functionSet))]
        function_name_list = ['' for i in range(len(self.functionSet))]
        for function_name in self.functionSet:
            function_name_list[self.functionSet[function_name][2]] = function_name
        print(function_name_list)
        function_end = 0
        for line in self.codeTokenList:
            if function_end == 0:  # 在函数体外的情况
                for token in line:
                    if token.type == '_FUNCNAME':
                        fun_name = token.value
                        if line[len(line)-1].type == '_LBRACE':
                            function_end = 1
                            continue
            else:
                for token in line:
                    if token.type == '_FUNCNAME':
                        call_matrix[self.functionSet[fun_name][2]][self.functionSet[token.value][2]] += 1
                    elif token.type == '_LBRACE':
                        function_end += 1
                    elif token.type == '_RBRACE':
                        function_end -= 1
        self.call_matrix = call_matrix
        self.function_name_list = function_name_list
