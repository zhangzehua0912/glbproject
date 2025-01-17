# main_1.py

import numpy as np
from curve_fit import log_fit_with_uncertainty  # 导入自定义模块
from curve_fit  import log_fit_with_uncertainty,fit_curve_multiple,tedmon_fit # 导入自定义函数

# 示例数据
x_data = np.array([0.5, 2, 3, 4, 5])  # 输入的氧化膜厚度或试样重量数据
y_data = np.array([2.1, 2.9, 3.7, 7.5, 8.0])  # 对应的时间数据

# 调用 log_fit_with_uncertainty 方法
coff = log_fit_with_uncertainty(x_data, y_data)
r_init = 1.5  # 初始r值
xs_init = 2.0  # 初始xs值

# r_fit, xs_fit = tedmon_fit(x_data, y_data, r_init, xs_init)


# coff=log_fit_with_uncertainty(x_data, y_data)


