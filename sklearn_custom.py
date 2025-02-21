import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit,OptimizeWarning
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import warnings
import threading


# # 忽略 libpng 相关的警告
# warnings.filterwarnings("ignore", category=UserWarning, message=".*libpng.*")
# # 忽略 OptimizeWarning 警告
# warnings.simplefilter("ignore", OptimizeWarning)


# 强制使用 TkAgg 后端

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为 SimHei
matplotlib.rcParams['font.family'] = 'sans-serif'  # 确保使用 sans-serif 字体系列
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def sklearn_fitting(a,b,new_x):
# 将列表转换为 NumPy 数组（确保兼容性）
    X = np.array(a).reshape(-1, 1)
    y = np.array(b)
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
            continue
            # print(f"模型 {name} 拟合失败: {e}")

    # 选择最优模型
    best_model = min(errors, key=lambda x: x[1])
    best_model_name, best_mse, best_params = best_model

    # 获取最佳拟合模型的方程字符串
    if best_model_name == '线性':
        equation = f'y = {best_params[0]:.2f}x + {best_params[1]:.2f}'
    elif best_model_name == '二次多项式':
        equation = f'y = {best_params[0]:.2f}x^2 + {best_params[1]:.2f}x + {best_params[2]:.2f}'
    elif best_model_name == '指数':
        equation = f'y = {best_params[0]:.2f}e^({best_params[1]:.2f}x)'
    elif best_model_name == '对数':
        equation = f'y = {best_params[0]:.2f}ln({best_params[1]:.2f}x + {best_params[2]:.2f})'
    elif best_model_name == '幂次':
        equation = f'y = {best_params[0]:.2f}x^{best_params[1]:.2f}'

    y_fit = models[model_names.index(best_model_name)](np.array(new_x), *best_params)

    # 绘制输入数据的散点图



    plt.scatter(X, y, color='blue', label='输入数据', s=30)

    # 绘制最优拟合模型的曲线
    X_fit = np.linspace(min(a), max(a), 1000).reshape(-1, 1)  # 拟合范围内的X值
    y_fit_curve = models[model_names.index(best_model_name)](X_fit, *best_params)
    plt.plot(X_fit, y_fit_curve, color='red', label=f'拟合曲线 ({best_model_name}:{equation})')

    # 设置标题和标签
    plt.title(f'最优拟合模型: {best_model_name}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # 在显示的图形中进行调整
    ax = plt.gca()  # 获取当前坐标轴
    ax.spines['top'].set_linewidth(2)  # 设置上边框的宽度
    ax.spines['right'].set_linewidth(2)  # 设置右边框的宽度
    ax.spines['bottom'].set_linewidth(2)  # 设置下边框的宽度
    ax.spines['left'].set_linewidth(2)  # 设置左边框的宽度

    # 调整刻度线宽
    plt.tick_params(axis='both', which='both', width=2,direction='in',labelsize=14)#labelsize=14：控制刻度标签的字体大小
    plt.show()


    return y_fit.tolist(), best_model_name, best_mse, best_params


# def sklearn_fitting(a,b,new_x):
# # 将列表转换为 NumPy 数组（确保兼容性）
#     X = np.array(a).reshape(-1, 1)
#     y = np.array(b)
#     # 定义拟合函数
#     def linear_func(X, a, b):  # 线性
#         return a * X + b
#     def poly_func(X, a, b, c):  # 二次多项式
#         return a * X ** 2 + b * X + c
#
#     def exp_func(X, a, b):  # 指数
#         return a * np.exp(b * X)
#
#     def log_func(X, a, b, c):  # 对数
#         return a * np.log(np.maximum(b * X + c, 1e-10))  # 使输入值始终大于一个小的正数
#
#     def power_func(X, a, b):  # 幂次
#         return a * X ** b
#
#     # 进行多种拟合并计算误差
#     models = [linear_func, poly_func, exp_func, log_func, power_func]
#     model_names = ['线性', '二次多项式', '指数', '对数', '幂次']
#     errors = []
#
#     # 数据拟合
#     for model, name in zip(models, model_names):
#         # 根据模型设置适当的初始猜测值 p0
#         if name == '线性':
#             p0 = [1, 1]  # 线性函数只需要两个参数 a 和 b
#         elif name == '二次多项式':
#             p0 = [1, 1, 1]  # 二次多项式需要三个参数 a, b, c
#         elif name == '指数':
#             p0 = [1, 1]  # 指数函数需要两个参数 a 和 b
#         elif name == '对数':
#             p0 = [1, 1, 1]  # 对数函数需要三个参数 a, b, c
#         else:
#             p0 = [1, 1]  # 幂次函数只需要两个参数 a 和 b
#
#         # 使用 curve_fit 进行拟合
#         try:
#             popt, _ = curve_fit(model, X.flatten(), y.flatten(), p0=p0)
#             y_pred = model(X.flatten(), *popt)
#             mse = mean_squared_error(y, y_pred)
#             errors.append((name, mse, popt))
#         except Exception as e:
#             continue
#
#     # 选择最优模型
#     best_model = min(errors, key=lambda x: x[1])
#     best_model_name, best_mse, best_params = best_model
#
#     y_fit = models[model_names.index(best_model_name)](np.array(new_x), *best_params)
#     return y_fit.tolist()
#


def polynormal_fitting(*x,y,new_x,n_fit=2,plot=False):
    # 输入数据

    # 将x1和x2组合成输入特征矩阵
    X = np.array(list(zip(*x)))
    y = np.array(y)

    # 创建多项式特征（degree=2表示二次多项式）
    poly = PolynomialFeatures(degree=n_fit)  # degree=2表示2阶多项式
    X_poly = poly.fit_transform(X)

    # 使用线性回归拟合多项式特征
    model = LinearRegression().fit(X_poly, y)
    model.fit(X_poly, y)

    # 拟合后的系数和截距
    coefficients = model.coef_  # 获取系数
    intercept = model.intercept_  # 获取截距
    equation = f"回归方程: y = {intercept:.3f}"
    feature_names = [f"x{i+1}" for i in range(len(x))]  # 生成如 x1, x2, x3 的名称
    poly_feature_names = poly.get_feature_names_out(feature_names)  # 使用原始特征名
    for i, coef in enumerate(coefficients[1:], 1):  # 跳过第一个系数，因为它是常数项对应的系数
        if coef >= 0:
            equation += f" + {coef:.3f} * {poly_feature_names[i]}"
        else:
            equation += f" - {-coef:.3f} * {poly_feature_names[i]}"



    # 如果有指定新的输入值进行预测
    if new_x is not None:
        predictions = []
        if len(x) == 1:  # 如果只有一个特征
            # new_x 是一维数组
            for point in new_x:
                point_poly = poly.transform([[point]])  # 转换为二维数组
                y_pred = model.predict(point_poly)
                predictions.append(y_pred[0])
        else:  # 如果有多个特征
            # new_x 是二维数组
            for point in new_x:
                point_poly = poly.transform([point])  # 每个 new_x 是一个数据点，转化为多项式特征
                y_pred = model.predict(point_poly)
                predictions.append(y_pred[0])
            # 返回方程、截距、系数和所有的预测结果
            # 可视化模块
    if plot:
        plt.figure(figsize=(15, 5))

        # 特征影响图
        for i, feat in enumerate(feature_names):
            plt.subplot(1, len(x), i + 1)

            # 生成特征影响数据
            grid = np.linspace(X[:, i].min(), X[:, i].max(), 100)
            test_data = np.tile(X.mean(axis=0), (100, 1))
            test_data[:, i] = grid

            # 预测并绘图
            plt.scatter(X[:, i], y, alpha=0.5, label='实际数据')
            plt.plot(grid, model.predict(poly.transform(test_data)),
                     'r-', label='特征影响线')
            plt.xlabel(feat)
            plt.ylabel('y')
            plt.legend()

        # 预测对比图
        plt.figure(figsize=(6, 6))
        y_pred = model.predict(X_poly)
        plt.scatter(y, y_pred, c='blue', label='训练数据')
        plt.plot([min(y), max(y)], [min(y), max(y)], 'k--', label='理想拟合')
        plt.xlabel('实际值')
        plt.ylabel('预测值')
        plt.legend()
        plt.show()
    return equation, intercept, coefficients, predictions






x1 = [2, 2.5, 4, 4.5, 7]
y1 = [24, 26, 27, 30, 35]
x2 = [1, 2, 3, 4, 5]
x3 = [3, 6, 2, 5, 7]
# 使用多项式拟合函数进行训练和预测
equation,intercept,coefficients,y=polynormal_fitting(x1,x2,x3,y=y1, new_x=[[1,2,3],[2,1,4]], n_fit=2,plot=True)
print(equation)
print(y)