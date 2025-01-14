import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams



def plot_curve():
    """从表格中获取数据并绘制曲线"""
    data = []
    for row in treeview.get_children():
        data.append(treeview.item(row)['values'])

    # 将数据转换为DataFrame
    df = pd.DataFrame(data, columns=['x', 'y'])

    # 绘制曲线
    ax.clear()
    ax.plot(df['x'], df['y'], marker='o')
    ax.set_title("曲线图")
    ax.set_xlabel("X值")
    ax.set_ylabel("Y值")
    canvas.draw()


def import_data():
    """导入数据文件"""
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        try:
            df = pd.read_csv(filepath)
            # 清空表格内容并插入数据
            for row in treeview.get_children():
                treeview.delete(row)
            for _, row in df.iterrows():
                treeview.insert('', 'end', values=(row['x'], row['y']))
            plot_curve()
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {e}")


def clear_data():
    """清空数据"""
    for row in treeview.get_children():
        treeview.delete(row)

# 设置matplotlib中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 设置为黑体，支持中文
rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 创建主窗口
app = ctk.CTk()
app.title("曲线绘制工具")
app.geometry("1500x800")

# 创建一个Frame容器，用于放置表格和绘图区域
frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# 左侧部分 - 数据输入表格
table_frame = ctk.CTkFrame(frame)
table_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")

# 创建Treeview控件用于展示表格
columns = ('x', 'y')
treeview = ttk.Treeview(table_frame, columns=columns, show='headings')
treeview.heading('x', text="X值")
treeview.heading('y', text="Y值")
treeview.grid(row=0, column=0, sticky="nswe")

# 插入一些默认数据
for i in range(10):
    treeview.insert('', 'end', values=(i, i ** 2))

# 右侧部分 - 绘制曲线
plot_frame = ctk.CTkFrame(frame)
plot_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nswe")

# 初始化matplotlib图形
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# 底部控制面板
control_frame = ctk.CTkFrame(app)
control_frame.pack(fill="x", padx=20, pady=10)

# 按钮：导入数据、绘制曲线、清空数据
import_button = ctk.CTkButton(control_frame, text="导入数据", command=import_data)
import_button.pack(side="left", padx=10)

plot_button = ctk.CTkButton(control_frame, text="绘制曲线", command=plot_curve)
plot_button.pack(side="left", padx=10)

clear_button = ctk.CTkButton(control_frame, text="清空数据", command=clear_data)
clear_button.pack(side="left", padx=10)





# 运行主事件循环
app.mainloop()
