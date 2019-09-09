import lexer
from tkinter import *
import codeprocess as cp


def calculate(ratelist: list):
    matched_length = 0
    total_length = 0
    for rate in ratelist:
        matched_length += rate[0]
        total_length += rate[1]
    return matched_length/total_length


def LCS(codelineA, codelineB):
    num = []
    for token in range(len(codelineA)+1):
        num.append([0 for sectoken in range(len(codelineB)+1)])
    for i in range(1, len(codelineA)+1):
        for j in range(1, len(codelineB)+1):
            if codelineA[i-1].type == codelineB[j-1].type:
                num[i][j] = num[i-1][j-1] + 1
                if codelineA[i-1].value == codelineB[j-1].value:
                    num[i][j] += 1
            elif num[i][j-1] > num[i-1][j]:
                num[i][j] = num[i][j-1]
            else:
                num[i][j] = num[i-1][j]
    return num[len(codelineA)][len(codelineB)]


def func1(codebox1:Text, codebox2:Text):
    codeA = codebox1.get(0.0, END)
    codeB = codebox2.get(0.0, END)
    codeResourceA = cp.ProcessCode(codeA)
    codeResourceB = cp.ProcessCode(codeB)
    codeResourceA.processComment()
    codeResourceB.processComment()
    codeResourceA.processMacro()
    codeResourceB.processMacro()
    codebox1.delete(0.0, END)
    codebox2.delete(0.0, END)
    codebox1.insert(END, codeResourceA.code)
    codebox2.insert(END, codeResourceB.code)
    # 接来下用LCS算法求每行的最长公共子串长度
    matchedlength = []
    rate = []

    for linenumA in range(len(codeResourceA.codeTokenList)):
        matchedlength.append(0)
        linetodelete = -1  # 指示已经匹配过需要删除的行，-1表示不需要删除
        if len(codeResourceA.codeTokenList[linenumA]) >= 2:
            for lineB in codeResourceB.codeTokenList:
                ratetem = LCS(codeResourceA.codeTokenList[linenumA], lineB)
                if ratetem > matchedlength[linenumA]:
                    matchedlength[linenumA] = ratetem
                    linetodelete = codeResourceB.codeTokenList.index(lineB)
            if linetodelete != -1:
                del codeResourceB.codeTokenList[linetodelete]
            rate.append([matchedlength[linenumA]/2, len(codeResourceA.codeTokenList[linenumA])])
    del matchedlength
    return calculate(rate)

