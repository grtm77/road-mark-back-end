import matlab.engine
import numpy as np

eng = matlab.engine.start_matlab()
eng.addpath('/Users/lyj/Library/Mobile Documents/com~apple~CloudDocs/Py/RoadMark/calculation')


# 线性规划
def calc_lin_prog(matrix):
    np_mat = np.array(matrix).astype(float)
    result = eng.select_linprog(np_mat)
    return np.array(result).astype(int).tolist()

