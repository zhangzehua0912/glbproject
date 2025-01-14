#删减版


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


    def show_data_analysis(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


    def show_data_prediction(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = CorrosionDatabaseApp()
    app.mainloop()
