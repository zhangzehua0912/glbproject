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
        self.rule_combobox = ctk.CTkComboBox(select_frame, values=["请选择", "类型1", "类型2", "类型3"])  # 修改 后面通过if来选择
        self.rule_combobox.pack(side="left", padx=10)

        formula_label = ctk.CTkLabel(select_frame, text="腐蚀动力学方程:")
        formula_label.pack(side="left", padx=10)
        self.formula_combobox = ctk.CTkComboBox(select_frame,
                                                values=["线性 x=At+B", "抛物线", "对数", "Tedmon", "自定义方程"])
        self.formula_combobox.pack(side="left", padx=10)
        selection_formula=self.formula_combobox.get()  #选择的公式

        custom_formula_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        custom_formula_frame.pack(pady=10)
        custom_formula_label = ctk.CTkLabel(custom_formula_frame,
                                            text="输入自定义幂函数拟合方程次数", font=("Times New Roman", 16))
        custom_formula_label.pack(side="left", padx=10)
        self.custom_formula_combobox = ctk.CTkComboBox(custom_formula_frame,
                                                       values=["请选择", "3次幂", "4次幂", "5次幂", "6次幂", "10次幂",
                                                               "自动选择"])
        self.custom_formula_combobox.pack(side="left", padx=10)
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
            data_content=pd.read_excel(dataset_path,usecols=["A","B"])#指定了读取AB列
            # 将数据转换为字符串
            data_preview = data_content.to_string(index=False)

            #预览窗口
            preview_window = ctk.CTkToplevel(self.main_frame)
            preview_window.title("预览数据")
            preview_window.geometry("600x400")

            preview_textbox = ctk.CTkTextbox(preview_window, width=580, height=380)
            preview_textbox.insert("1.0", data_preview)
            preview_textbox.configure(state="disabled")  # 设置为只读
            preview_textbox.pack(pady=10, padx=10)

        except Exception as e:
            error_message = ctk.CTkLabel(self.main_frame, text=f"预览文件出错: {str(e)}", text_color="red")
            error_message.pack()

    def edit_data(self, index):

        pass

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
