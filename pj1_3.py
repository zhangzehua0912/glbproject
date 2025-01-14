#第二个项目内容
#注释模块功能一般在代码前面


import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        manual_input_button = ctk.CTkButton(manual_action_frame, text="手动输入", text_color="#FFFFFF",
                                            fg_color="#FFC107", hover_color="#E0A800",
                                            command=self.open_manual_input)
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


    def open_manual_input(self):#手动输入数据框
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
                                            text="输入自定义方程的次数,f(x)=a1*x+a2*x^2+a3*x^3...计算a1,a2,a3…的值",font=("Times New Roman",16))
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
        # Placeholder for previewing data logic
        pass

    def edit_data(self, index):
        # Placeholder for editing data logic
        pass

    def perform_analysis(self):
        # Placeholder for performing analysis logic
        pass

    def perform_prediction(self):
        # Placeholder for performing prediction logic
        pass


###################################################上面是第二页的功能##########################################################


###################################################下面是第三页的功能##########################################################

    def show_data_prediction(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()
