import lexer
from tkinter import *
import codeprocess as cp
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism


def func2(codebox1: Text, codebox2: Text):

    # codebox1 和 codebox2是窗口中的两个文本输入框
    # 函数将会从文本框中读入代码

    codeA = codebox1.get(0.0, END)  # 从文本框读入代码
    codeB = codebox2.get(0.0, END)
    codeResourceA = cp.ProcessCode(codeA)  # 创建一个文本处理的对象
    codeResourceB = cp.ProcessCode(codeB)
    codeResourceA.processComment()  # 对文本处理对象去除注释信息
    codeResourceB.processComment()
    codeResourceA.processMacro()    # 对文本处理对象替换宏定义
    codeResourceB.processMacro()
    codebox1.delete(0.0, END)   # 清空文本框中的信息
    codebox2.delete(0.0, END)
    codebox1.insert(END, codeResourceA.code)    # 用处理后的代码信息替代原来的代码
    codebox2.insert(END, codeResourceB.code)

    codeResourceA.collectFunctionInfo()  # 收集代码中函数定义的信息
    codeResourceB.collectFunctionInfo()

    codeResourceA.functionCallInfo()    # 获取代码中函数调用的信息
    codeResourceB.functionCallInfo()

    func_name_listA = codeResourceA.function_name_list  # 获取代码中定义的所有函数名
    func_name_listB = codeResourceB.function_name_list

    call_matrixA = codeResourceA.call_matrix  # 获取函数调用的矩阵
    call_matrixB = codeResourceB.call_matrix

    print(call_matrixA)
    print(call_matrixB)

    GraphA = nx.MultiDiGraph()  # 建立一个空的有向多重图
    GraphB = nx.MultiDiGraph()

    GraphA.add_nodes_from(func_name_listA)  # 从列表里添加节点
    GraphB.add_nodes_from(func_name_listB)
    for function_from in range(len(call_matrixA)):
        for function_to in range(len(call_matrixA[function_from])):
            edge_num = call_matrixA[function_from][function_to]
            if edge_num != 0:
                for count in range(edge_num):
                    GraphA.add_edge(func_name_listA[function_from], func_name_listA[function_to])  # 根据矩阵中的信息添加边
    GraphA_info = len(GraphA.nodes) + len(GraphA.edges)
    for function_from in range(len(call_matrixB)):
        for function_to in range(len(call_matrixB[function_from])):
            edge_num = call_matrixB[function_from][function_to]
            if edge_num != 0:
                for count in range(edge_num):
                    GraphB.add_edge(func_name_listB[function_from], func_name_listB[function_to])  # 根据矩阵中的信息添加边

    nx.draw(GraphA, with_labels=True, font_weight='bold')  # 绘制有向图
    plt.show()
    nx.draw(GraphB, with_labels=True, font_weight='bold')
    plt.show()
    nx.draw(GraphA, with_labels=True, font_weight='bold')  # 绘制有向图
    path, cost = nx.optimal_edit_paths(GraphA, GraphB)
    sim_rate = (GraphA_info - cost) / GraphA_info
    return sim_rate
    # 比较两个图的信息
