def show_data_analysis(self):
    for widget in self.main_frame.winfo_children():
        widget.destroy()

    title_label = ctk.CTkLabel(self.main_frame, text="数据分析中心", font=("Arial", 20))
    title_label.grid(row=0, column=0, columnspan=6, pady=10)

    # 腐蚀规律类型选择
    rule_label = ctk.CTkLabel(self.main_frame, text="腐蚀规律类:")
    rule_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
    self.rule_combobox = ctk.CTkComboBox(self.main_frame, values=["请选择", "类型1", "类型2", "类型3"])  # 修改  后面通过if来选择
    self.rule_combobox.grid(row=1, column=1, pady=10, padx=10)

    # 腐蚀动力学方程选择
    formula_label = ctk.CTkLabel(self.main_frame, text="腐蚀动力学方程:")
    formula_label.grid(row=1, column=2, pady=10, padx=10, sticky="w")
    self.formula_combobox = ctk.CTkComboBox(self.main_frame,
                                            values=["线性 x=At+B", "抛物线", "对数", "Tedmon", "自定义方程"])
    self.formula_combobox.grid(row=1, column=3, pady=10, padx=10)

    # 自定义输入
    custom_formula_label = ctk.CTkLabel(self.main_frame,
                                        text="输入自定义方程,f(x)=a1*x+a2*x^2+a3*x^3...中a1,a2,a3…的值，以空格分隔")
    custom_formula_label.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="w")
    self.custom_formula_entry = ctk.CTkEntry(self.main_frame, width=200)
    self.custom_formula_entry.grid(row=2, column=3, pady=10, padx=10)

    # Analysis and Prediction Buttons
    analyze_button = ctk.CTkButton(self.main_frame, text="拟合", command=self.perform_analysis)
    analyze_button.grid(row=10, column=1, pady=20, padx=10)

    predict_button = ctk.CTkButton(self.main_frame, text="预测", command=self.perform_prediction)
    predict_button.grid(row=10, column=2, pady=20, padx=10)

    # 腐蚀数据集选择
    data_label = ctk.CTkLabel(self.main_frame, text="腐蚀数据集选择:")
    data_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    self.dataset_frames = []
    for i in range(6):
        dataset_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        dataset_frame.grid(row=3 + i, column=0, columnspan=6, pady=5, padx=10, sticky="w")
        self.dataset_frames.append(dataset_frame)

        checkbox = ctk.CTkCheckBox(dataset_frame, text=f"选项{i + 1}")
        checkbox.pack(side="left", padx=5)

        filename_entry = ctk.CTkEntry(dataset_frame, width=200)
        filename_entry.insert(0, f"腐蚀数据集2024-09-27.xlsx")
        filename_entry.pack(side="left", padx=5)

        preview_button = ctk.CTkButton(dataset_frame, text="预览", command=lambda: self.preview_data(i))
        preview_button.pack(side="left", padx=5)

        edit_button = ctk.CTkButton(dataset_frame, text="编辑", command=lambda: self.edit_data(i))
        edit_button.pack(side="left", padx=5)

        # 页码导航
        nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_frame.pack(pady=10)
        # 当前页码
        self.current_page = 1  # 要改
        self.total_pages = 5  # 总页数 要改
        prev_button = ctk.CTkButton(nav_frame, text="<上一页", text_color="black", fg_color="gray", width=30,
                                    command=lambda: print("上一页"))
        prev_button.grid(row=0, column=0, padx=5)
        page_label = ctk.CTkLabel(nav_frame, text=f"第 {self.current_page} 页 / 共 {self.total_pages} 页",
                                  font=("Arial", 12))
        page_label.grid(row=0, column=1, padx=5)
        next_button = ctk.CTkButton(nav_frame, text="下一页>", text_color="black", fg_color="gray", width=30,
                                    command=lambda: print("下一页"))
        next_button.grid(row=0, column=2, padx=5)