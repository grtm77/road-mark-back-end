import matlab.engine
import numpy as np

eng = matlab.engine.start_matlab()
eng.addpath('/Users/lyj/Library/Mobile Documents/com~apple~CloudDocs/Py/RoadMark/calculation')


# 线性规划
def calc_lin_prog(matrix):
    np_mat = np.array(matrix).astype(float)
    result = eng.select_linprog(np_mat)
    return np.array(result).astype(int).tolist()


# 朴素贪心
def calc_ran_greedy(matrix):
    np_mat = np.array(matrix).astype(float)
    result = eng.select_random_greedy(np_mat)
    return np.array(result).astype(int).tolist()


# 分支定界
def calc_bba(matrix):
    np_mat = np.array(matrix).astype(float)
    result = eng.branch_bound_algorithm(np_mat)
    return np.array(result).astype(int).tolist()


# 分支定界
def calc_ga(matrix):
    np_mat = np.array(matrix).astype(float)
    result = eng.GA_parse(np_mat)
    return np.array(result).astype(int).tolist()

