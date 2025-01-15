#第二个项目内容
#注释模块功能一般在代码前面
#原本的第一版


import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CorrosionDatabaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.formula = None  # 定义为类的实例属性
        self.title("腐蚀数据分析系统")
        self.geometry("1600x800")
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

        analysis_button = ctk.CTkButton(button_frame, text="2.数据分析预测", text_color="#FFFFFF",
                                          font=("Roboto", 16, "bold"),
                                          fg_color="#2B2B2B",  # 深灰背景
                                          hover_color="#005F5F",  # 鼠标悬停变深
                                          border_width=2,  # 增加边框
                                          border_color="#00FFCC",  # 边框为荧光绿
                                          corner_radius=10,command=self.show_data_analysis)
        analysis_button.grid(row=0, column=1, padx=10)

        prediction_button = ctk.CTkButton(button_frame, text="2.数据分析预测", text_color="#FFFFFF",
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
        rule_combobox = ctk.CTkComboBox(select_frame, values=["请选择", "类型1", "类型2", "类型3"])  # 修改 后面通过if来选择
        rule_value=rule_combobox.get()
        rule_combobox.pack(side="left", padx=10)

        def on_formula_select(event=None):
            if formula_combobox.get() == "自定义方程":
                custom_formula_combobox.configure(state="normal")  # 激活
            else:
                custom_formula_combobox.configure(state="disabled")  # 禁用

        formula_label = ctk.CTkLabel(select_frame, text="腐蚀动力学方程:")
        formula_label.pack(side="left", padx=10)
        formula_combobox = ctk.CTkComboBox(select_frame,
                                                values=["线性 x=At+B", "抛物线", "对数", "Tedmon", "自定义方程"],command=on_formula_select)
        formula_combobox.pack(side="left", padx=10)
        selection_formula=formula_combobox.get()  #选择的公式

        custom_formula_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        custom_formula_frame.pack(pady=10)
        custom_formula_label = ctk.CTkLabel(custom_formula_frame,
                                            text="输入自定义幂函数拟合方程次数", font=("Times New Roman", 16))
        custom_formula_label.pack(side="left", padx=10)

        custom_formula_combobox = ctk.CTkComboBox(custom_formula_frame,
                                                       values=["3次幂", "4次幂", "5次幂", "6次幂", "10次幂",
                                                               "自动选择"],state="disabled")
        custom_formula_combobox.pack(side="left", padx=10)

        # 腐蚀规律类型选择###########################以上#############################################

        # 拟合和预测按钮-以下#########
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        analyze_button = ctk.CTkButton(button_frame, text="拟合/预测", fg_color="#508e54", command=self.perform_analysis)
        analyze_button.pack(side="left", padx=10)
        # predict_button = ctk.CTkButton(button_frame, text="预测", fg_color="#b54747", command=self.perform_prediction)
        # predict_button.pack(side="left", padx=10)
        # 拟合和预测按钮-以上########

        # 数据集相关
        data_label = ctk.CTkLabel(self.main_frame, text="腐蚀数据集选择:")
        data_label.pack(pady=10)

        self.datasets = [f"腐蚀数据集2024-{i + 1:02d}-27.xlsx" for i in range(50)]  # 模拟50个数据集
        self.items_per_page2 = 10  # 每页显示10条
        self.current_page2 = 1  # 当前页默认为1
        self.display_dataset_page()  # 执行模块

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

    def display_dataset_page(self):#模块执行
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

    def update_page_label(self):  # 初始化页码，更新页码
        total_pages = (len(self.datasets) + self.items_per_page2 - 1) // self.items_per_page2
        self.page_label.configure(text=f" {self.current_page2}  /  {total_pages} ")

    def prev_page(self):  # 上一页
        if self.current_page2 > 1:
            self.current_page2 -= 1
            self.update_page_label()
            self.display_dataset_page()

    def next_page(self):  # 下一页
        total_pages = (len(self.datasets) + self.items_per_page2 - 1) // self.items_per_page2
        if self.current_page2 < total_pages:
            self.current_page2 += 1
            self.update_page_label()
            self.display_dataset_page()

    def preview_data(self, index):
        """预览 Excel 数据的 AB 列内容"""
        try:
            dataset_path=r"数据.xlsx"   # 利用 self.datasets[index] 替换文件路径
            data_content=pd.read_excel(dataset_path,usecols=["X","Y"])#指定了读取第一第二列

            # 创建预览窗口
            preview_window = ctk.CTkToplevel(self.main_frame)
            preview_window.title("预览数据")
            preview_window.geometry("380x400")
            preview_window.attributes('-topmost', True)  # 窗口置顶

            # 使用 ttk.Treeview 创建表格
            tree = ttk.Treeview(preview_window, columns=("X", "Y"), show="headings", height=20)
            tree.heading("X", text="X 列")
            tree.heading("Y", text="Y 列")
            tree.column("X", width=100, anchor="center")
            tree.column("Y", width=100, anchor="center")

            # 填充数据到 Treeview
            for _, row in data_content.iterrows():
                tree.insert("", "end", values=(row["X"], row["Y"]))

            # 添加滚动条
            scrollbar = ttk.Scrollbar(preview_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # 布局 Treeview 和滚动条
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        except Exception as e:
            error_message = ctk.CTkLabel(self.main_frame, text=f"预览文件出错: {str(e)}", text_color="red")
            error_message.pack()

    def edit_data(self, index):
        """编辑 Excel 数据的 XY 列内容"""
        try:
            dataset_path = r"数据.xlsx"
            data_content = pd.read_excel(dataset_path, usecols=["X", "Y"])  # 指定读取 XY 列

            # 创建编辑窗口
            edit_window = ctk.CTkToplevel(self.main_frame)
            edit_window.title("编辑数据")
            edit_window.geometry("500x450")
            edit_window.attributes('-topmost', True)  # 窗口置顶

            # 使用 ttk.Treeview 创建表格
            tree = ttk.Treeview(edit_window, columns=("X", "Y"), show="headings", height=20)
            tree.heading("X", text="X 列")
            tree.heading("Y", text="Y 列")
            tree.column("X", width=100, anchor="center")
            tree.column("Y", width=100, anchor="center")

            # 填充数据到 Treeview
            for _, row in data_content.iterrows():
                tree.insert("", "end", values=(row["X"], row["Y"]))

            # 添加滚动条
            scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # 布局 Treeview 和滚动条
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # 全局变量存储编辑状态
            editing_state = {"item": None, "col_idx": None, "row_values": None}

            # 定义单元格编辑功能
            def on_double_click(event):
                """双击单元格进行编辑"""
                # 获取点击位置的行和列
                selected_item = tree.focus()
                column = tree.identify_column(event.x)
                row_values = tree.item(selected_item, "values")
                if not selected_item or not column or not row_values:
                    return

                # 确定列索引
                col_idx = int(column[1:]) - 1  # Treeview 列名以 "#1", "#2" 等格式
                col_value = row_values[col_idx]
                # 存储当前编辑状态
                editing_state["item"] = selected_item
                editing_state["col_idx"] = col_idx
                editing_state["row_values"] = row_values

                # 创建一个 Entry 来编辑单元格内容
                entry = ttk.Entry(edit_window)
                entry.insert(0, col_value)  # 插入当前单元格的值
                entry.focus()
                entry.place(x=event.x_root - edit_window.winfo_rootx(), y=event.y_root - edit_window.winfo_rooty())

                def save_edit(event=None):
                    """保存编辑的值"""
                    new_value = entry.get()
                    updated_values = list(editing_state["row_values"])
                    updated_values[editing_state["col_idx"]] = new_value
                    tree.item(editing_state["item"], values=updated_values)  # 更新 Treeview 数据
                    entry.destroy()

                def cancel_edit(event=None):
                    """取消编辑"""
                    entry.destroy()

                entry.bind("<Return>", save_edit)  # 按回车保存
                entry.bind("<Escape>", cancel_edit)  # 按 Esc 取消编辑

            tree.bind("<Double-1>", on_double_click)  # 绑定双击事件

            # 保存按钮
            def save_changes():
                try:
                    # 收集编辑后的数据
                    new_data = []
                    for item in tree.get_children():
                        values = tree.item(item, "values")  # 获取每行的值
                        new_data.append(values)

                    # 将新数据写回到 Excel 文件
                    edited_data = pd.DataFrame(new_data, columns=["X", "Y"])
                    edited_data.to_excel(dataset_path, index=False)

                    # 显示保存成功的消息
                    success_message = ctk.CTkLabel(edit_window, text="修改已保存！", text_color="green")
                    success_message.pack(pady=5)
                except Exception as e:
                    error_message = ctk.CTkLabel(edit_window, text=f"保存文件出错: {str(e)}", text_color="red")
                    error_message.pack(pady=5)

            save_button = ctk.CTkButton(edit_window, text="保存", fg_color="#17b784",text_color="yellow", command=save_changes)
            save_button.pack(pady=10)
            tips_label = ctk.CTkLabel(edit_window, text="双击->编辑数据;\nEnter->保存;\nEsc->取消编辑。",font=("宋体", 12))
            tips_label.pack()

        except Exception as e:
            error_message = ctk.CTkLabel(self.main_frame, text=f"编辑文件出错: {str(e)}", text_color="red")
            error_message.pack()


    def perform_analysis(self):

        print("跳转到页面3")

###################################################上面是第二页的功能##########################################################


###################################################下面是第三页的功能##########################################################

    def show_data_prediction(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()
