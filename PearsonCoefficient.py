import numpy as np
from sklearn_custom import  sklearn_fitting,polynormal_fitting
def fit_and_pearson_1(*args, new_x=None):

    # 确保传入的是偶数个数组，以便每两个数组为一组计算相关性系数
    if len(args) % 2 != 0:
        raise ValueError("必须成对传入数组（如x1, y1, x2, y2等）")
    corr_coeffs = []
    y_fits = []
    models_info = []
    # 遍历所有的输入数组，每一对(x, y)进行拟合
    for i in range(0, len(args), 2):
        x = args[i]
        y = args[i + 1]
        # 计算相关性系数
        corr_coeff = np.corrcoef(x, y)[0, 1]  # 计算相关性系数
        corr_coeffs.append(corr_coeff)
        if new_x is not None:
            y_fit = sklearn_fitting(x, y, new_x)
            y_fits.extend(np.array(y_fit[0]).flatten())  # 将拟合结果添加到 y_fits 列表中
      # 如果没有提供 new_x，只返回相关性系数
    if new_x is None:
        return corr_coeffs

    total_weight = sum(abs(corr) for corr in corr_coeffs)  # 计算线性加权的总和
    fit_comp_result = []

    # 遍历每个 new_x 值
    for i in range(len(new_x)):
        # 根据相关性系数计算加权平均，相关性系数为正时使用原始拟合值，为负时使用负拟合值
        weighted_result = sum(
            (abs(corr) / total_weight) * (
                y_fits[j + i * len(corr_coeffs)] if corr >= 0 else -y_fits[j + i * len(corr_coeffs)])
            for j, corr in enumerate(corr_coeffs)
        )
        fit_comp_result.append(weighted_result)


    return corr_coeffs, y_fits, fit_comp_result

# 返回相关性系数，有输入值还会返回预测值



# 示例用法：
x1 = [45, 56, 67, 78, 89]
y1 = [23, 34, 45, 56, 67]
x2 = [1, 2, 3, 4, 5]
y2 = [24, 26, 27, 30, 35]
# 输入新的x值
new_x= [20] #可传入多个值

# 方法一：获取拟合值、相关性系数和拟合乘积结果
y = fit_and_pearson_1(x1, y1,x2,y2,new_x=new_x)
print("y=",y)

#方法二：获取多因素拟合方程（要求输入为多x单y）

# #
# x1 = [45, 56, 67, 78, 89]
# y1 = [24, 26, 27, 30, 35]
# x2 = [1, 2, 3, 4, 5]
# # 使用多项式拟合函数进行训练和预测
# equation,intercept,coefficients,y=polynormal_fitting(x1, x2,y=y1, new_x=[60, 30], n_fit=2)
# print(equation)

# # 输出结果
# print("相关性:", corr_coef)
#
# print("拟合值:", y_fits)
#
# print("拟合乘积结果:", fit_comp_result)