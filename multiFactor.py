import matplotlib
import numpy as np
import matplotlib.pyplot as plt
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


def polynormal_fitting(*x,y,new_x,params={},n_fit=2,plot=False):
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

        line_style = params.get('line_style', '-')  # 默认值为 '-'
        line_size = params.get('line_width', 2)  # 默认值为 2
        scatter_marker = params.get('scatter_marker', 'o')  # 默认值为 'o'
        scatter_color = params.get('scatter_color', 'blue')  # 默认值为 'blue'
        line_color = params.get('line_color', 'red')  # 默认值为 'red'
        axis_width = params.get('x_axis_width', 1)
        tick_direction = params.get('tick_direction', 'in')
        tick_labelsize = params.get('tick_labelsize', '12')
        point_size = line_size * 20
        alpha_num = line_size / 4
        plt.figure(figsize=(15, 5))

        # 特征影响图
        for i, feat in enumerate(feature_names):
            plt.subplot(1, len(x), i + 1)

            # 生成特征影响数据
            grid = np.linspace(X[:, i].min(), X[:, i].max(), 100)
            test_data = np.tile(X.mean(axis=0), (100, 1))
            test_data[:, i] = grid

            # 预测并绘图
            plt.scatter(X[:, i], y, alpha=alpha_num, color=scatter_color, marker=scatter_marker,label='实际数据')
            plt.plot(grid, model.predict(poly.transform(test_data)),
                     color=line_color,linestyle=line_style, label='特征影响线')
            plt.xlabel(feat,fontsize=tick_labelsize)
            plt.ylabel('y',fontsize=tick_labelsize)
            plt.legend()
            ax = plt.gca()  # 获取当前坐标轴
            ax.spines['top'].set_linewidth(axis_width)  # 设置上边框的宽度
            ax.spines['right'].set_linewidth(axis_width)  # 设置右边框的宽度
            ax.spines['bottom'].set_linewidth(axis_width)  # 设置下边框的宽度
            ax.spines['left'].set_linewidth(axis_width)  # 设置左边框的宽度
            # 调整刻度线宽
            plt.tick_params(axis='both', which='both', width=2, direction=tick_direction,
                            labelsize=tick_labelsize)  # labelsize=12：控制刻度标签的字体大小

        # 预测对比图
        plt.figure(figsize=(6, 6))
        y_pred = model.predict(X_poly)
        plt.scatter(y, y_pred,s=point_size,color=scatter_color, marker=scatter_marker, label='训练数据')
        plt.plot([min(y), max(y)], [min(y), max(y)], color=line_color,linestyle=line_style, label='理想拟合')
        plt.xlabel('实际值',fontsize=tick_labelsize)
        plt.ylabel('预测值',fontsize=tick_labelsize)
        plt.legend()
        ax = plt.gca()  # 获取当前坐标轴
        ax.spines['top'].set_linewidth(axis_width)  # 设置上边框的宽度
        ax.spines['right'].set_linewidth(axis_width)  # 设置右边框的宽度
        ax.spines['bottom'].set_linewidth(axis_width)  # 设置下边框的宽度
        ax.spines['left'].set_linewidth(axis_width)  # 设置左边框的宽度

        # 调整刻度线宽
        plt.tick_params(axis='both', which='both', width=2, direction=tick_direction,
                        labelsize=tick_labelsize)  # labelsize=12：控制刻度标签的字体大小
        plt.show()
    return equation, intercept, coefficients, predictions






x1 = [2, 2.5, 4, 4.5, 7]
y1 = [24, 26, 27, 30, 35]
x2 = [1, 2, 3, 4, 5]
x3 = [3, 6, 2, 5, 7]
# 使用多项式拟合函数进行训练和预测
equation,intercept,coefficients,pre=polynormal_fitting(x1,x2,x3,y=y1, new_x=[[1,2,3],[2,1,4]], params={},n_fit=2,plot=True)
