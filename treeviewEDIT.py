'''Treeview控件本身不直接支持编辑单元格，但可以通过以下方法实现一个可编辑的表格：

捕捉鼠标事件：当用户双击某个单元格时，创建一个 Entry 或 CTkEntry 小部件，覆盖在该单元格上，用于编辑。

完成编辑：当用户按下回车键或点击其他地方时，保存更改并更新 Treeview 的值。'''
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class EditableTreeviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editable Treeview")

        # Frame容器
        pre_frame = ctk.CTkFrame(root, fg_color="transparent")
        pre_frame.pack(pady=20, padx=20, fill="both", expand=True)
        pre_frame.grid_columnconfigure(0, weight=1)

        # 数据输入表格Frame
        table_data_frame = ctk.CTkFrame(pre_frame, fg_color="transparent")
        table_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        table_data_frame.grid_columnconfigure(0, weight=1)

        # Treeview表格
        self.columns = ('x', 'y')
        self.treeview = ttk.Treeview(table_data_frame, columns=self.columns, show='headings')
        self.treeview.heading('x', text="X值")
        self.treeview.heading('y', text="Y值")
        self.treeview.grid(row=0, column=0, sticky="nsew")

        # 滚动条
        scrollbar3 = ttk.Scrollbar(table_data_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar3.set)
        scrollbar3.grid(row=0, column=1, sticky="ns")

        # 插入默认数据
        for i in range(30):
            self.treeview.insert('', 'end', values=(i, i ** 2))

        # 绑定双击事件
        self.treeview.bind('<Double-1>', self.on_double_click)

    def on_double_click(self, event):
        # 获取双击的单元格
        item_id = self.treeview.identify_row(event.y)  # 获取行ID
        column = self.treeview.identify_column(event.x)  # 获取列编号
        if not item_id or not column:
            return

        column_idx = int(column.replace('#', '')) - 1  # 列编号转索引
        selected_item = self.treeview.item(item_id, 'values')  # 获取选中行的数据

        # 创建Entry输入框
        x, y, width, height = self.treeview.bbox(item_id, column)
        entry = tk.Entry(self.treeview)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, selected_item[column_idx])  # 填入原值

        def save_edit(event=None):
            # 保存编辑后的值
            new_value = entry.get()
            values = list(selected_item)
            values[column_idx] = new_value
            self.treeview.item(item_id, values=values)
            entry.destroy()  # 删除输入框

        entry.bind('<Return>', save_edit)  # 按回车保存
        entry.bind('<FocusOut>', lambda e: entry.destroy())  # 失去焦点时销毁输入框
        entry.focus()  # 聚焦输入框

# 创建主窗口
root = ctk.CTk()
app = EditableTreeviewApp(root)
root.mainloop()
