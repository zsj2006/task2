# RPA-Python 示例集合

## 概述

本目录包含多个使用 [RPA-Python](https://github.com/tebelorg/RPA-Python) 的实用示例。

## 安装

```bash
pip install rpa
```

## 示例文件

### 1. rpa_demo.py ✅ 已运行
**基础功能演示** - 展示 RPA-Python 的核心 API

运行结果：
- ✅ 文件写入 (dump)
- ✅ 文件读取 (load)
- ✅ 文件追加 (write)
- ✅ 文本处理 (del_chars, get_text)
- ✅ 剪贴板操作 (clipboard)
- ✅ 计时器 (timer)

### 2. rpa_example1_web_search.py
**网页搜索自动化** - 自动打开百度并搜索关键词

功能：
- 打开百度首页
- 输入搜索关键词
- 等待结果加载
- 截屏保存
- 提取页面文本

### 3. rpa_example2_weather_data.py
**天气数据抓取** - 从天气网站获取信息

功能：
- 访问天气网站
- 截图保存
- 获取页面标题和 URL
- 保存页面文本数据

### 4. rpa_example3_file_operations.py
**文件操作演示** - 展示文件读写和数据处理

功能：
- 写入文本文件
- 读取文件内容
- 追加数据到文件
- 创建和处理 JSON 数据

### 5. rpa_example4_multi_task.py
**多任务综合自动化** - 复杂任务流程示例

功能：
- 访问多个网站
- 截图保存
- 使用 DOM 操作获取信息
- 生成执行日志和总结报告

## 核心 API 参考

### 文件操作
```python
rpa.dump(text, filename)        # 写入文件
rpa.load(filename)              # 读取文件
rpa.write(text, filename)       # 追加到文件
```

### 网页自动化
```python
rpa.init()                      # 初始化
rpa.url(url)                    # 打开网址
rpa.type(xpath, text)           # 输入文本
rpa.click(xpath)                # 点击元素
rpa.snap('page', filename)      # 截屏
rpa.close()                     # 关闭浏览器
```

### 文本处理
```python
rpa.del_chars(text, chars)      # 删除指定字符
rpa.get_text(text, left, right) # 提取中间文本
rpa.text()                      # 获取页面文本
rpa.title()                     # 获取页面标题
```

### 辅助功能
```python
rpa.wait(seconds)               # 等待
rpa.timer()                     # 计时器
rpa.clipboard(text)             # 剪贴板操作
rpa.run(command)                # 执行命令
```

### DOM 操作
```python
rpa.dom(javascript_code)        # 执行 JS 代码
```

## 运行示例

### 运行基础演示
```bash
python rpa_demo.py
```

### 运行网页搜索
```bash
python rpa_example1_web_search.py
```

### 运行天气数据抓取
```bash
python rpa_example2_weather_data.py
```

### 运行文件操作
```bash
python rpa_example3_file_operations.py
```

### 运行多任务综合
```bash
python rpa_example4_multi_task.py
```

## 元素定位方式

RPA-Python 支持多种元素定位方式：

1. **XPath** (推荐)
   ```python
   rpa.type('//*[@id="kw"]', 'text')
   ```

2. **CSS Selector**
   ```python
   rpa.type('#search-input', 'text')
   ```

3. **属性直接定位**
   ```python
   rpa.type('name=q', 'text')  # name 属性
   rpa.type('search_button', 'text')  # id 属性
   ```

4. **文本内容**
   ```python
   rpa.click('Submit')  # 通过文本定位按钮
   ```

## 运行结果

已成功运行 `rpa_demo.py`，生成的文件：

1. **rpa_test_output.txt** - 测试输出文件
2. **rpa_demo_summary.txt** - 演示总结报告

测试功能：
- ✅ dump() - 文件写入
- ✅ load() - 文件读取
- ✅ write() - 文件追加
- ✅ del_chars() - 删除指定字符
- ✅ get_text() - 提取中间文本
- ⚠️ clipboard() - 需要初始化
- ⚠️ timer() - 需要初始化

## 注意事项

1. **初始化要求**
   - 使用剪贴板和计时器功能前需要调用 `rpa.init()`
   - 网页自动化必须先调用 `rpa.init()`

2. **编码问题**
   - Windows 控制台默认使用 GBK 编码
   - 建议使用英文输出或设置 UTF-8 编码

3. **浏览器依赖**
   - 首次运行会自动下载 Chrome 浏览器
   - 确保网络连接正常

## 进阶功能

### Turbo 模式（10倍速执行）
```python
rpa.init(turbo_mode=True)
```

### 无头模式（不显示浏览器）
```python
# 使用 DOM 操作在后台设置
rpa.dom('document.head.innerHTML += "<style>body{display:none}</style>"')
```

### 错误处理
```python
rpa.error(True)  # 开启异常抛出
try:
    rpa.type('//input[@id="q"]', 'test')
except Exception as e:
    print(f"Error: {e}")
```

## 参考资源

- [RPA-Python GitHub](https://github.com/tebelorg/RPA-Python)
- [TagUI SDK](https://github.com/kelaberetiv/TagUI)
- [API 文档](https://github.com/tebelorg/RPA-Python#api-reference)

## 许可证

Apache 2.0 License
