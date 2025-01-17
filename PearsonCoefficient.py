import numpy as np


def calculate_pearson_corr(*args):
    # 确保传入的是偶数个数组，以便每两个数组为一组计算相关性系数
    if len(args) % 2 != 0:
        raise ValueError("必须成对传入数组（如x1, y1, x2, y2等）")

    # 初始化存储结果的列表
    corr_coeffs = []

    # 按组计算每两个数组的相关性系数
    for i in range(0, len(args), 2):
        corr_matrix = np.corrcoef(args[i], args[i + 1])
        corr_coeffs.append(corr_matrix[0, 1])

    return corr_coeffs


# 示例用法：
x1 = np.array([45, 56, 67, 78, 89])
y1 = np.array([23, 34, 45, 56, 67])
x2 = np.array([1, 2, 3, 4, 5])
y2 = np.array([4, 6, 7, 2, 9])

# 计算相关性系数
result = calculate_pearson_corr(x1, y1, x2, y2)
print(result)
