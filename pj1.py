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

        title_label = ctk.CTkLabel(self.main_frame, text="数据上传", font=("黑体", 20))
        title_label.pack(pady=10)

        # 上传按钮框架
        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        action_frame.pack(pady=10)

        select_file_button = ctk.CTkButton(action_frame, text="选择文件", text_color="#FFFFFF",fg_color="#28A745", hover_color="#218838",command=lambda: self.select_file())
        select_file_button.grid(row=0, column=0, padx=10)

        upload_button = ctk.CTkButton(action_frame, text="上传解析",text_color="#FFFFFF",command=lambda: self.parse_file(self.table))
        upload_button.grid(row=0, column=1, padx=10)

        # 表格框架
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ["时间1", "数据1", "时间2", "数据2", "时间3", "数据3", "时间4", "数据4", "备注"]
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.table.pack(side="left", fill="both", expand=True)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)

        # 测试数据,这个数据应该是来源于EXCEL的。也可以用于输入和编辑
        sample_data = [
            ["2024-01-01 10:00", "10", "2024-01-01 11:00", "20", "2024-01-01 12:00", "30", "2024-01-01 13:00", "40",
             "备注1"],
            ["2024-01-02 10:00", "15", "2024-01-02 11:00", "25", "2024-01-02 12:00", "35", "2024-01-02 13:00", "45",
             "备注2"],
            ["2024-01-03 10:00", "20", "2024-01-03 11:00", "30", "2024-01-03 12:00", "40", "2024-01-03 13:00", "50",
             "备注3"],
        ]
        for row in sample_data:#插入示例数据
            self.table.insert("", "end", values=row)

        #手动输入(需要配套删除功能)
        manual_action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        manual_action_frame.pack(pady=10)

        def open_manual_input():#手动输入数据框
            manual_window = ctk.CTkToplevel()
            manual_window.title("手动输入数据")
            manual_window.geometry("400x550")
            manual_window.attributes('-topmost', True)  # 设置窗口始终置顶
            input_frame = ctk.CTkFrame(manual_window, fg_color="transparent")
            input_frame.pack(fill="both", expand=True, padx=20, pady=20)
            # Input labels and fields
            labels = ["时间1", "数据1", "时间2", "数据2", "时间3", "数据3", "时间4", "数据4", "备注"]
            inputs = {}
            for i, label in enumerate(labels):
                lbl = ctk.CTkLabel(input_frame, text=label, font=("Arial", 12))
                lbl.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                entry = ctk.CTkEntry(input_frame, width=200)
                entry.grid(row=i, column=1, padx=10, pady=5)
                inputs[label] = entry

            # Submit button
            submit_button = ctk.CTkButton(manual_window, text="提交", text_color="#FFFFFF", fg_color="#28A745",
                                          hover_color="#218838", command=lambda: self.submit_manual_data(inputs))
            submit_button.pack(pady=20)

        manual_input_button = ctk.CTkButton(manual_action_frame, text="手动输入", text_color="#FFFFFF",
                                            fg_color="#FFC107", hover_color="#E0A800",
                                            command=open_manual_input)
        manual_input_button.grid(row=0, column=0, padx=10)


        self.delete_button = ctk.CTkButton(manual_action_frame, text="删除", text_color="#FFFFFF",
                                           fg_color="#DC3545", hover_color="#C82333",
                                           state="disabled", command=lambda: self.delete_selected_row(self.table))
        self.delete_button.grid(row=0, column=1, padx=10)
        # 绑定选中事件
        self.table.bind("<<TreeviewSelect>>", lambda event: self.toggle_delete_button(self.table))

        # 翻页框架
        nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_frame.pack(pady=10)

        prev_button = ctk.CTkButton(nav_frame, text="<上一页", text_color="black", fg_color="gray",width=30,command=lambda: self.change_page(-1, self.table))
        prev_button.grid(row=0, column=0, padx=5)

        next_button = ctk.CTkButton(nav_frame, text="下一页>", text_color="black", fg_color="gray",width=30,command=lambda: self.change_page(1, self.table))
        next_button.grid(row=0, column=2, padx=5)

        self.page_label = ctk.CTkLabel(nav_frame, text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页", font=("Arial", 12))
        self.page_label.grid(row=0, column=1, padx=10)




    def toggle_delete_button(self, table):    #未选中状态禁用删除功能
        # 获取选中的行
        selected_items = table.selection()
        if selected_items:  # 如果有选中内容，启用删除按钮
            self.delete_button.configure(state="normal")
        else:  # 否则禁用删除按钮
            self.delete_button.configure(state="disabled")
    def delete_selected_row(self, table):  #删除功能
        # 获取选中的行
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("警告", "未选择任何行！")  # 未选中行时显示警告
            return
        # 删除选中的行#最好弹出提示框
        confirm = messagebox.askyesno("确认删除", "确定要删除选中的行吗？")
        if confirm:  # 如果用户确认
            for item in selected_item:
                table.delete(item)
            print("选中的行已删除")
            self.toggle_delete_button(table)
        else:
            print("删除操作已取消")

    def submit_manual_data(self, inputs):
        # 从输入字段中提取数据
        data = {key: field.get() for key, field in inputs.items()}

        # 检查是否所有字段都填写
        if any(not value for value in data.values()):
            messagebox.showwarning("警告", "所有字段均为必填项，请填写完整！")
            return

        # 将数据转换为列表（与表格列匹配）
        data_values = [data.get(col, "") for col in
                       ["时间1", "数据1", "时间2", "数据2", "时间3", "数据3", "时间4", "数据4", "备注"]]

        # 将数据插入表格
        self.table.insert("", "end", values=data_values)

        # 关闭输入窗口并打印信息
        print("手动输入的数据已添加到表格：", data_values)
        inputs[list(inputs.keys())[0]].winfo_toplevel().destroy()  # 关闭窗口

    def select_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if self.selected_file:
            print(f"已选择文件: {self.selected_file}")

    def parse_file(self, table):
        if not self.selected_file:
            print("请先选择文件")
            return

        if self.selected_file.endswith(".csv"):
            data = pd.read_csv(self.selected_file)
        elif self.selected_file.endswith(".xlsx"):
            data = pd.read_excel(self.selected_file)
        else:
            print("不支持的文件格式")
            return

        self.all_data = data.values.tolist()
        self.total_pages = (len(self.all_data) + 9) // 10  # 每页10行
        self.current_page = 1
        self.update_table_data(table)

    def update_table_data(self, table):
        start_index = (self.current_page - 1) * 10
        end_index = start_index + 10
        page_data = self.all_data[start_index:end_index]

        for row in table.get_children():
            table.delete(row)

        for row in page_data:
            table.insert("", "end", values=row)

        self.page_label.configure(text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页")

    def change_page(self, direction, table):
        if direction == -1 and self.current_page > 1:
            self.current_page -= 1
        elif direction == 1 and self.current_page < self.total_pages:
            self.current_page += 1
        self.update_table_data(table)

################################################上面为第一页的功能########################################################
################################################下面为第二个功能########################################################
    def show_data_analysis(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.main_frame, text="数据分析中心", font=("黑体", 24))
        title_label.pack(pady=10)

        # 腐蚀规律类型选择###########################以下#############################################
        select_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        select_frame.pack(pady=10)
        rule_label = ctk.CTkLabel(select_frame, text="腐蚀规律类:")
        rule_label.pack(side="left", padx=10)
        self.rule_combobox = ctk.CTkComboBox(select_frame, values=["请选择", "类型1", "类型2", "类型3"])  # 修改 后面通过if来选择
        self.rule_combobox.pack(side="left", padx=10)

        formula_label = ctk.CTkLabel(select_frame, text="腐蚀动力学方程:")
        formula_label.pack(side="left", padx=10)
        self.formula_combobox = ctk.CTkComboBox(select_frame,
                                                values=["线性 x=At+B", "抛物线", "对数", "Tedmon", "自定义方程"])
        self.formula_combobox.pack(side="left", padx=10)

        custom_formula_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        custom_formula_frame.pack(pady=10)
        custom_formula_label = ctk.CTkLabel(custom_formula_frame,
                                            text="输入自定义幂函数拟合方程次数",font=("Times New Roman",16))
        custom_formula_label.pack(side="left", padx=10)
        self.custom_formula_combobox = ctk.CTkComboBox(custom_formula_frame, values=["请选择", "3次幂", "4次幂", "5次幂","6次幂","10次幂","自动选择"])
        self.custom_formula_combobox.pack(side="left", padx=10)
        # 腐蚀规律类型选择###########################以上#############################################

        # 拟合和预测按钮-以下#########
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        analyze_button = ctk.CTkButton(button_frame, text="拟合", fg_color="#508e54", command=self.perform_analysis)
        analyze_button.pack(side="left", padx=10)
        predict_button = ctk.CTkButton(button_frame, text="预测", fg_color="#b54747", command=self.perform_prediction)
        predict_button.pack(side="left", padx=10)
        # 拟合和预测按钮-以上########

        #数据集相关
        data_label = ctk.CTkLabel(self.main_frame, text="腐蚀数据集选择:")
        data_label.pack(pady=10)

        self.datasets = [f"腐蚀数据集2024-{i + 1:02d}-27.xlsx" for i in range(50)]  # 模拟50个数据集
        self.items_per_page2 = 10#每页显示10条
        self.current_page2 = 1 #当前页默认为1
        self.display_dataset_page()#执行模块

        # 页码导航（更新页面功能）-以下######################################################################################
        self.nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.nav_frame.pack(pady=10)
        prev_button = ctk.CTkButton(self.nav_frame, text="<<PgUp", text_color="blue", fg_color="#f9f9f9", width=30,
                                    command=self.prev_page)
        prev_button.pack(side="left", padx=5)

        self.page_label = ctk.CTkLabel(self.nav_frame, text="", font=("Arial", 12))
        self.page_label.pack(side="left", padx=5)

        next_button = ctk.CTkButton(self.nav_frame, text="PgDn>>", text_color="blue", fg_color="#f9f9f9", width=30,
                                    command=self.next_page)
        next_button.pack(side="left", padx=5)
        # 页码导航——以上##################################################################################################
        self.display_dataset_page()  # 执行模块
        self.update_page_label()  # 初始化页码



    def display_dataset_page(self):
        start_index = (self.current_page2 - 1) * self.items_per_page2
        end_index = start_index + self.items_per_page2
        visible_datasets = self.datasets[start_index:end_index]

        for frame in getattr(self, "dataset_frames", []):  # 清除以前的帧
            frame.destroy()

        self.dataset_frames = []
        for i, dataset in enumerate(visible_datasets):
            dataset_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            dataset_frame.pack(pady=5)
            self.dataset_frames.append(dataset_frame)

            checkbox = ctk.CTkCheckBox(dataset_frame, text=f"选项{start_index + i + 1}",
                                       font=("Times New Roman", 12))
            checkbox.pack(side="left", padx=5)

            filename_entry = ctk.CTkEntry(dataset_frame, width=500)
            filename_entry.insert(0, dataset)
            filename_entry.pack(side="left", padx=5)

            preview_button = ctk.CTkButton(dataset_frame, text="预览", fg_color="#99c913", width=30,
                                           command=lambda i=i: self.preview_data(start_index + i))
            preview_button.pack(side="left", padx=5)

            edit_button = ctk.CTkButton(dataset_frame, text="编辑", fg_color="#b78217", width=30,
                                        command=lambda i=i: self.edit_data(start_index + i))
            edit_button.pack(side="left", padx=5)


    def update_page_label(self):    #更新页码
        total_pages = (len(self.datasets) + self.items_per_page2 - 1) // self.items_per_page2
        self.page_label.configure(text=f" {self.current_page2}  /  {total_pages} ")

    def prev_page(self):    #上一页
        if self.current_page2 > 1:
            self.current_page2 -= 1
            self.update_page_label()
            self.display_dataset_page()
    def next_page(self):    #下一页
        total_pages = (len(self.datasets) + self.items_per_page2 - 1) // self.items_per_page2
        if self.current_page2 < total_pages:
            self.current_page2 += 1
            self.update_page_label()
            self.display_dataset_page()




    def preview_data(self, index):

        pass

    def edit_data(self, index):

        pass

    def perform_analysis(self):

        pass

    def perform_prediction(self):

        pass
###################################################上面是第二页的功能##########################################################
###################################################下面是第三页的功能##########################################################

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
        columns = ('x', 'y')
        treeview = ttk.Treeview(table_data_frame, columns=columns, show='headings')
        treeview.heading('x', text="X值")
        treeview.heading('y', text="Y值")
        treeview.grid(row=0, column=0, sticky="nsew")
        # 滚动条
        scrollbar3 = ttk.Scrollbar(table_data_frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar3.set)
        scrollbar3.grid(row=0, column=1, sticky="ns")

        for i in range(30): # 插入一些默认数据，Treeview控件本身不直接支持编辑单元格，但可以通过捕捉鼠标事件：当用户双击某个单元格时，创建一个 CTkEntry 小部件，覆盖在该单元格上，用于编辑。
            ## 完成编辑：当用户按下回车键或点击其他地方时，保存更改并更新 Treeview 的值。
            treeview.insert('', 'end', values=(i, i ** 2))

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
        columns = ('时间','原始值','拟合值','偏差值','方程','腐蚀速率')
        treeview2 = ttk.Treeview(table_print_frame, columns=columns, show='headings')

        #treeview.insert('', 'end', values=(x,y))插入数据
        for col in columns:
            treeview2.heading(col,text=col,anchor='center')
            treeview2.column(col, width=40, anchor='center')
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
        x_gap_label=ctk.CTkLabel(x_range_frame,text="X轴间距:")
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
        y_gap_label = ctk.CTkLabel(y_range_frame, text="Y轴间距:")
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
        line_style_label=ctk.CTkComboBox(cur_setting_frame,width=80,values=["-", "--", "-.", ":"])
        line_style_label.pack(side="left",padx=5)
        mark_style_label=ctk.CTkLabel(cur_setting_frame,text="标记点样式：")
        mark_style_label.pack(side="left",padx=5)
        mark_style_label=ctk.CTkComboBox(cur_setting_frame,width=80,values=[".-点标记", "o-圆", "v-倒三角", "^-三角","<-左三角",">-右三角","1-下弧","2-上弧", "5-正方形","p-五角","*-星形","+=加号","x-X形状","h-六边形","D-菱形","d-小菱形"])
        mark_style_label.pack(side="left",padx=5)
        line_width_label=ctk.CTkLabel(cur_setting_frame,text="线条粗细：")
        line_width_label.pack(side="left",padx=5)
        line_width_combobox=ctk.CTkComboBox(cur_setting_frame,width=80,values=["1","1.5","2","2.5","3","4","5","6","7","8","9","10"])
        line_width_combobox.pack(side="left", padx=5)



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
            df = pd.DataFrame(data, columns=['x', 'y'])
            # 绘制曲线
            self.canvas.delete("all")  # 清除之前的绘图内容
            width = 900     #绘图框宽度——改变量
            height = 450    #绘图框高度——改变量
            margin = 50 #页边距
            x_grid=6    #x轴间距——改变量
            y_grid=6    #y轴间距——改变量

            # 数据归一化
            x_min, x_max = df['x'].min(), df['x'].max()
            y_min, y_max = df['y'].min(), df['y'].max()
            x_scale = (width - 2 * margin) / (x_max - x_min)
            y_scale = (height - 2 * margin) / (y_max - y_min)

            # 绘制坐标轴
            x_axis_y = height - margin  # X轴的Y坐标
            y_axis_x = margin  # Y轴的X坐标
            self.canvas.create_line(margin, height - margin, width - margin, height - margin, arrow=tk.LAST)  # X轴
            self.canvas.create_line(margin, height - margin, margin, margin, arrow=tk.LAST)  # Y轴

            # 绘制X轴刻度和标签
            for i in range(x_grid):
                x_val = x_min + i * (x_max - x_min) / 5
                x_pos = margin + (x_val - x_min) * x_scale
                self.canvas.create_line(x_pos, x_axis_y, x_pos, x_axis_y + 5)
                self.canvas.create_text(x_pos, x_axis_y + 20, text=f"{x_val:.1f}")

            # 绘制Y轴刻度和标签
            for i in range(y_grid):
                y_val = y_min + i * (y_max - y_min) / 5
                y_pos = height - margin - (y_val - y_min) * y_scale
                self.canvas.create_line(y_axis_x - 5, y_pos, y_axis_x, y_pos)
                self.canvas.create_text(y_axis_x - 20, y_pos, text=f"{y_val:.1f}")

            # 绘制曲线
            prev_x = prev_y = None
            for _, row in df.iterrows():
                x, y = row['x'], row['y']
                canvas_x = margin + (x - x_min) * x_scale
                canvas_y = height - margin - (y - y_min) * y_scale
                self.canvas.create_oval(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill="blue")  # 数据点
                if prev_x is not None and prev_y is not None:
                    self.canvas.create_line(prev_x, prev_y, canvas_x, canvas_y, fill="blue")  # 连线
                prev_x, prev_y = canvas_x, canvas_y


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
        plot_button = ctk.CTkButton(button_under_frame, text="绘图\拟合\刷新",fg_color="#508e54",text_color="yellow",font=("Arial",20),
                                    width=180,height=40,command=plot_curve)
        plot_button.pack(side="left", padx=5)

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




###################################################下面是第三页的功能##########################################################



if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()


