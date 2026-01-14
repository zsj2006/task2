import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("计算器")
        self.root.geometry("350x450")
        self.root.resizable(False, False)

        # 当前显示的数字
        self.current = "0"
        # 存储的数字
        self.stored = None
        # 上一个操作符
        self.operation = None
        # 是否开始新输入
        self.new_input = True

        # 创建显示区域
        self.display = tk.Entry(
            root,
            font=('Arial', 24),
            justify='right',
            bd=5,
            relief=tk.SUNKEN
        )
        self.display.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky='nsew')
        self.display.insert(0, "0")

        # 配置行列权重，使按钮平均分配空间
        for i in range(5):
            root.grid_rowconfigure(i + 1, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        # 创建按钮
        buttons = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]

        for btn in buttons:
            if len(btn) == 3:
                text, row, col = btn
                colspan = 1
            else:
                text, row, col, colspan = btn

            button = tk.Button(
                root,
                text=text,
                font=('Arial', 18, 'bold'),
                command=lambda t=text: self.button_click(t)
            )

            # 设置颜色
            if text in '÷×-+=':
                button.config(bg='#ff9500', fg='white', activebackground='#ff8000')
            elif text in 'C±%':
                button.config(bg='#d4d4d2', activebackground='#c0c0c0')
            elif text == '=':
                button.config(bg='#ff9500', fg='white', activebackground='#ff8000')
            else:
                button.config(bg='#505050', fg='white', activebackground='#707070')

            button.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2, sticky='nsew')

        # 绑定键盘事件
        root.bind('<Key>', self.key_press)

    def button_click(self, text):
        if text.isdigit():
            self.digit_press(text)
        elif text == '.':
            self.decimal_press()
        elif text in '÷×-+':
            self.operation_press(text)
        elif text == '=':
            self.equals_press()
        elif text == 'C':
            self.clear_press()
        elif text == '±':
            self.sign_press()
        elif text == '%':
            self.percent_press()

        self.update_display()

    def digit_press(self, digit):
        if self.new_input:
            self.current = digit
            self.new_input = False
        else:
            if self.current == "0":
                self.current = digit
            else:
                self.current += digit

    def decimal_press(self):
        if self.new_input:
            self.current = "0."
            self.new_input = False
        else:
            if '.' not in self.current:
                self.current += '.'

    def operation_press(self, op):
        if self.stored is not None and not self.new_input:
            self.calculate()

        self.stored = float(self.current)
        self.operation = op
        self.new_input = True

    def equals_press(self):
        if self.stored is not None and self.operation:
            self.calculate()
            self.stored = None
            self.operation = None
            self.new_input = True

    def calculate(self):
        try:
            current_value = float(self.current)

            if self.operation == '+':
                result = self.stored + current_value
            elif self.operation == '-':
                result = self.stored - current_value
            elif self.operation == '×':
                result = self.stored * current_value
            elif self.operation == '÷':
                if current_value == 0:
                    self.current = "错误"
                    return
                result = self.stored / current_value
            else:
                return

            # 处理浮点数精度问题
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))

        except Exception:
            self.current = "错误"

    def clear_press(self):
        self.current = "0"
        self.stored = None
        self.operation = None
        self.new_input = True

    def sign_press(self):
        if self.current != "0" and self.current != "错误":
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    def percent_press(self):
        try:
            value = float(self.current)
            result = value / 100
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(round(result, 10))
        except:
            pass

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current)

    def key_press(self, event):
        key = event.char

        if key.isdigit():
            self.button_click(key)
        elif key == '.':
            self.button_click('.')
        elif key == '+':
            self.button_click('+')
        elif key == '-':
            self.button_click('-')
        elif key == '*':
            self.button_click('×')
        elif key == '/':
            self.button_click('÷')
        elif key == '\r' or key == '=':
            self.button_click('=')
        elif key == '\x08':  # Backspace
            if not self.new_input and len(self.current) > 1:
                self.current = self.current[:-1]
                self.update_display()
            elif not self.new_input and len(self.current) == 1:
                self.current = "0"
                self.new_input = True
                self.update_display()
        elif key == '\x1b':  # Escape
            self.button_click('C')

def main():
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
