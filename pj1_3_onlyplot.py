#第二个项目内容
#注释模块功能一般在代码前面

import random
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
from custom_fit import log_fit_with_uncertainty

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CorrosionDatabaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.formula = None  # 定义为类的实例属性
        self.title("腐蚀数据分析系统")
        self.geometry("1600x850")
        self.minsize(800, 600)
        self.resizable(True, True)

        self.current_page = 1
        self.total_pages = 5
        self.all_data = []  # 存储上传的数据
        self.selected_file = ""

        # 左侧菜单栏
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.home_button = ctk.CTkButton(self.sidebar, text="0-首页", command=self.show_home)
        self.home_button.pack(pady=10, padx=10)

        self.upload_button = ctk.CTkButton(self.sidebar, text="1-数据管理", command=self.show_data_upload)
        self.upload_button.pack(pady=10, padx=10)

        self.predict_button = ctk.CTkButton(self.sidebar, text="2-数据分析", command=self.show_data_analysis)
        self.predict_button.pack(pady=10, padx=10)

        self.predict_button = ctk.CTkButton(self.sidebar, text="3-数据预测", command=self.show_data_prediction)
        self.predict_button.pack(pady=10, padx=10)

        # 主内容区域
        self.main_frame = ctk.CTkFrame(self, corner_radius=0,fg_color="#efefef")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # 分隔线
        self.sidebar_separator = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.sidebar_separator.pack(side="left", fill="y")

        self.show_home()

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        center_frame = ctk.CTkFrame(self.main_frame,
                                    fg_color="#F5F5F5",  # 浅灰色背景
                                    corner_radius=15,  # 圆角边框
                                    border_width=3,  # 边框宽度
                                    border_color="#00CCFF",  # 边框颜色（亮蓝色）
                                    width = 600,  # 强制宽度
                                    height = 200  # 强制高度
                                    )
        center_frame.pack_propagate(False)  # 禁用子组件自动调整框架尺寸
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(center_frame, text="腐蚀数据分析系统", font=("Roboto", 36))
        label.pack(pady=20)

        sub_label = ctk.CTkLabel(center_frame, text="欢迎使用腐蚀数据分析系统", font=("Arial", 18))
        sub_label.pack(pady=10)

        button_frame = ctk.CTkFrame(center_frame,fg_color="transparent")
        button_frame.pack(pady=20)

        upload_button = ctk.CTkButton(button_frame, text="1.数据管理中心",text_color="#FFFFFF",
            font=("Roboto", 16, "bold"),
            fg_color="#2B2B2B",  # 深灰背景
            hover_color="#005F5F",  # 鼠标悬停变深
            border_width=2,  # 增加边框
            border_color="#00FFCC",  # 边框为荧光绿
            corner_radius=10,command=self.show_data_upload)
        upload_button.grid(row=0, column=0, padx=10)

        analysis_button = ctk.CTkButton(button_frame, text="2.数据中心", text_color="#FFFFFF",
                                          font=("Roboto", 16, "bold"),
                                          fg_color="#2B2B2B",  # 深灰背景
                                          hover_color="#005F5F",  # 鼠标悬停变深
                                          border_width=2,  # 增加边框
                                          border_color="#00FFCC",  # 边框为荧光绿
                                          corner_radius=10,command=self.show_data_analysis)
        analysis_button.grid(row=0, column=1, padx=10)

        prediction_button = ctk.CTkButton(button_frame, text="3.分析预测", text_color="#FFFFFF",
                                          font=("Roboto", 16, "bold"),
                                          fg_color="#2B2B2B",  # 深灰背景
                                          hover_color="#005F5F",  # 鼠标悬停变深
                                          border_width=2,  # 增加边框
                                          border_color="#00FFCC",  # 边框为荧光绿
                                          corner_radius=10, command=self.show_data_prediction)
        prediction_button.grid(row=0, column=2, padx=10)

    def show_data_upload(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_data_analysis(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
###################################################上面是第一、二页的功能##########################################################
####################################↓↓↓↓↓↓第三页↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓####################################

    def destroy_plot_canvas(self):
        """销毁 Matplotlib 图形资源"""
        try:
            if hasattr(self, 'canvas') and self.canvas is not None:
                self.canvas.get_tk_widget().destroy()  # 销毁 Tkinter 小部件
                self.canvas = None  # 清空 canvas 对象引用
        except Exception as e:
            print(f"销毁图形时出错: {e}")

    def show_data_prediction(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # 设置matplotlib中文字体
        rcParams['font.sans-serif'] = ['SimHei']  # 设置为黑体，支持中文
        rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        # 创建标题
        title3_label = ctk.CTkLabel(self.main_frame, text="长周期预测", font=("黑体", 20))
        title3_label.pack(pady=10)

        #时间
        time3_Frame=ctk.CTkFrame(self.main_frame, fg_color="transparent")
        time3_Frame.pack(pady=10)
        self.unit_combobox = ctk.CTkComboBox(time3_Frame, values=["请选择", "sec","min","hour", "day"])  # 修改 后面通过if来选择
        self.unit_combobox.pack(side="left", padx=10)
        start_time_label = ctk.CTkLabel(time3_Frame, text="开始时间:")
        start_time_label.pack(side="left", padx=10)
        self.strat_time_entry = ctk.CTkEntry(time3_Frame,placeholder_text="请输入开始时间")
        self.strat_time_entry.pack(side="left", padx=10)
        finish_time_label = ctk.CTkLabel(time3_Frame, text="结束时间:")
        finish_time_label.pack(side="left", padx=10)
        self.finish_time_entry = ctk.CTkEntry(time3_Frame, placeholder_text="请输入结束时间")
        self.finish_time_entry.pack(side="left", padx=10)


        # 创建一个Frame容器，用于放置表格和绘图区域
        pre_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pre_frame.pack(pady=20, padx=20, fill="both", expand=True)
        pre_frame.grid_columnconfigure(0, weight=1)  # 设置列

        # 左侧部分 - 数据输入表格
        table_data_frame = ctk.CTkFrame(pre_frame, fg_color="transparent")
        table_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        table_data_frame.grid_columnconfigure(0, weight=1)# 确保数据表格框架的列宽与父框架一致

        # 创建Treeview控件用于展示表格
        columns_1 = ('x', 'y', 'xx', 'yy')  # 更新列定义，增加两列 xx 和 yy
        treeview = ttk.Treeview(table_data_frame, columns=columns_1, show='headings')
        treeview.heading('x', text="X值")
        treeview.heading('y', text="Y值")
        treeview.heading('xx', text="XX值")#第二组数据，不一定有
        treeview.heading('yy', text="YY值")#第二组数据，不一定有
        for col in columns_1:
            treeview.column(col, width=40, anchor='center')

        treeview.grid(row=0, column=0, sticky="nsew")
        # 滚动条
        scrollbar3 = ttk.Scrollbar(table_data_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar3.set)
        scrollbar3.grid(row=0, column=1, sticky="ns")

        #数据插入部分
        for i in range(30): # 插入一些默认数据，Treeview控件本身不直接支持编辑单元格，但可以通过捕捉鼠标事件：当用户双击某个单元格时，创建一个 CTkEntry 小部件，覆盖在该单元格上，用于编辑。
            ## 完成编辑：当用户按下回车键或点击其他地方时，保存更改并更新 Treeview 的值。
            treeview.insert('', 'end', values=(i, i ** 2, i * 2, i ** 3))  # 插入两组数据 (x, y, xx, yy)


        # 绑定双击事件
        def on_double_click(event):
            # 获取双击的单元格
            item_id = treeview.identify_row(event.y)  # 获取行ID
            column = treeview.identify_column(event.x)  # 获取列编号
            if not item_id or not column:
                return
            column_idx = int(column.replace('#', '')) - 1  # 列编号转索引
            selected_item = treeview.item(item_id, 'values')  # 获取选中行的数据

            # 创建Entry输入框
            x, y, width, height =treeview.bbox(item_id, column)
            entry = tk.Entry(treeview)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, selected_item[column_idx])  # 填入原值

            def save_edit(event=None):
                # 保存编辑后的值
                new_value = entry.get()
                values = list(selected_item)
                values[column_idx] = new_value
                treeview.item(item_id, values=values)
                entry.destroy()  # 删除输入框

            entry.bind('<Return>', save_edit)  # 按回车保存
            entry.bind('<FocusOut>', lambda e: entry.destroy())  # 失去焦点时销毁输入框
            entry.focus()  # 聚焦输入框

        treeview.bind('<Double-1>', on_double_click)

        #预测结果表格框架布局
        table_print_frame = ctk.CTkFrame(pre_frame,fg_color="transparent")
        table_print_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        table_print_frame.grid_columnconfigure(0, weight=1)# 确保结果表格框架的列宽与父框架一致
        #写个标签
        label_pre=ctk.CTkLabel(table_print_frame,text="预测结果",font=("黑体",20))
        label_pre.grid(row=0,column=0,columnspan=2)
        # 创建Treeview控件用于展示表格
        columns = ('时间','原始值','拟合值','偏差值','自定义1','自定义2')
        treeview2 = ttk.Treeview(table_print_frame, columns=columns, show='headings')

        for col in columns:
            treeview2.heading(col,text=col,anchor='center')
            treeview2.column(col, width=40, anchor='center')

        # 填充数据
        data_demo = [
            ("10", 100, 105, 5, None, None),
            ("20", 98, 102, 4),
            ("30", 105, 107, 2, "自定义值1", "自定义值2"),
        ]
        for row in data_demo:
            treeview2.insert('', 'end', values=row)

        treeview2.grid(row=1, column=0, sticky="nsew")
        # 滚动条
        scrollbar4 = ttk.Scrollbar(table_print_frame, orient="vertical", command=treeview.yview)
        treeview2.configure(yscrollcommand=scrollbar4.set)
        scrollbar4.grid(row=1, column=1, sticky="ns")


        # 右侧部分 - 绘制曲线
        plot_frame = ctk.CTkFrame(pre_frame,fg_color="transparent")
        plot_frame.grid(row=0, column=1, rowspan=2,padx=20, pady=20, sticky="nsew")

        # 右下部分 - 参数调整
        setting_frame = ctk.CTkFrame(pre_frame,fg_color="transparent")
        setting_frame.grid(row=2, column=1,padx=20, pady=20, sticky="nsew")###########

        #x轴范围和间距输入框,x_xxx_entry后面都需要判定，作为变量使用，如if x_xxx_entry=1，就使用entry输入的值
        x_range_frame=ctk.CTkFrame(setting_frame,fg_color="transparent")
        x_range_frame.pack(side="top", pady=5)
        x_range_label=ctk.CTkLabel(x_range_frame,text="X轴范围:")
        x_range_label.pack(side="left", padx=10)
        x_min_entry=ctk.CTkEntry(x_range_frame,placeholder_text="min",width=80)
        x_min_entry.pack(side="left", padx=5)
        x_1_label = ctk.CTkLabel(x_range_frame, text="-")
        x_1_label.pack(side="left", padx=5)
        x_max_entry = ctk.CTkEntry(x_range_frame, placeholder_text="max", width=80)
        x_max_entry.pack(side="left", padx=5)
        x_gap_label=ctk.CTkLabel(x_range_frame,text="X轴间隔数:")
        x_gap_label.pack(side="left", padx=10)
        x_gap_entry = ctk.CTkEntry(x_range_frame, placeholder_text="X间距", width=50)
        x_gap_entry.pack(side="left", padx=5)

        # y轴范围和间距输入框
        y_range_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        y_range_frame.pack(side="top", pady=5)
        y_range_label = ctk.CTkLabel(y_range_frame, text="Y轴范围:")
        y_range_label.pack(side="left", padx=10)
        y_min_entry = ctk.CTkEntry(y_range_frame, placeholder_text="min", width=80)
        y_min_entry.pack(side="left", padx=5)
        y_1_label = ctk.CTkLabel(y_range_frame, text="-")
        y_1_label.pack(side="left", padx=5)
        y_max_entry = ctk.CTkEntry(y_range_frame, placeholder_text="max", width=80)
        y_max_entry.pack(side="left", padx=5)
        y_gap_label = ctk.CTkLabel(y_range_frame, text="Y轴间隔数:")
        y_gap_label.pack(side="left", padx=10)
        y_gap_entry = ctk.CTkEntry(y_range_frame, placeholder_text="Y间距", width=50)
        y_gap_entry.pack(side="left", padx=5)

        #曲线参数
        cur_setting_frame = ctk.CTkFrame(setting_frame, fg_color="transparent")
        cur_setting_frame.pack(side="top", pady=5)
        color_label=ctk.CTkLabel(cur_setting_frame,text="线条颜色：")
        color_label.pack(side="left",padx=5)
        color_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=["black","red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta"])
        color_combobox.pack(side="left",padx=5)
        line_style_label=ctk.CTkLabel(cur_setting_frame,text="线条样式：")
        line_style_label.pack(side="left",padx=5)
        line_style_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=["-", "--", "-.", ":"])
        line_style_combobox.pack(side="left",padx=5)
        mark_style_label=ctk.CTkLabel(cur_setting_frame,text="标记点样式：")
        mark_style_label.pack(side="left",padx=5)
        mark_style_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=[".-点标记", "o-圆", "v-倒三角", "^-三角","<-左三角",">-右三角","1-下弧","2-上弧", "5-正方形","p-五角","*-星形","+=加号","x-X形状","h-六边形","D-菱形","d-小菱形"])
        mark_style_combobox.pack(side="left",padx=5)
        line_width_label=ctk.CTkLabel(cur_setting_frame,text="线条粗细：")
        line_width_label.pack(side="left",padx=5)
        line_width_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=["1","1.5","2","2.5","3","4","5","6","7","8","9","10"])
        line_width_combobox.pack(side="left", padx=5)
        color_point_label=ctk.CTkLabel(cur_setting_frame,text="点颜色：")
        color_point_label.pack(side="left",padx=5)
        color_point_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=["black","red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "magenta"])
        color_point_combobox.pack(side="left",padx=5)

        def plotStyle_button_click():
            params = {'line_style': line_style_combobox.get(),  # 线条样式,
                      'line_width': line_width_combobox.get(),  # 线条宽度,
                      'scatter_marker': mark_style_combobox.get()[0],  # 标记点样式,
                      'scatter_color': color_point_combobox.get(),
                      'line_color': color_combobox.get()}
            import numpy as np
            # 示例数据
            x_data = np.array([0.5, 2, 3, 4, 5])  # 输入的氧化膜厚度或试样重量数据
            y_data = np.array([2.1, 2.9, 3.7, 7.5, 8.0])  # 对应的时间数据
            # 调用 log_fit_with_uncertainty 方法
            coff = log_fit_with_uncertainty(x_data, y_data,params)
            return params,coff




        # 左下部分 - 按钮位置
        button_frame = ctk.CTkFrame(pre_frame,fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")


        # 初始化matplotlib图形
        self.canvas = tk.Canvas(plot_frame, width=900, height=100, bg="white")
        self.canvas.pack(fill="both", expand=True)





        def plot_curve():#从表格中获取数据并绘制曲线
            data = []
            for row in treeview.get_children():
                data.append(treeview.item(row)['values'])
            # 将数据转换为 DataFrame
            df = pd.DataFrame(data, columns=['x', 'y', 'xx', 'yy'])
            # 绘制曲线
            self.canvas.delete("all")  # 清除之前的绘图内容
            width = 900     #绘图框宽度——可选改变量
            height = 450    #绘图框高度——可选改变量
            margin = 50 #页边距

            # 获取用户输入的X轴范围，若没有输入，则使用数据的最小最大值
            if x_min_entry.get() and x_max_entry.get():  # 如果用户输入了X轴的范围
                x_min = float(x_min_entry.get())
                x_max = float(x_max_entry.get())
            else:  # 否则，使用数据中的最小值和最大值
                x_min, x_max = min(df['x'].min(), df['xx'].min()), max(df['x'].max(), df['xx'].max())

            # 获取用户输入的Y轴范围，若没有输入，则使用数据的最小最大值
            if y_min_entry.get() and y_max_entry.get():  # 如果用户输入了Y轴的范围
                y_min = float(y_min_entry.get())
                y_max = float(y_max_entry.get())
            else:  # 否则，使用数据中的最小值和最大值
                y_min, y_max = min(df['y'].min(), df['yy'].min()), max(df['y'].max(), df['yy'].max())

            # 获取用户输入的X轴间距，若没有输入，则使用默认值
            if x_gap_entry.get():  # 如果用户输入了X轴间距
                x_grid = int(x_gap_entry.get())
            else:  # 否则，使用默认间距
                x_grid = 5

            if y_gap_entry.get():  # 如果用户输入了X轴间距
                y_grid = int(y_gap_entry.get())
            else:  # 否则，使用默认间距
                y_grid = 5

            #画布大小
            x_scale = (width - 2 * margin) / (x_max - x_min)
            y_scale = (height - 2 * margin) / (y_max - y_min)

            # 绘制坐标轴
            x_axis_y = height - margin  # X轴的Y坐标
            y_axis_x = margin  # Y轴的X坐标
            self.canvas.create_line(margin, height - margin, width - margin, height - margin, arrow=tk.LAST)  # X轴
            self.canvas.create_line(margin, height - margin, margin, margin, arrow=tk.LAST)  # Y轴

            # 绘制X轴刻度和标签
            for i in range(x_grid):
                x_val = x_min + i * (x_max - x_min) / x_grid
                x_pos = margin + (x_val - x_min) * x_scale
                self.canvas.create_line(x_pos, x_axis_y, x_pos, x_axis_y + 5)
                self.canvas.create_text(x_pos, x_axis_y + 20, text=f"{x_val:.1f}")

            # 绘制Y轴刻度和标签
            for i in range(y_grid):
                y_val = y_min + i * (y_max - y_min) / y_grid
                y_pos = height - margin - (y_val - y_min) * y_scale
                self.canvas.create_line(y_axis_x - 5, y_pos, y_axis_x, y_pos)
                self.canvas.create_text(y_axis_x - 20, y_pos, text=f"{y_val:.1f}")

            prev_x = prev_y = None#初始化
            prev_xx = prev_yy = None#初始化

            # 绘制曲线
            for _, row in df.iterrows():
                # 绘制 (x, y) 曲线
                x, y = row['x'], row['y']
                canvas_x = margin + (x - x_min) * x_scale
                canvas_y = height - margin - (y - y_min) * y_scale
                self.canvas.create_oval(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill="blue")  # 数据点
                if prev_x is not None and prev_y is not None:
                    self.canvas.create_line(prev_x, prev_y, canvas_x, canvas_y, fill="blue")  # 连线
                prev_x, prev_y = canvas_x, canvas_y
                # 绘制 (xx, yy) 曲线
                xx, yy = row['xx'], row['yy']
                canvas_xx = margin + (xx - x_min) * x_scale
                canvas_yy = height - margin - (yy - y_min) * y_scale
                self.canvas.create_oval(canvas_xx - 2, canvas_yy - 2, canvas_xx + 2, canvas_yy + 2, fill="red")  # 数据点
                if prev_xx is not None and prev_yy is not None:
                    self.canvas.create_line(prev_xx, prev_yy, canvas_xx, canvas_yy, fill="red")  # 连线
                prev_xx, prev_yy = canvas_xx, canvas_yy

            # 为每条曲线添加标签（如 "x-y 曲线" 和 "xx-yy 曲线"）
            self.canvas.create_text(width - margin, height - margin - 20, text="x-y 曲线", fill="blue",
                                    font=("Arial", 10, "bold"))
            self.canvas.create_text(width - margin, height - margin - 40, text="xx-yy 曲线", fill="red",
                                    font=("Arial", 10, "bold"))


        def import_data():  #导入数据文件
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

        def clear_data():#清空数据
            try:
                for row in treeview.get_children():
                    treeview.delete(row)
            except Exception as e:
                messagebox.showerror("错误", f"清空数据时出错: {e}")



        # 按钮：导入数据、绘制曲线(醒目记号)、清空数据
        button_under_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_under_frame.pack(side="top", pady=5)

        import_button = ctk.CTkButton(button_under_frame, text="导入数据",width=70,command=import_data)
        import_button.pack(side="left", padx=5)
        clear_button = ctk.CTkButton(button_under_frame, text="清空数据", width=70, command=clear_data)
        clear_button.pack(side="left", padx=5)
        plot_button = ctk.CTkButton(button_under_frame, text="绘图\刷新",fg_color="#508e54",text_color="yellow",font=("Arial",20),
                                    width=100,height=40,command=plot_curve)
        plot_button.pack(side="left", padx=5)

        #拟合作为调用，弹出界面显示图形
        fit_button = ctk.CTkButton(button_under_frame, text="拟合",fg_color="#3366cc",text_color="white",font=("Arial",20),
                                    width=100,height=40,command=lambda:print(plotStyle_button_click()))
        fit_button.pack(side="left", padx=5)

        data_select_frame=ctk.CTkFrame(button_frame, fg_color="transparent")
        data_select_frame.pack(side="top", pady=5)
        #数据选择（预留），当有多列数据时候，需要选择以哪两列为xy轴时使用的
        xdata=["X","Y"]  #变量更新
        ydata = ["X", "Y"]  # 变量更新
        data_choose_label=ctk.CTkLabel(data_select_frame,text="数据选择X-Y:")
        data_choose_label.pack(side="left", padx=10)
        xdata_combobox=ctk.CTkComboBox(data_select_frame,width=80,values=xdata)
        xdata_combobox.pack(side="left", padx=5)
        ydata_combobox=ctk.CTkComboBox(data_select_frame,width=80,values=ydata)
        ydata_combobox.pack(side="left", padx=5)

        #预测结果数据，再增加按钮，进行连接






if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()


