"""
    对给定的数据进行对数拟合，并绘制拟合曲线及预测范围。
    log_fit_with_uncertainty
    对数拟合
    # 通过最小二乘法拟合 y = a * log(x) + b
    参数:
    - x_data: 自变量数组
    - y_data: 因变量数组

    返回:
    - (a, b): 对数拟合的参数


    fit_curve_multiple    多项式拟合
    参数：
    - x_data,自变量数组
    - y_data, 因变量数组
    - n_fits=2, 拟合次数
    - line_style='-', 线条样式
    - line_width=2,  线条宽度
    - scatter_marker='o', 点样式
    - scatter_color='blue',点颜色
    - line_color='red' 线颜色

    tedmonf_fit    tedmon拟合
    参数：
    - x_data,自变量数组
    - y_data, 因变量数组
    - r_init, r的初始值
    - xs_init, xs的初始值
    - line_style='-', 线条样式
    - line_width=2,  线条宽度
    - scatter_marker='o', 点样式
    - scatter_color='blue',点颜色
    - line_color='red' 线颜色
    """

    #




import numpy as np

def log_fit_with_uncertainty(x_data, y_data,params,x_value=None):
    import matplotlib.pyplot as plt
    from matplotlib import rcParams,font_manager
    line_style = params.get('line_style', '-')  # 默认值为 '-'
    line_width = params.get('line_width', 2)  # 默认值为 2
    scatter_marker = params.get('scatter_marker', 'o')  # 默认值为 'o'
    scatter_color = params.get('scatter_color', 'blue')  # 默认值为 'blue'
    line_color = params.get('line_color', 'red')  # 默认值为 'red'

    log_x = np.log(x_data)
    A = np.vstack([log_x, np.ones(len(log_x))]).T
    a, b = np.linalg.lstsq(A, y_data, rcond=None)[0]

    # 计算拟合值
    y_fit = a * log_x + b

    # 计算标准误差
    residuals = y_data - y_fit
    s = np.sqrt(np.sum(residuals**2) / (len(y_data) - 2))
    perr = s * np.sqrt(np.linalg.inv(A.T @ A).diagonal())  # 标准误差

    # 计算预测的不确定度
    y_uncertainty = np.sqrt(perr[0]**2 * (np.log(x_data)**2) + perr[1]**2)

    # 扩展 x 的范围，增加 20%
    x_min, x_max = np.min(x_data), np.max(x_data)
    x_range = np.linspace(x_min - 0.1 * (x_max - x_min), x_max + 0.1 * (x_max - x_min), 800)  # 1000个点使得曲线更平滑

    # 确保 x_range 中的值大于 1e-10，避免计算对数时出错
    x_range = np.clip(x_range, 1e-10, None)  # 限制值为大于 1e-10
    log_x_range = np.log(x_range)

    # 计算扩展范围的拟合值
    y_fit_range = a * log_x_range + b



    # 计算扩展范围的预测不确定度
    y_uncertainty_range = np.sqrt(perr[0] ** 2 * (np.log(x_range) ** 2) + perr[1] ** 2)

    # 设置中文字体（根据你的操作系统调整字体路径）
    rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是常见的中文字体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 绘制结果
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label="数据点", color=scatter_color, marker=scatter_marker)  # 原始数据
    plt.plot(x_range, y_fit_range, label=f"拟合曲线: y = {a:.2f}*ln(x) + {b:.2f}", color=line_color,
             linestyle=line_style, linewidth=line_width)  # 拟合曲线
    plt.fill_between(
        x_range,
        y_fit_range - y_uncertainty_range,
        y_fit_range + y_uncertainty_range,
        color='red', alpha=0.2, label="残差范围"
    )  # 绘制预测范围
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("残差")
    plt.legend()
    plt.grid(True)
    plt.show()

    if x_value is not None:#实例
        if x_value <= 0:
            raise ValueError("x_value must be greater than 0 for logarithmic calculation.")
        y_value = a * np.log(x_value) + b
        print(f"在 x = {x_value} 时，预测的 y 值为: {y_value:.2f}")
        return a, b, y_uncertainty, y_value

    return a, b, y_uncertainty




def fit_curve_multiple(x_data, y_data, params,n_fits=2):#拟合次数不能大于数据量
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    line_style = params.get('line_style', '-')  # 默认值为 '-'
    line_width = params.get('line_width', 2)  # 默认值为 2
    scatter_marker = params.get('scatter_marker', 'o')  # 默认值为 'o'
    scatter_color = params.get('scatter_color', 'blue')  # 默认值为 'blue'
    line_color = params.get('line_color', 'red')  # 默认值为 'red'
    # 设置中文字体
    rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是常见的中文字体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 检查数据点数目与拟合次数的关系
    if len(y_data) <= n_fits:
        raise ValueError("数据点数目应大于拟合的多项式次数")

    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label="数据点", color=scatter_color, marker=scatter_marker)  # 原始数据



    # 使用numpy的polyfit进行多项式拟合
    coeffs = np.polyfit(x_data, y_data,n_fits)

    # 计算拟合的标准误差
    y_fit = np.polyval(coeffs, x_data)  # 拟合值
    residuals = y_data - y_fit  # 残差
    s = np.sqrt(np.sum(residuals ** 2) / (len(y_data) - len(coeffs)))  # 标准误差

    # 扩展x的范围，增加20%的范围
    x_min, x_max = np.min(x_data), np.max(x_data)
    x_range = np.linspace(x_min - 0.1 * (x_max - x_min), x_max + 0.1 * (x_max - x_min), 800)  # 1000个点使得曲线更平滑
    y_fit_range = np.polyval(coeffs, x_range)  # 计算拟合值

    # 计算拟合的不确定度 (不适用过度复杂的置信区间计算)
    # 使用简化的标准误差计算预测的不确定度
    x_diff = x_range - x_data[:, np.newaxis]  # x点的差异
    covariance_matrix = np.linalg.pinv(
        np.dot(np.vstack([x_data, np.ones(len(x_data))]).T, np.vstack([x_data, np.ones(len(x_data))])))  # 协方差矩阵
    y_uncertainty = s * np.sqrt(np.diagonal(np.dot(x_diff.T, np.dot(covariance_matrix, x_diff))))  # 计算不确定度

    # 精简拟合方程，科学计数法，去掉非常小的项
    equation_parts = []
    for i, coeff in enumerate(coeffs[::-1]):
        if i == 0:
            # 对于常数项直接显示
            equation_parts.append(f"{coeff:.1f}")
        else:
            # 对于其他项，判断系数是否为负数
            if coeff >= 0:
                equation_parts.append(f"+ {coeff:.1f}x^{i}")
            else:
                equation_parts.append(f"{coeff:.1f}x^{i}")

    # 合并所有项
    equation = " ".join(equation_parts)

    # 绘制拟合曲线
    if n_fits > 2:
        label = f"{n_fits}次多项式拟合: \n{equation}"
    elif n_fits == 1:
        label = f"线性拟合: \n{equation}"
    elif n_fits == 2:
        label = f"抛物线拟合: \n{equation}"

    plt.plot(x_range, y_fit_range, label=label,color=line_color, linestyle=line_style, linewidth=line_width)

    # 绘制预测范围
    plt.fill_between(x_range, y_fit_range - y_uncertainty, y_fit_range + y_uncertainty, color='red', alpha=0.2, label="残差")


    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"残差")
    plt.legend(fontsize=10)
    plt.grid(True)

    plt.show()

    return coeffs





# 定义拟合函数
def tedmon_equation(x, r, xs):
    x = np.clip(x, None, xs - 1e-5)  # 确保 x 不超过 xs
    return -x / r - (xs / r) * np.log(1 - x / xs)


# 计算残差平方和 (Sum of Squared Residuals)
def residuals(params, x_data, y_data):
    r, xs = params
    y_fit = tedmon_equation(x_data, r, xs)
    return np.sum((y_data - y_fit)**2)

# 拟合函数
def tedmon_fit(x_data, y_data, params,r_init, xs_init):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    line_style = params.get('line_style', '-')  # 默认值为 '-'
    line_width = params.get('line_width', 2)  # 默认值为 2
    scatter_marker = params.get('scatter_marker', 'o')  # 默认值为 'o'
    scatter_color = params.get('scatter_color', 'blue')  # 默认值为 'blue'
    line_color = params.get('line_color', 'red')  # 默认值为 'red'

    # 设置中文字体
    rcParams['font.sans-serif'] = ['SimHei']  # SimHei 是常见的中文字体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 梯度下降法拟合
    r = r_init
    xs = xs_init
    learning_rate = 0.001
    max_iter = 1000
    tol = 1e-6

    for i in range(max_iter):
        # 计算当前拟合值
        y_fit = tedmon_equation(x_data, r, xs)
        residuals_value = y_data - y_fit

        # 梯度计算
        log_term = 1 - x_data / xs
        log_term = np.clip(log_term, 1e-10, 1)  # 避免 log(0) 或负数
        xs_grad = -2 * np.sum(residuals_value * (-x_data / r + np.log(log_term) / r))

        r_grad = -2 * np.sum(residuals_value * (x_data / r ** 2 + xs * x_data / (xs * r ** 2 - xs * x_data)))

        # 更新拟合参数
        r -= learning_rate * r_grad
        xs -= learning_rate * xs_grad

        # 判断是否满足收敛条件
        if np.sqrt(r_grad ** 2 + xs_grad ** 2) < tol:
            break

    # 计算拟合值
    y_fit = tedmon_equation(x_data, r, xs)

    # 计算拟合标准误差
    s = np.sqrt(np.sum((y_data - y_fit) ** 2) / (len(y_data) - 2))

    # 计算预测的不确定度
    A = np.vstack([x_data, np.ones(len(x_data))]).T
    try:
        # 使用伪逆来避免奇异矩阵错误
        inv_A = np.linalg.pinv(A.T @ A)
        perr = s * np.sqrt(np.diagonal(inv_A))  # 标准误差
    except np.linalg.LinAlgError:
        perr = np.full(A.shape[1], np.inf)  # 发生错误时返回无穷大

        # 计算预测的不确定度
    y_uncertainty = np.sqrt(perr[0] ** 2 * (np.log(x_data) ** 2) + perr[1] ** 2)

    # 扩展x的范围，增加5%
    x_min, x_max = np.min(x_data), np.max(x_data)
    x_range = np.linspace(x_min - 0.1 * (x_max - x_min), x_max + 0.1 * (x_max - x_min), 800)  # 1000个点使得曲线更平滑

    # 计算扩展范围的拟合值
    y_fit_range = tedmon_equation(x_range, r, xs)

    # 确保 x_range 中的值大于 1e-10，避免计算对数时出错
    x_range = np.clip(x_range, 1e-10, None)  # 限制值为大于 1e-10

    # 计算扩展范围的预测不确定度
    y_uncertainty_range = np.sqrt(perr[0] ** 2 * (np.log(x_range) ** 2) + perr[1] ** 2)

    # 绘制拟合结果
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label="数据点", color=scatter_color, marker=scatter_marker)

    # 绘制拟合曲线
    plt.plot(x_range, y_fit_range, label=f"Tedmon 拟合曲线:\nt = {-r:.2f} * x / r - {xs:.2f} * ln(1 - x / xs)",
             color=line_color, linestyle=line_style, linewidth=line_width)

    # 绘制预测范围
    plt.fill_between(x_range, y_fit_range - y_uncertainty_range, y_fit_range + y_uncertainty_range, color='red',
                     alpha=0.2, label="残差范围")


    plt.xlabel("x (氧化膜厚度或试样重量)")
    plt.ylabel("t (时间)")
    plt.title(f"Tedmon 方程拟合")
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.show()

    return r, xs
