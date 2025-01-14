def adjust_column_widths(table, columns, data):
    """根据表格内容动态调整列宽"""
    for col_index, col in enumerate(columns):
        # 初始宽度设置为标题的宽度
        max_width = len(col) * 10  # 标题宽度，调整比例为 10
        for row in data:
            try:
                # 获取每一行的列内容
                cell_value = str(row[col_index])
                # 动态调整宽度，按内容长度设置
                max_width = max(max_width, len(cell_value) * 10)  # 调整比例为 10
            except IndexError:
                continue
        # 设置列宽
        table.column(col, width=max_width)

# 示例数据
columns = ["文献类型", "标题", "作者", "期刊名称", "发布时间", "ISSN", "DOI", "URL", "操作"]
data = [
    ["JOUR", "A very long title example to adjust the width dynamically", "作者1", "期刊名称1", "2022-03-01", "2468-2276", "10.1016/xxxx", "https://example.com", "查看"],
    ["JOUR", "Short Title", "作者2", "期刊名称2", "2023-09-19", "0921-5093", "10.1016/yyyy", "https://example2.com", "查看"],
]

# 创建表格
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

# 插入数据
for row in data:
    table.insert("", "end", values=row)

# 调用动态调整列宽函数
adjust_column_widths(table, columns, data)
