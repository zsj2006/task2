import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import io
import os

class InvoiceViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("票据识别结果查看器 - 通用版")
        self.root.geometry("1600x900")

        # 数据
        self.pdf_path = None
        self.excel_path = None
        self.df = None
        self.png_files = []
        self.current_page = 0
        self.image_dir = None

        # 创建UI（先创建界面）
        self.create_widgets()

        # 选择PDF文件
        self.select_pdf_file()

    def select_pdf_file(self):
        """选择PDF文件"""
        pdf_path = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )

        if not pdf_path:
            # 用户取消选择，退出程序
            self.root.destroy()
            return

        self.pdf_path = pdf_path
        self.process_pdf()

    def process_pdf(self):
        """处理选中的PDF文件"""
        # 更新窗口标题
        pdf_name = os.path.basename(self.pdf_path)
        self.root.title(f"票据识别结果查看器 - {pdf_name}")

        # 创建图片缓存目录
        base_name = os.path.splitext(pdf_name)[0]
        self.image_dir = f"{base_name}_pages_cache"
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        # 自动生成PNG图片
        self.generate_pdf_images()

        # 查找对应的Excel文件
        self.find_excel_file(base_name)

        # 加载PNG文件列表
        self.load_png_files()

        # 更新表格数据
        if self.df is not None:
            self.refresh_table()

        # 显示第一页
        if len(self.png_files) > 0:
            self.show_page(0)

    def find_excel_file(self, base_name):
        """查找与PDF同名的Excel文件"""
        # 尝试多种可能的Excel文件名
        possible_names = [
            f"{base_name}.xlsx",
            f"{base_name}.xls",
            f"{base_name}_增强识别结果.xlsx",
            f"{base_name}_识别结果.xlsx",
            f"{os.path.basename(base_name)}_增强识别结果.xlsx",
        ]

        pdf_dir = os.path.dirname(self.pdf_path)

        for name in possible_names:
            # 先在同一目录查找
            path = os.path.join(pdf_dir, name)
            if os.path.exists(path):
                self.excel_path = path
                self.load_data()
                print(f"找到Excel文件: {path}")
                return

            # 再在当前工作目录查找
            path = os.path.join(".", name)
            if os.path.exists(path):
                self.excel_path = path
                self.load_data()
                print(f"找到Excel文件: {path}")
                return

        print("未找到对应的Excel文件")

    def generate_pdf_images(self):
        """生成PDF页面的PNG图片"""
        print(f"正在处理PDF: {self.pdf_path}")

        try:
            pdf_doc = fitz.open(self.pdf_path)
            zoom = 4.0  # 高分辨率

            for page_num in range(len(pdf_doc)):
                image_path = os.path.join(self.image_dir, f"page_{page_num + 1}.png")

                # 检查是否已存在
                if os.path.exists(image_path):
                    print(f"  页面 {page_num + 1} PNG已存在，跳过")
                    continue

                try:
                    page = pdf_doc[page_num]
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)
                    img_data = pix.tobytes("png")

                    # 直接保存PNG数据
                    with open(image_path, 'wb') as f:
                        f.write(img_data)

                    print(f"  [OK] 生成页面 {page_num + 1} PNG图片")
                except Exception as e:
                    print(f"  [ERROR] 生成页面 {page_num + 1} 失败: {e}")

            print(f"PDF页面PNG图片生成完成，共 {len(pdf_doc)} 页")
            pdf_doc.close()

        except Exception as e:
            messagebox.showerror("错误", f"处理PDF失败: {e}")

    def load_data(self):
        """加载Excel数据"""
        try:
            self.df = pd.read_excel(self.excel_path, skiprows=[0, 1])
            self.df = self.df.dropna(how='all')
            self.df = self.df.reset_index(drop=True)
            print(f"成功加载 {len(self.df)} 条记录")
        except Exception as e:
            print(f"加载Excel失败: {e}")
            self.df = pd.DataFrame()

    def load_png_files(self):
        """加载PNG图片文件列表"""
        if not self.image_dir or not os.path.exists(self.image_dir):
            print(f"错误: 图片目录不存在 {self.image_dir}")
            return

        # 获取所有PNG文件并按文件名排序
        png_files = [f for f in os.listdir(self.image_dir) if f.endswith('.png')]
        png_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]) if '_' in x else 0)

        self.png_files = [os.path.join(self.image_dir, f) for f in png_files]
        print(f"成功加载 {len(self.png_files)} 个PNG图片文件")

    def refresh_table(self):
        """刷新表格数据"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 获取列名并删除"发票代码"列
        if self.df is not None and len(self.df.columns) > 0:
            columns = list(self.df.columns)
            columns = [col for col in columns if col != '发票代码']

            # 同时从DataFrame中删除该列
            if '发票代码' in self.df.columns:
                self.df = self.df.drop(columns=['发票代码'])

            # 更新表格列
            self.tree['columns'] = columns
            for col in columns:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
                self.tree.column(col, width=100, anchor='w')

            # 填充数据
            for idx, row in self.df.iterrows():
                self.tree.insert('', 'end', iid=idx, values=list(row))

            # 更新统计标签
            self.stats_label.config(text=f"共 {len(self.df)} 条记录")

    def create_widgets(self):
        """创建界面组件"""
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ==================== 左侧面板：Excel数据 ====================
        left_frame = tk.Frame(main_paned, width=600, bg='#f0f0f0')
        main_paned.add(left_frame, minsize=500)

        tk.Label(
            left_frame,
            text="票据识别数据表",
            font=("微软雅黑", 14, "bold"),
            bg='#f0f0f0'
        ).pack(pady=10)

        # 表格容器
        table_container = tk.Frame(left_frame, bg='#f0f0f0')
        table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 表格区域（包含表格和垂直滚动条）
        table_frame = tk.Frame(table_container)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 初始化表格（空表格）
        columns = []
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.column('#0', width=0, stretch=False)

        # 垂直滚动条（右侧）
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        # pack布局：表格和垂直滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # 水平滚动条（在表格下方，独立容器）
        hsb_frame = tk.Frame(table_container, height=25, bg='#cccccc', relief=tk.SUNKEN, bd=1)
        hsb_frame.pack(side=tk.BOTTOM, fill=tk.X)
        hsb_frame.pack_propagate(False)  # 固定高度

        hsb = ttk.Scrollbar(hsb_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.tree.configure(xscrollcommand=hsb.set)

        # 绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.on_row_click)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<F2>', lambda e: self.edit_selected_cell())

        # 点击时获取焦点，确保滚轮可用
        self.tree.bind('<Button-1>', self.on_tree_click)

        # 启用鼠标滚轮（Windows）
        self.tree.bind('<MouseWheel>', self.on_tree_mousewheel)
        # 启用鼠标滚轮（Linux）
        self.tree.bind('<Button-4>', lambda e: self.tree.yview_scroll(-1, "units"))
        self.tree.bind('<Button-5>', lambda e: self.tree.yview_scroll(1, "units"))

        # 统计信息和文件操作
        stats_frame = tk.Frame(left_frame, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, padx=5, pady=5)

        # 打开新文件按钮
        tk.Button(
            stats_frame,
            text="📂 打开新PDF",
            command=self.select_pdf_file,
            width=12,
            bg='#9370db',
            fg='white',
            font=("微软雅黑", 9, "bold")
        ).pack(side=tk.LEFT, padx=5)

        self.stats_label = tk.Label(
            stats_frame,
            text="共 0 条记录",
            font=("微软雅黑", 10),
            bg='#f0f0f0'
        )
        self.stats_label.pack(side=tk.LEFT, padx=5)

        # 编辑按钮组
        edit_btn_frame = tk.Frame(left_frame, bg='#f0f0f0')
        edit_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            edit_btn_frame,
            text="➕ 添加新行",
            command=self.add_new_row,
            width=10,
            bg='#50c878',
            fg='white',
            font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            edit_btn_frame,
            text="✏️ 编辑",
            command=self.edit_selected_cell,
            width=8,
            bg='#4a90e2',
            fg='white',
            font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            edit_btn_frame,
            text="🗑️ 删除",
            command=self.delete_selected_row,
            width=8,
            bg='#dc143c',
            fg='white',
            font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            edit_btn_frame,
            text="💾 保存",
            command=self.save_to_excel,
            width=8,
            bg='#ffa500',
            fg='white',
            font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            edit_btn_frame,
            text="🧹 清除数据",
            command=self.clear_data,
            width=10,
            bg='#808080',
            fg='white',
            font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=2)

        # ==================== 右侧面板：PDF显示 ====================
        right_frame = tk.Frame(main_paned, bg='white')
        main_paned.add(right_frame, minsize=800)

        # PDF标题栏（显示缩放比例）
        pdf_header = tk.Frame(right_frame, bg='white', height=50)
        pdf_header.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(
            pdf_header,
            text="PNG图片预览",
            font=("微软雅黑", 14, "bold"),
            bg='white',
            fg='#2e8b57'
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            pdf_header,
            text=f"(高分辨率PNG)",
            font=("微软雅黑", 10),
            bg='white',
            fg='#4169e1'
        ).pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(
            pdf_header,
            text="第 1 页 | 100%",
            font=("微软雅黑", 12),
            bg='white',
            fg='blue'
        )
        self.page_label.pack(side=tk.RIGHT, padx=5)

        # PDF图片容器
        pdf_container = tk.Frame(right_frame, bg='gray90')
        pdf_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 创建Canvas
        self.canvas = tk.Canvas(pdf_container, bg='white')

        # 垂直滚动条（右侧）
        canvas_vsb = ttk.Scrollbar(pdf_container, orient="vertical", command=self.canvas.yview)
        canvas_vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # 水平滚动条（底部）
        canvas_hsb = ttk.Scrollbar(pdf_container, orient="horizontal", command=self.canvas.xview)
        canvas_hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # 配置Canvas滚动条
        self.canvas.configure(yscrollcommand=canvas_vsb.set, xscrollcommand=canvas_hsb.set)

        # Canvas最后pack（确保在滚动条之后）
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ==================== 缩放控制面板 ====================
        control_panel = tk.Frame(right_frame, bg='#e0e0e0', relief=tk.RAISED, bd=2)
        control_panel.pack(fill=tk.X, padx=5, pady=10)

        # 第一行：翻页
        row1 = tk.Frame(control_panel, bg='#e0e0e0')
        row1.pack(fill=tk.X, pady=5)

        tk.Label(row1, text="翻页：", font=("微软雅黑", 10, "bold"), bg='#e0e0e0').pack(side=tk.LEFT, padx=5)

        tk.Button(
            row1, text="◀ 上一页", command=lambda: self.change_page(-1),
            width=10, height=2, bg='#4a90e2', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            row1, text="下一页 ▶", command=lambda: self.change_page(1),
            width=10, height=2, bg='#4a90e2', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        # 第二行：缩放按钮和提示
        row2 = tk.Frame(control_panel, bg='#e0e0e0')
        row2.pack(fill=tk.X, pady=5)

        tk.Label(row2, text="缩放：", font=("微软雅黑", 10, "bold"), bg='#e0e0e0').pack(side=tk.LEFT, padx=5)

        # 放大按钮
        tk.Button(
            row2, text="➕ 放大 (+)", command=lambda: self.zoom_by_step(0.1),
            width=10, height=2, bg='#50c878', fg='white', font=("微软雅黑", 9, "bold")
        ).pack(side=tk.LEFT, padx=3)

        # 缩小按钮
        tk.Button(
            row2, text="➖ 缩小 (-)", command=lambda: self.zoom_by_step(-0.1),
            width=10, height=2, bg='#ff6347', fg='white', font=("微软雅黑", 9, "bold")
        ).pack(side=tk.LEFT, padx=3)

        # 使用说明
        tk.Label(
            row2,
            text="| 提示: 鼠标滚轮也可缩放",
            font=("微软雅黑", 9),
            bg='#e0e0e0',
            fg='#666666'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            row2, text="适应窗口", command=self.fit_to_window,
            width=8, height=2, bg='#ffa500', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.RIGHT, padx=3)

        # 缩放比例滑块
        row3 = tk.Frame(control_panel, bg='#e0e0e0')
        row3.pack(fill=tk.X, pady=5)

        tk.Label(row3, text="手动缩放：", font=("微软雅黑", 10), bg='#e0e0e0').pack(side=tk.LEFT, padx=5)

        self.scale_slider = tk.Scale(
            row3,
            from_=50,
            to=300,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change,
            bg='#e0e0e0',
            font=("微软雅黑", 9),
            showvalue=0
        )
        self.scale_slider.set(200)  # 默认200%
        self.scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 第三行：旋转
        row4 = tk.Frame(control_panel, bg='#e0e0e0')
        row4.pack(fill=tk.X, pady=5)

        tk.Label(row4, text="旋转：", font=("微软雅黑", 10, "bold"), bg='#e0e0e0').pack(side=tk.LEFT, padx=5)

        tk.Button(
            row4, text="↺ 左转90°", command=lambda: self.rotate(-90),
            width=10, height=2, bg='#9370db', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            row4, text="↻ 右转90°", command=lambda: self.rotate(90),
            width=10, height=2, bg='#9370db', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            row4, text="⇄ 水平", command=self.flip_h,
            width=8, height=2, bg='#dc143c', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            row4, text="⇅ 垂直", command=self.flip_v,
            width=8, height=2, bg='#dc143c', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            row4, text="🔄 重置", command=self.reset_transform,
            width=8, height=2, bg='#696969', fg='white', font=("微软雅黑", 9)
        ).pack(side=tk.LEFT, padx=3)

        # ==================== 初始化参数 ====================
        self.zoom_factor = 2.0  # 默认放大
        self.rotation_angle = 90  # 默认横版
        self.flip_horizontal = False
        self.flip_vertical = False
        self.pdf_image = None
        self.pdf_image_tk = None
        self.base_image = None  # 原始图片（未缩放）

        # 绑定缩放事件
        self.bind_zoom_events()

    def bind_zoom_events(self):
        """绑定所有缩放相关事件"""
        # Canvas滚轮事件
        self.canvas.bind('<MouseWheel>', self.on_mousewheel)
        self.canvas.bind('<Button-4>', self.on_mousewheel_linux)
        self.canvas.bind('<Button-5>', self.on_mousewheel_linux)

        # 键盘快捷键
        self.root.bind('<plus>', lambda e: self.zoom_by_step(0.1))
        self.root.bind('<equal>', lambda e: self.zoom_by_step(0.1))
        self.root.bind('<minus>', lambda e: self.zoom_by_step(-0.1))
        self.root.bind('<underscore>', lambda e: self.zoom_by_step(-0.1))

        # 让Canvas可以接收事件
        self.canvas.bind('<Button-1>', self.on_canvas_click)

    def on_canvas_click(self, event):
        """点击Canvas时获取焦点"""
        self.canvas.focus_set()

    def on_slider_change(self, value):
        """滑块拖动缩放"""
        self.zoom_factor = float(value) / 100.0
        self.refresh_display()
        self.update_page_label()

    def on_mousewheel(self, event):
        """鼠标滚轮缩放 (Windows) - 参考HTML代码实现"""
        # 参考HTML代码中的逻辑：deltaY < 0 表示向上滚动（放大）
        scale_step = 0.1  # 10%步长

        if event.delta < 0:
            # 向上滚动 = 放大
            self.zoom_factor = min(self.zoom_factor + scale_step, 3.0)
        else:
            # 向下滚动 = 缩小
            self.zoom_factor = max(self.zoom_factor - scale_step, 0.5)

        self.refresh_display()
        self.update_page_label()
        self.update_slider()

        # 阻止事件传播
        return 'break'

    def on_mousewheel_linux(self, event):
        """Linux滚轮缩放"""
        scale_step = 0.1

        if event.num == 4:
            self.zoom_factor = min(self.zoom_factor + scale_step, 3.0)
        elif event.num == 5:
            self.zoom_factor = max(self.zoom_factor - scale_step, 0.5)

        self.refresh_display()
        self.update_page_label()
        self.update_slider()
        return 'break'

    def zoom_by_step(self, step):
        """按步长缩放（键盘快捷键）"""
        self.zoom_factor = max(0.5, min(self.zoom_factor + step, 3.0))
        self.refresh_display()
        self.update_page_label()
        self.update_slider()

    def update_slider(self):
        """更新滑块位置"""
        self.scale_slider.set(int(self.zoom_factor * 100))

    def update_page_label(self):
        """更新页码标签"""
        self.page_label.config(
            text=f"第 {self.current_page + 1} / {len(self.png_files)} 页 | {int(self.zoom_factor * 100)}%"
        )

    def on_tree_click(self, event):
        """点击表格时获取焦点，确保滚轮可用"""
        self.tree.focus_set()

    def on_tree_mousewheel(self, event):
        """表格滚轮事件（Windows）"""
        # 向上滚动（delta < 0）= 向下查看内容
        scroll_units = int(-1 * (event.delta / 120))
        if scroll_units != 0:
            self.tree.yview_scroll(scroll_units, "units")
        return 'break'

    def on_row_click(self, event):
        """处理行点击事件"""
        selection = self.tree.selection()
        if not selection:
            return

        idx = int(selection[0])

        if self.df is not None and idx < len(self.df):
            page_num = None
            for col in self.df.columns:
                if '票据序号' in str(col) or '序号' in str(col):
                    page_num = self.df.iloc[idx][col]
                    break

            if page_num is None:
                page_num = idx + 1

            try:
                page_num = int(page_num)
                self.show_page(page_num - 1)
            except:
                pass

    def on_double_click(self, event):
        """处理双击单元格事件"""
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return

        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item or not column:
            return

        row_idx = int(item)
        col_idx = int(column[1:]) - 1

        if self.df is None or row_idx >= len(self.df) or col_idx >= len(self.df.columns):
            return

        col_name = self.df.columns[col_idx]
        current_value = self.df.iloc[row_idx][col_name]

        self.edit_cell_dialog(row_idx, col_idx, col_name, current_value)

    def show_page(self, page_num):
        """显示PNG图片页面"""
        if page_num < 0 or page_num >= len(self.png_files):
            return

        self.current_page = page_num
        image_path = self.png_files[page_num]

        if not os.path.exists(image_path):
            print(f"警告: PNG文件不存在 {image_path}")
            return

        try:
            # 加载原始PNG图片（保持原始尺寸，不缩放）
            img = Image.open(image_path)
            self.base_image = img  # 保存原始图片作为基准

            # 根据当前缩放比例显示
            self.display_scaled_image()

        except Exception as e:
            print(f"加载PNG图片失败: {e}")

    def display_scaled_image(self):
        """根据当前缩放比例显示图片"""
        if self.base_image is None:
            return

        try:
            # 获取基准图片
            img = self.base_image.copy()

            # 计算原始尺寸（图片是用4倍DPI生成的）
            base_width = int(img.width / 4.0)
            base_height = int(img.height / 4.0)

            # 根据zoom_factor缩放
            new_width = int(base_width * self.zoom_factor)
            new_height = int(base_height * self.zoom_factor)

            # 高质量缩放
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 应用旋转变换
            img = self.apply_transform(img)

            # 更新显示
            self.pdf_image = img
            self.pdf_image_tk = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.pdf_image_tk)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            # 更新标签和滑块
            self.update_page_label()
            self.update_slider()

        except Exception as e:
            print(f"显示图片失败: {e}")

    def apply_transform(self, img):
        """应用翻转和旋转变换"""
        if self.rotation_angle != 0:
            img = img.rotate(self.rotation_angle, expand=True)

        if self.flip_horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if self.flip_vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

        return img

    def rotate(self, angle):
        """旋转图片"""
        self.rotation_angle = (self.rotation_angle + angle) % 360
        self.refresh_display()

    def flip_h(self):
        """水平翻转"""
        self.flip_horizontal = not self.flip_horizontal
        self.refresh_display()

    def flip_v(self):
        """垂直翻转"""
        self.flip_vertical = not self.flip_vertical
        self.refresh_display()

    def reset_transform(self):
        """重置变换"""
        self.rotation_angle = 90
        self.flip_horizontal = False
        self.flip_vertical = False
        self.zoom_factor = 2.0
        self.refresh_display()
        self.update_slider()
        self.update_page_label()

    def refresh_display(self):
        """刷新显示 - 根据当前缩放比例重新显示"""
        self.display_scaled_image()

    def change_page(self, delta):
        """翻页"""
        new_page = self.current_page + delta
        if 0 <= new_page < len(self.png_files):
            self.show_page(new_page)

    def fit_to_window(self):
        """适应窗口"""
        if self.base_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        if canvas_width > 1:
            # 计算原始尺寸（图片是用4倍DPI生成的）
            base_width = int(self.base_image.width / 4.0)

            # 考虑旋转（如果旋转了90度，宽度和高度会交换）
            if self.rotation_angle % 180 != 0:
                base_width = int(self.base_image.height / 4.0)

            # 计算合适的缩放比例
            scale = (canvas_width * 0.95) / base_width

            # 限制在合理范围内
            self.zoom_factor = max(0.5, min(scale, 3.0))

            self.refresh_display()
            self.update_slider()
            self.update_page_label()

    def edit_cell_dialog(self, row_idx, col_idx, col_name, current_value):
        """编辑单元格对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑: {col_name}")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"编辑单元格 - 第{row_idx + 1}行, {col_name}",
            font=("微软雅黑", 12, "bold"),
            fg='#4a90e2'
        ).pack(pady=10)

        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(frame, text="当前值:", font=("微软雅黑", 10)).pack(anchor='w')

        entry = tk.Entry(frame, font=("微软雅黑", 11))
        entry.insert(0, str(current_value) if current_value else "")
        entry.pack(fill=tk.X, pady=5)
        entry.focus_set()
        entry.select_range(0, tk.END)

        tk.Label(
            dialog,
            text="提示: 按 Enter 确认，按 Esc 取消",
            font=("微软雅黑", 9),
            fg='gray'
        ).pack(pady=5)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        def save_and_close():
            new_value = entry.get()
            self.df.iloc[row_idx, col_idx] = new_value
            self.tree.item(str(row_idx), values=list(self.df.iloc[row_idx]))
            dialog.destroy()
            self.stats_label.config(text=f"已更新: {col_name} → {new_value[:20]}...", fg='green')

        def cancel():
            dialog.destroy()

        tk.Button(
            btn_frame,
            text="✓ 保存",
            command=save_and_close,
            width=10,
            bg='#50c878',
            fg='white',
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="✗ 取消",
            command=cancel,
            width=10,
            bg='#dc143c',
            fg='white',
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT, padx=5)

        entry.bind('<Return>', lambda e: save_and_close())
        entry.bind('<Escape>', lambda e: cancel())

    def add_new_row(self):
        """添加新行"""
        if self.df is None:
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("添加新行")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="添加新记录",
            font=("微软雅黑", 14, "bold"),
            fg='#50c878'
        ).pack(pady=10)

        input_frame = tk.Frame(dialog)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        entries = {}
        for col_name in self.df.columns:
            row = tk.Frame(input_frame)
            row.pack(fill=tk.X, pady=3)

            tk.Label(
                row,
                text=f"{col_name}:",
                font=("微软雅黑", 9),
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)

            entry = tk.Entry(row, font=("微软雅黑", 9))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entries[col_name] = entry

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)

        def save_new_row():
            new_values = {}
            for col_name, entry in entries.items():
                new_values[col_name] = entry.get()

            self.df.loc[len(self.df)] = new_values
            self.tree.insert('', 'end', iid=len(self.df) - 1, values=list(new_values.values()))
            self.stats_label.config(text=f"共 {len(self.df)} 条记录", fg='green')
            dialog.destroy()
            messagebox.showinfo("成功", "新行已添加！", parent=self.root)

        def cancel():
            dialog.destroy()

        tk.Button(
            btn_frame,
            text="✓ 添加",
            command=save_new_row,
            width=10,
            bg='#50c878',
            fg='white',
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="✗ 取消",
            command=cancel,
            width=10,
            bg='#dc143c',
            fg='white',
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT, padx=5)

    def edit_selected_cell(self):
        """编辑选中的单元格"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一行！", parent=self.root)
            return

        item = selection[0]
        row_idx = int(item)

        if self.df is None or row_idx >= len(self.df):
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("选择要编辑的列")
        dialog.geometry("300x400")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"第 {row_idx + 1} 行 - 选择列",
            font=("微软雅黑", 12, "bold"),
            fg='#4a90e2'
        ).pack(pady=10)

        listbox_frame = tk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            listbox_frame,
            font=("微软雅黑", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        for col_name in self.df.columns:
            listbox.insert(tk.END, f"{col_name}: {self.df.iloc[row_idx][col_name]}")

        def edit_column():
            selection = listbox.curselection()
            if not selection:
                return

            col_idx = selection[0]
            col_name = self.df.columns[col_idx]
            current_value = self.df.iloc[row_idx][col_name]

            dialog.destroy()
            self.edit_cell_dialog(row_idx, col_idx, col_name, current_value)

        tk.Button(
            dialog,
            text="✓ 编辑",
            command=edit_column,
            width=12,
            bg='#4a90e2',
            fg='white',
            font=("微软雅黑", 10)
        ).pack(pady=10)

        listbox.bind('<Double-1>', lambda e: edit_column())

    def delete_selected_row(self):
        """删除选中的行"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择要删除的行！", parent=self.root)
            return

        item = selection[0]
        row_idx = int(item)

        result = messagebox.askyesno(
            "确认删除",
            f"确定要删除第 {row_idx + 1} 行吗？",
            parent=self.root
        )

        if result:
            self.df = self.df.drop(row_idx)
            self.df = self.df.reset_index(drop=True)
            self.tree.delete(item)

            for old_iid in self.tree.get_children():
                self.tree.item(old_iid, values=list(self.df.iloc[int(old_iid)]))

            self.stats_label.config(text=f"共 {len(self.df)} 条记录", fg='red')
            messagebox.showinfo("成功", "行已删除！", parent=self.root)

    def save_to_excel(self):
        """保存到Excel文件"""
        if self.df is None or len(self.df) == 0:
            messagebox.showwarning("提示", "没有数据可保存！", parent=self.root)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            initialfile="345_票据识别结果_已修改.xlsx",
            parent=self.root
        )

        if not file_path:
            return

        try:
            self.df.to_excel(file_path, index=False, engine='openpyxl')
            messagebox.showinfo("成功", f"数据已保存到:\n{file_path}", parent=self.root)
            self.stats_label.config(text=f"已保存", fg='green')
        except Exception as e:
            messagebox.showerror("错误", f"保存失败:\n{str(e)}", parent=self.root)

    def clear_data(self):
        """清除所有数据"""
        if self.df is None or len(self.df) == 0:
            messagebox.showinfo("提示", "当前没有数据可清除", parent=self.root)
            return

        result = messagebox.askyesno(
            "确认清除",
            "确定要清除所有数据吗？此操作不可撤销！",
            parent=self.root
        )

        if result:
            # 清空 DataFrame
            self.df = pd.DataFrame()

            # 清空表格
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 更新统计标签
            self.stats_label.config(text=f"共 0 条记录", fg='red')

            messagebox.showinfo("成功", "所有数据已清除！", parent=self.root)

    def sort_by_column(self, col):
        """排序列"""
        if self.df is None:
            return

        self.df = self.df.sort_values(by=col)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, row in self.df.iterrows():
            self.tree.insert('', 'end', iid=idx, values=list(row))

def main():
    root = tk.Tk()
    app = InvoiceViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
