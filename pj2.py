import customtkinter as ctk
from tkinter import ttk

ctk.set_appearance_mode("System")  # 设置外观模式：System、Dark 或 Light
ctk.set_default_color_theme("blue")  # 设置主题颜色


class CorrosionDatabaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("腐蚀数据库系统")
        self.geometry("1750x800")
        self.minsize(1500, 600)
        self.resizable(True, True)

        # 左侧菜单栏
        self.sidebar = ctk.CTkFrame(self, width=200,corner_radius=0)#去圆角
        self.sidebar.pack(side="left", fill="y")

        self.home_button = ctk.CTkButton(self.sidebar, text="首页", command=self.show_home)
        self.home_button.pack(pady=10, padx=10)

        self.literature_button = ctk.CTkButton(self.sidebar, text="文献数据", command=self.show_literature_data)
        self.literature_button.pack(pady=10, padx=10)

        self.experiment_button = ctk.CTkButton(self.sidebar, text="试验数据", command=self.show_experiment_data)
        self.experiment_button.pack(pady=10, padx=10)

        # 主内容区域
        self.main_frame = ctk.CTkFrame(self,corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")

        # 分隔线
        self.sidebar_separator = ctk.CTkFrame(self, width=2, fg_color="gray")
        self.sidebar_separator.pack(side="left", fill="y")

        self.show_home()

    def show_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # 创建一个居中的父框架
        center_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")  # 整个内容框架居中

        label = ctk.CTkLabel(center_frame, text="腐蚀数据库系统", font=("楷体", 36))
        label.pack(pady=20)

        sub_label = ctk.CTkLabel(center_frame, text="欢迎使用腐蚀数据库系统", font=("Arial", 18))
        sub_label.pack(pady=10)

        button_frame = ctk.CTkFrame(center_frame)
        button_frame.pack(pady=20)

        doc_button = ctk.CTkButton(button_frame, text="文献数据", command=self.show_literature_data)
        doc_button.grid(row=0, column=0, padx=10)

        experiment_button = ctk.CTkButton(button_frame, text="试验数据", command=self.show_experiment_data)
        experiment_button.grid(row=0, column=1, padx=10)

    def show_literature_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.main_frame, text="文献数据", font=("黑体", 20))
        title_label.pack(pady=10)

        search_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        search_frame.pack(pady=10)

        title_entry = ctk.CTkEntry(search_frame, placeholder_text="文献标题")
        title_entry.grid(row=0, column=0, padx=5)

        author_entry = ctk.CTkEntry(search_frame, placeholder_text="作者")
        author_entry.grid(row=0, column=1, padx=5)

        issn_entry = ctk.CTkEntry(search_frame, placeholder_text="ISSN")
        issn_entry.grid(row=0, column=2, padx=5)

        doi_entry = ctk.CTkEntry(search_frame, placeholder_text="DOI")
        doi_entry.grid(row=0, column=3, padx=5)

        search_button = ctk.CTkButton(search_frame, text="模 糊 查 询", fg_color="#4CAF50",hover_color="#45A049",text_color="white",
                                      command=lambda: print("查询文献数据"))
        search_button.grid(row=0, column=4, padx=5)

        #table Frame
        table_frame = ctk.CTkTextbox(self.main_frame, width=800, height=400)
        table_frame.pack(pady=20,fill="both",expand=True)

        # 表格
        columns = ["文献类型", "标题", "作者", "期刊名称", "发布时间", "ISSN", "DOI", "URL","操作"]
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
        )
        table.grid(row=0, column=0, sticky="nsew")

        # 表格垂直滚动条
        table_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table_scroll.grid(row=0, column=1, sticky="ns")

        # 滚动条
        table.configure(yscrollcommand=table_scroll.set)

        # Set column headers and widths
        for col in columns:
            if col == "标题" or col == "DOI":
                table.heading(col, text=col)
                table.column(col, anchor="w", width=160)
            else:
                table.heading(col, text=col)
                table.column(col, anchor="w", width=80)



        # 插入的数据，需要导入数据库或者链接数据库，按页码
        sample_data = [
            ["JOUR", "Title", "作者", "期刊名称", "2022-03-01", "2468-2276",
             "10.1016/xxxx", "https://...","双击查看"],
            ["JOUR", "Title", "author", "期刊名称2", "2023-09-19", "0921-5093",
             "10.1016/xxx", "https://...","双击查看"],
        ]

        for row in sample_data:
            values = row[:-1]  # 不包括操作列
            item_id = table.insert("", "end", values=values)
            table.set(item_id, column="操作", value="双击查看")

        #在用户点击包含“查看”的列时，触发相应的逻辑。例如，点击“查看”列后跳转到 URL 或执行某个操作
        # 添加双击跳转事件
        def table1_doubleclick(event):
            selected_item = table.selection()
            if selected_item:  # 如果有选中的行
                item = table.item(selected_item)
                values = item["values"]
                if len(values) >= 9 and values[8] == "双击查看":
                    url = values[7]  # 获取 激活行的URL
                    print(f"跳转到 URL: {url}")
                    # 实现web跳转功能
                    import webbrowser
                    webbrowser.open(url)

        # 双击实现查看，不容易添加按钮
        table.bind("<Double-1>", table1_doubleclick)

        # 页码导航
        nav_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        nav_frame.pack(pady=10)

        # 当前页码
        self.current_page = 1 #要改
        self.total_pages = 5  # 总页数 要改

        # 显示页码
        page_label = ctk.CTkLabel(nav_frame, text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页",
                                  font=("Arial", 12))
        page_label.grid(row=0, column=1, padx=5)

        prev_button = ctk.CTkButton(nav_frame, text="<上一页",text_color="black",fg_color="gray", width=30, command=lambda: print("上一页"))
        prev_button.grid(row=0, column=0, padx=5)

        next_button = ctk.CTkButton(nav_frame, text="下一页>",text_color="black", fg_color="gray",width=30,command=lambda: print("下一页"))
        next_button.grid(row=0, column=2, padx=5)

    # 翻页功能  未使用 作参考
    def change_page(self, direction, page_label):
        # 更新当前页码
        if 1 <= self.current_page + direction <= self.total_pages:
            self.current_page += direction
            page_label.configure(text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页")
            print(f"切换到第 {self.current_page} 页")
            # 在这里更新表格数据逻辑，例如从数据库加载下一页数据

    def show_experiment_data(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(self.main_frame, text="试验数据", font=("黑体", 20))
        title_label.pack(pady=10)
        #搜索
        search_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        search_frame.pack(pady=10)

        #搜索-字段
        material_name_label = ctk.CTkLabel(search_frame, text="材料名称:")
        material_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        material_name_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        material_name_entry.grid(row=0, column=1, padx=5, pady=5)

        composition_label = ctk.CTkLabel(search_frame, text="材料成分:")
        composition_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        composition_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        composition_entry.grid(row=0, column=3, padx=5, pady=5)

        temp_label = ctk.CTkLabel(search_frame, text="试验温度:")
        temp_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        temp_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        temp_entry.grid(row=0, column=5, padx=5, pady=5)

        pressure_label = ctk.CTkLabel(search_frame, text="试验压力:")
        pressure_label.grid(row=0, column=6, padx=5, pady=5, sticky="e")
        pressure_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        pressure_entry.grid(row=0, column=7, padx=5, pady=5)

        process_label = ctk.CTkLabel(search_frame, text="试验流速:")
        process_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        process_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        process_entry.grid(row=1, column=1, padx=5, pady=5)

        gas_label = ctk.CTkLabel(search_frame, text="氧浓度:")
        gas_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        gas_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        gas_entry.grid(row=1, column=3, padx=5, pady=5)

        reserve1_label = ctk.CTkLabel(search_frame, text="预留1:")
        reserve1_label.grid(row=1, column=4, padx=5, pady=5, sticky="e")
        reserve1_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        reserve1_entry.grid(row=1, column=5, padx=5, pady=5)

        reserve2_label = ctk.CTkLabel(search_frame, text="预留2:")
        reserve2_label.grid(row=1, column=6, padx=5, pady=5, sticky="e")
        reserve2_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        reserve2_entry.grid(row=1, column=7, padx=5, pady=5)

        reserve3_label = ctk.CTkLabel(search_frame, text="预留3:")
        reserve3_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        reserve3_entry = ctk.CTkEntry(search_frame, placeholder_text="请输入")
        reserve3_entry.grid(row=2, column=1, padx=5, pady=5)

        search_button = ctk.CTkButton(search_frame, text="查询", text_color="#000000",fg_color="#7989FF",hover_color="#0078D7",
                                      command=lambda: print("查询试验数据"))
        search_button.grid(row=2, column=7, padx=5,pady=5)

        # 表格框架
        table_frame = ctk.CTkTextbox(self.main_frame, width=800, height=400)
        table_frame.pack(pady=20, fill="both", expand=True)

        # 表格
        columns = [
            "材料类型", "材料名称", "成分", "处理工艺", "试验时间", "试验温度",
            "试验压力", "试验件表面流速(m/s)", "试验气浓度(wt%)", "氧化膜厚度",
            "试样重量", "数据来源", "预留1", "预留2", "预留3"
        ]
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
        )
        table.grid(row=0, column=0, sticky="nsew")

        # 添加滚动条
        table_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        table_scroll.grid(row=0, column=1, sticky="ns")
        table.configure(yscrollcommand=table_scroll.set)

        # 设置列标题
        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor="w", width=100)

        #数据,需要链接到数据库
        sample_data = [
            [
                "钢", "Eurofer steel", "Fe-Al", "电沉积", "4000小时", "400℃",
                "未指定", "大约 2.4", "未指定", "55µm", "未指定", "10.1016/j.surface",
                "空", "空", "空"
            ]
        ]
        for row in sample_data:
            table.insert("", "end", values=row)


        # 功能按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        # “查看图片”按钮
        view_image_button = ctk.CTkButton(button_frame, text="查看图片", fg_color="#007BFF", hover_color="#0056b3",
                                          text_color="white", state="disabled",  # 默认禁用
                                          command=lambda: print("查看图片被点击"))
        view_image_button.grid(row=0, column=0, padx=10)

        # “查看数据”按钮
        view_data_button = ctk.CTkButton(button_frame, text="查看数据", fg_color="#28A745", hover_color="#218838",
                                         text_color="white", state="disabled",  # 默认禁用
                                         command=lambda: print("查看数据被点击"))
        view_data_button.grid(row=0, column=1, padx=10)

        # 页码导航
        nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_frame.pack(pady=10)

        # 当前页码
        self.current_page = 1 #要改
        self.total_pages = 5  # 总页数 要改

        prev_button = ctk.CTkButton(nav_frame, text="<上一页", text_color="black", fg_color="gray",width=30,
                                    command=lambda: print("上一页"))
        prev_button.grid(row=0, column=0, padx=5)

        page_label = ctk.CTkLabel(nav_frame, text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页", font=("Arial", 12))
        page_label.grid(row=0, column=1, padx=5)

        next_button = ctk.CTkButton(nav_frame, text="下一页>", text_color="black", fg_color="gray",width=30,
                                    command=lambda: print("下一页"))
        next_button.grid(row=0, column=2, padx=5)


        # 表格行选中事件
        def on_table2_select(event):
            # 获取当前选中的行
            selected_item = table.selection()
            if selected_item:  # 如果有选中行
                view_image_button.configure(state="normal")  # 激活“查看图片”按钮
                view_data_button.configure(state="normal")  # 激活“查看数据”按钮
            else:
                view_image_button.configure(state="disabled")  # 禁用“查看图片”按钮
                view_data_button.configure(state="disabled")  # 禁用“查看数据”按钮

        # 绑定表格选中事件
        table.bind("<<TreeviewSelect>>", on_table2_select)


if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()
