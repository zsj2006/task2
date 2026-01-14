"""
测试编辑功能的诊断脚本
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# 创建测试数据
test_df = pd.DataFrame({
    '票据序号': [1, 2, 3],
    '票据类型': ['专用发票', '普通发票', '电子发票'],
    '购买方': ['公司A', '公司B', '公司C'],
    '销售方': ['供应商X', '供应商Y', '供应商Z'],
    '金额': [1000.0, 500.0, 750.0]
})

print("测试数据:")
print(test_df)
print("\n测试编辑功能...")

# 创建测试窗口
root = tk.Tk()
root.title("编辑功能测试")
root.geometry("600x400")

# 创建框架
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 创建表格
tree = ttk.Treeview(frame, columns=list(test_df.columns), show='headings')
for col in test_df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# 填充数据
for idx, row in test_df.iterrows():
    tree.insert('', 'end', iid=idx, values=list(row))

tree.pack(fill=tk.BOTH, expand=True)

# 测试双击事件
def on_double_click(event):
    region = tree.identify_region(event.x, event.y)
    if region != "cell":
        return

    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)

    if not item or not column:
        return

    row_idx = int(item)
    col_idx = int(column[1:]) - 1

    if row_idx >= len(test_df) or col_idx >= len(test_df.columns):
        return

    col_name = test_df.columns[col_idx]
    current_value = test_df.iloc[row_idx][col_name]

    print(f"\n双击编辑:")
    print(f"  行: {row_idx + 1}")
    print(f"  列: {col_name}")
    print(f"  当前值: {current_value}")

    # 创建编辑对话框
    dialog = tk.Toplevel(root)
    dialog.title(f"编辑: {col_name}")
    dialog.geometry("400x200")

    tk.Label(
        dialog,
        text=f"编辑: {col_name}",
        font=("微软雅黑", 12, "bold")
    ).pack(pady=10)

    entry = tk.Entry(dialog, font=("微软雅黑", 11))
    entry.insert(0, str(current_value) if current_value else "")
    entry.pack(fill=tk.X, padx=20, pady=10)
    entry.focus_set()
    entry.select_range(0, tk.END)

    def save_and_close():
        new_value = entry.get()
        test_df.iloc[row_idx, col_idx] = new_value
        tree.item(str(row_idx), values=list(test_df.iloc[row_idx]))
        dialog.destroy()
        print(f"  新值已保存: {new_value}")
        messagebox.showinfo("成功", f"已更新: {col_name} → {new_value}")

    def cancel():
        dialog.destroy()
        print("  取消编辑")

    btn_frame = tk.Frame(dialog)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="保存", command=save_and_close, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="取消", command=cancel, width=10).pack(side=tk.LEFT, padx=5)

    entry.bind('<Return>', lambda e: save_and_close())
    entry.bind('<Escape>', lambda e: cancel())

# 绑定双击事件
tree.bind('<Double-1>', on_double_click)

# 添加说明标签
info_label = tk.Label(
    root,
    text="💡 提示: 双击表格中的任意单元格进行编辑",
    font=("微软雅黑", 10),
    fg='blue'
)
info_label.pack(pady=5)

# 添加状态栏
status_bar = tk.Label(root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

print("\n✓ 测试窗口已启动")
print("✓ 双击任意单元格测试编辑功能\n")
print("关闭测试窗口继续...")

root.mainloop()
