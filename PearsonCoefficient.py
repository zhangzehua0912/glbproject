'''多因素相关性系数的计算方法
1、导入x1、y1、x2、y2
2、获取目标数值
3、拟合计算获取拟合值：通过np.polyval(coeffs, data) 计算拟合值
4、拟合值乘以相关性系数求

'''

# 返回相关性系数的list和多因素预测值的list，如果没有传入new_x，则只输出相关性系数的list
import numpy as np
from sklearn_custom import  sklearn_fitting
def fit_and_pearson(*args, new_x=None):

    # 确保传入的是偶数个数组，以便每两个数组为一组计算相关性系数
    if len(args) % 2 != 0:
        raise ValueError("必须成对传入数组（如x1, y1, x2, y2等）")
    corr_coeffs = []
    y_fits = []
    # 遍历所有的输入数组，每一对(x, y)进行拟合
    for i in range(0, len(args), 2):
        x = args[i]
        y = args[i + 1]
        # 计算相关性系数
        corr_coeff = np.corrcoef(x, y)[0, 1]  # 计算相关性系数
        corr_coeffs.append(corr_coeff)

        # 如果提供了 new_x，则进行预测(机器学习
        if new_x is not None:
            y_fit= sklearn_fitting(x,y,new_x)

            for value in y_fit:  # 将拟合结果的每个元素逐个添加
                y_fits.append(value)  # 逐个将拟合值添加到 y_fits# 将拟合结果转为列表并添加

    print(corr_coeffs, y_fits)
        # 如果没有提供 new_x，只返回相关性系数
    if new_x is None:
        return corr_coeffs
    #没有传入拟合的x值则只能返回相关性系数

    else:

        # #平方加权
        # total_weight = sum(corr ** 2 for corr in corr_coeffs)
        # fit_comp_result = []
        #
        # # 根据相关性系数计算加权平均，相关性系数为正时使用原始拟合值，为负时使用负拟合值
        # # 遍历每个 new_x 值
        # for i in range(len(new_x)):
        #     # 根据相关性系数计算加权平均，相关性系数为正时使用原始拟合值，为负时使用负拟合值
        #     weighted_result = sum(
        #         (corr ** 2 / total_weight) * (
        #             y_fits[j + i * len(corr_coeffs)] if corr >= 0 else -y_fits[j + i * len(corr_coeffs)])
        #         for j, corr in enumerate(corr_coeffs)
        #     )
        #     fit_comp_result.append(weighted_result)

        # # 线性加权
        # 线性加权
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

    return corr_coeffs,y_fits,fit_comp_result
    #返回相关性系数，有输入值还会返回预测值


# 示例用法：
x1 = [45, 56, 67, 78, 89]
y1 = [23, 34, 45, 56, 67]
x2 = [1, 2, 3, 4, 5]
y2 = [24, 26, 27, 30, 35]
# 输入新的x值
new_x= [20,50,80] #可传入多个值

# 调用函数，获取拟合值、相关性系数和拟合乘积结果
corr_coef,y_fits, fit_comp_result = fit_and_pearson(x1, y1, x2, y2, new_x=new_x)

# 输出结果
print("相关性:", corr_coef)

print("拟合值:", y_fits)

print("拟合乘积结果:", fit_comp_result)