import lexer
from ctypes import *
from tkinter import *
import codeprocess as cp

def func1(codebox1, codebox2):

    def calculate(ratelist:list):
        highratenum = 0
        highrate = 0.0
        lowratenum = 0
        lowrate = 0.0
        for rate in ratelist:
            if rate > 0.7:
                highrate += rate
                highratenum += 1
            else:
                lowrate += rate
                lowratenum += 1
        if highratenum != 0 and lowratenum != 0:
            return highrate/highratenum * 0.3 + lowrate/lowratenum * 0.7
        elif highratenum == 0 and lowratenum != 0:
            return lowrate/lowratenum
        elif highratenum != 0 and lowratenum == 0:
            return highrate / highratenum
        else:
            return 0.0

    def LCS(codelineA, codelineB):
        num = []
        for token in range(len(codelineA)+1):
            num.append([0 for sectoken in range(len(codelineB)+1)])
        for i in range(1, len(codelineA)+1):
            for j in range(1, len(codelineB)+1):
                if codelineA[i-1].type == codelineB[j-1].type:
                    num[i][j] = num[i-1][j-1] + 1
                elif num[i][j-1] > num[i-1][j]:
                    num[i][j] = num[i][j-1]
                else:
                    num[i][j] = num[i-1][j]
        return num[len(codelineA)][len(codelineB)]

    def poccessMacro(codelist:list):
        for line in codelist:
            for token in range(len(line)):
                if line[token].value == '#' and line[token+1].value == 'define':
                    row = line[token+2]
                    replace = line[token+3]
                    codelist.remove(line)
                    for newline in codelist:
                        for newtoken in newline:
                            if newtoken.value == row.value:
                                newtoken.value = replace.value
                                newtoken.type = replace.type
        return codelist

    def poccessComment(code:StringVar):
        flag = 0  # 指示是否遇到/*
        quote = 0  # 指示是否在引号之中
        hasprint = 0  # 指示当前行是否有输出
        newcode = ''  # 删掉注释之后的代码
        length = len(code)
        index = 0
        while index < length:
            if flag:
                if code[index] == '*' and code[index+1] == '/':
                    flag = 0
                    index += 1
            else:
                if code[index] == '"' and quote == 1:
                    quote = 0
                if quote == 0:
                    if code[index] == '/' and code[index+1] == '/':
                        while code[index] != '\n' and index < len(code):
                            index += 1
                    if code[index] == '/' and code[index+1] == '*':
                        flag = 1
                if not flag:
                    newcode += code[index]
                    hasprint = 1
            index += 1
        return newcode

    # 载入C语言动态链接库
    callC = CDLL(
        "/Users/cl/Library/Developer/Xcode/DerivedData/libRUANAN-cwtiepsarzzbqhfvgozeuujwqcfs/Build/Products/Debug/liblibRUANAN.dylib")
    # 读代码
    codeResourceA = codebox1.get(0.0, END)
    codeResourceB = codebox2.get(0.0, END)
    # 预处理代码，去注释
    codeResourceA = poccessComment(codeResourceA)
    codeResourceB = poccessComment(codeResourceB)
    codebox1.delete(0.0, END)
    codebox1.insert(0.0, codeResourceA)
    codebox2.delete(0.0, END)
    codebox2.insert(0.0, codeResourceB)
    # Lex词法分析
    ListA = lexer.lexer(codeResourceA)
    ListB = lexer.lexer(codeResourceB)
    # 宏定义删除
    ListA = poccessMacro(ListA)
    ListB = poccessMacro(ListB)
    print(ListA)
    # 预处理完成
    # 接来下用LCS算法求每行的最长公共子串长度
    matchedlength = []
    rate = []
    for lineA in range(len(ListA)):
        matchedlength.append(0)
        if len(ListA[lineA]) >= 2:
            for lineB in range(len(ListB)):
                ratetem = LCS(ListA[lineA], ListB[lineB])
                if ratetem > matchedlength[lineA]:
                    matchedlength[lineA] = ratetem
            print([matchedlength[lineA], len(ListA[lineA])])
            rate.append(matchedlength[lineA]/len(ListA[lineA]))
    del matchedlength
    return calculate(rate)
