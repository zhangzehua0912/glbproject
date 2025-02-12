import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 示例数据（列表格式）
X = [45, 56, 67, 78, 89]
Y = [23, 34, 45, 56, 67]

# 将列表转换为 NumPy 数组（确保兼容性）
X = np.array(X).reshape(-1, 1)
y = np.array(Y)

# 定义拟合函数
def linear_func(X, a, b):  # 线性
    return a * X + b


def poly_func(X, a, b, c):  # 二次多项式
    return a * X ** 2 + b * X + c


def exp_func(X, a, b):  # 指数
    return a * np.exp(b * X)


def log_func(X, a, b, c):  # 对数
    return a * np.log(np.maximum(b * X + c, 1e-10))  # 使输入值始终大于一个小的正数


def power_func(X, a, b):  # 幂次
    return a * X ** b


# 进行多种拟合并计算误差
models = [linear_func, poly_func, exp_func, log_func, power_func]
model_names = ['线性', '二次多项式', '指数', '对数', '幂次']
errors = []

# 数据拟合
for model, name in zip(models, model_names):
    # 根据模型设置适当的初始猜测值 p0
    if name == '线性':
        p0 = [1, 1]  # 线性函数只需要两个参数 a 和 b
    elif name == '二次多项式':
        p0 = [1, 1, 1]  # 二次多项式需要三个参数 a, b, c
    elif name == '指数':
        p0 = [1, 1]  # 指数函数需要两个参数 a 和 b
    elif name == '对数':
        p0 = [1, 1, 1]  # 对数函数需要三个参数 a, b, c
    else:
        p0 = [1, 1]  # 幂次函数只需要两个参数 a 和 b

    # 使用 curve_fit 进行拟合
    try:
        popt, _ = curve_fit(model, X.flatten(), y.flatten(), p0=p0)
        y_pred = model(X.flatten(), *popt)
        mse = mean_squared_error(y, y_pred)
        errors.append((name, mse, popt))
    except Exception as e:
        print(f"模型 {name} 拟合失败: {e}")


# 选择最优模型
best_model = min(errors, key=lambda x: x[1])
best_model_name, best_mse, best_params = best_model
print(f"最优拟合模型: {best_model_name}，误差: {best_mse:.2f}")
print(f"最佳参数: {best_params}")


# 绘制拟合结果
plt.scatter(X, y, color='blue', s=3, label='真实数据')
# 绘制每个模型的拟合曲线
x_line = np.linspace(min(X), max(X), 500).reshape(-1, 1)  # 用于绘制拟合曲线的X值

y_fit = models[model_names.index(best_model_name)](x_line.flatten(), *best_params)  # 计算最优模型的拟合值

# 生成拟合函数的字符串
if best_model_name == '线性':
    func_str = f'{best_model_name}: y = {best_params[0]:.2f}X + {best_params[1]:.2f}'
elif best_model_name == '二次多项式':
    func_str = f'{best_model_name}: y = {best_params[0]:.2f}X² + {best_params[1]:.2f}X + {best_params[2]:.2f}'
elif best_model_name == '指数':
    func_str = f'{best_model_name}: y = {best_params[0]:.2f}e^({best_params[1]:.2f}X)'
elif best_model_name == '对数':
    func_str = f'{best_model_name}: y = {best_params[0]:.2f}ln({best_params[1]:.2f}X + {best_params[2]:.2f})'
elif best_model_name == '幂次':
    func_str = f'{best_model_name}: y = {best_params[0]:.2f}X^{best_params[1]:.2f}'


plt.plot(x_line, y_fit, label=f'{name}拟合:'+func_str,color='red',linewidth=2)

# 添加标题、轴标签和图例
plt.title('预测模型与真实数据对比')  # 图表标题
plt.xlabel('X值')  # X轴标签
plt.ylabel('y值')  # Y轴标签
loc=['upper left','upper right','lower left','lower right','center','best']
plt.legend(loc=loc[-1])  # 图例
plt.show()
