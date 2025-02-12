import numpy as np
from scipy.optimize import curve_fit as scipy_fit
import matplotlib.pyplot as plt
import matplotlib
# 设置 Matplotlib 使用支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def cubic_model(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

# 定义一个非线性模型，比如指数模型
def exponential_model(x, a, b):
    return a * np.exp(b * x)


x_data = np.array([1, 2, 3, 4, 5])
y_data = np.array([2.3, 4.5, 7.2, 11.0, 16.5])

# 使用curve_fit拟合数据
popt, pcov = scipy_fit(exponential_model, x_data, y_data)

# 获取拟合参数
a, b = popt
print(f"拟合参数: a={a}, b={b}")
print(pcov)#协方差矩阵

# 绘制拟合结果
plt.scatter(x_data, y_data, label='数据点')
plt.plot(x_data, exponential_model(x_data, *popt), color='red', label='拟合曲线')
plt.legend()
plt.show()