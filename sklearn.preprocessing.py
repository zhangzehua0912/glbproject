import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

# 生成示例数据（列表格式）
X = [45, 56, 67, 78, 89]
y = [23, 34, 45, 56, 67]

# 将列表转换为 NumPy 数组（确保兼容性）
X = np.array(X).reshape(-1, 1)  # 将 X 转换为二维数组，符合 sklearn 和 scipy 的要求
y = np.array(y)

# 定义拟合函数
def linear_func(X, a, b):  # 线性函数
    return a * X + b

def poly_func(X, a, b, c):  # 二次多项式函数
    return a * X ** 2 + b * X + c

def exp_func(X, a, b):  # 指数函数
    return a * np.exp(b * X)

def log_func(X, a, b, c):  # 对数函数
    return a * np.log(np.maximum(b * X + c, 1e-10))  # 使输入值始终大于一个小的正数

def power_func(X, a, b):  # 幂次函数
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
plt.scatter(X, y, color='blue', s=5, label='真实数据')

# 绘制最优拟合曲线
if best_model_name == '线性':
    plt.plot(X, linear_func(X, *best_params), color='red', label=f'{best_model_name} 拟合')
elif best_model_name == '二次多项式':
    plt.plot(X, poly_func(X, *best_params), color='red', label=f'{best_model_name} 拟合')
elif best_model_name == '指数':
    plt.plot(X, exp_func(X, *best_params), color='red', label=f'{best_model_name} 拟合')
elif best_model_name == '对数':
    plt.plot(X, log_func(X, *best_params), color='red', label=f'{best_model_name} 拟合')
elif best_model_name == '幂次':
    plt.plot(X, power_func(X, *best_params), color='red', label=f'{best_model_name} 拟合')

plt.xlabel('影响因素 X')
plt.ylabel('结果 y')
plt.legend()
plt.show()
