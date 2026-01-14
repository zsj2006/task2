# 网页自动化截屏脚本 - 使用说明

## 概述

本脚本用于自动化执行网页操作并定时截屏，适用于需要定期监控网页内容的场景。

## 功能特性

- ✅ 自动打开指定网页
- ✅ 在搜索栏输入关键词并触发搜索
- ✅ 自动截屏保存（带时间戳）
- ✅ 可配置执行时长和间隔
- ✅ 完善的异常处理
- ✅ 详细的运行日志
- ✅ 支持Chrome和Firefox浏览器

## 文件说明

### 1. web_automation_screenshot.py
**内置配置版本** - 所有配置在脚本开头直接修改

适合场景：快速测试、简单任务

### 2. web_automation_config.py + config_automation.ini
**外部配置版本** - 配置与代码分离

适合场景：生产环境、频繁修改配置

## 环境准备

### 安装Python依赖

```bash
pip install selenium
```

### 安装浏览器驱动

#### Chrome浏览器
1. 下载ChromeDriver：https://chromedriver.chromium.org/downloads
2. 将ChromeDriver放到系统PATH目录或脚本同级目录

#### Firefox浏览器
1. 下载GeckoDriver：https://github.com/mozilla/geckodriver/releases
2. 将GeckoDriver放到系统PATH目录或脚本同级目录

## 使用方法

### 方式一：内置配置版本

1. **修改配置**：编辑 `web_automation_screenshot.py` 文件开头的配置区域

```python
# 网页配置
WEB_URL = "https://www.baidu.com"        # 改为你的目标网址
SEARCH_KEYWORD = "2025年1月14日"         # 改为你的搜索关键词

# 搜索栏定位
SEARCH_LOCATOR_TYPE = "ID"              # 定位方式
SEARCH_LOCATOR_VALUE = "kw"             # 定位值

# 截屏保存路径
SCREENSHOT_DIR = "./screenshots"        # 保存目录

# 执行时间配置
TOTAL_DURATION = 300                    # 总时长（秒）
EXECUTION_INTERVAL = 30                 # 间隔（秒）
```

2. **运行脚本**：
```bash
python web_automation_screenshot.py
```

### 方式二：外部配置版本

1. **修改配置文件**：编辑 `config_automation.ini`

```ini
[web]
url = https://www.baidu.com
keyword = 2025年1月14日

[search_box]
locator_type = ID
locator_value = kw

[screenshot]
dir = ./screenshots
prefix = search_

[execution]
total_duration = 300
interval = 30
```

2. **运行脚本**：
```bash
python web_automation_config.py
```

## 配置说明

### 搜索栏定位方式

脚本支持多种定位方式，适用于不同网站：

| 定位方式 | 说明 | 示例 |
|---------|------|------|
| ID | 通过元素ID定位 | `locator_type = ID`<br>`locator_value = kw` |
| NAME | 通过name属性定位 | `locator_type = NAME`<br>`locator_value = q` |
| CLASS_NAME | 通过class名称定位 | `locator_type = CLASS_NAME`<br>`locator_value = search-input` |
| XPATH | 通过XPath表达式定位 | `locator_type = XPATH`<br>`locator_value = //input[@name='wd']` |
| CSS_SELECTOR | 通过CSS选择器定位 | `locator_type = CSS_SELECTOR`<br>`locator_value = input#s` |

### 不同网站的配置示例

#### 百度 (Baidu)
```ini
[web]
url = https://www.baidu.com
keyword = 测试关键词

[search_box]
locator_type = ID
locator_value = kw
```

#### Google
```ini
[web]
url = https://www.google.com
keyword = test keyword

[search_box]
locator_type = NAME
locator_value = q
```

#### 必应 (Bing)
```ini
[web]
url = https://www.bing.com
keyword = search term

[search_box]
locator_type = ID
locator_value = sb_form_q
```

#### 通用XPath示例
```ini
[search_box]
locator_type = XPATH
locator_value = //input[@type='search' or @type='text']
```

## 输出说明

### 日志输出示例

```
[2025-01-14 10:30:00] [INFO] ============================================================
[2025-01-14 10:30:00] [INFO] 网页自动化截屏脚本启动
[2025-01-14 10:30:00] [INFO] ============================================================
[2025-01-14 10:30:00] [INFO] 目标网页: https://www.baidu.com
[2025-01-14 10:30:00] [INFO] 搜索关键词: 2025年1月14日
[2025-01-14 10:30:00] [INFO] 总执行时长: 300 秒
[2025-01-14 10:30:00] [INFO] 执行间隔: 30 秒
[2025-01-14 10:30:00] [INFO] 预计执行次数: 10
[2025-01-14 10:30:00] [INFO] ============================================================
[2025-01-14 10:30:01] [INFO] 正在初始化 CHROME 浏览器...
[2025-01-14 10:30:02] [INFO] CHROME 浏览器初始化成功
[2025-01-14 10:30:02] [INFO] 剩余执行时间: 300 秒 (5 分 0 秒)
[2025-01-14 10:30:02] [INFO] ========== 第 1 次执行开始 ==========
[2025-01-14 10:30:02] [INFO] 正在打开网页: https://www.baidu.com
[2025-01-14 10:30:03] [INFO] 网页加载成功
[2025-01-14 10:30:03] [INFO] 搜索栏定位成功（方式: ID, 值: kw）
[2025-01-14 10:30:03] [INFO] 已输入搜索关键词: 2025年1月14日
[2025-01-14 10:30:03] [INFO] 搜索已触发
[2025-01-14 10:30:05] [INFO] 截屏已保存: ./screenshots/search_20250114_103005.png
[2025-01-14 10:30:05] [INFO] 第 1 次执行完成
[2025-01-14 10:30:05] [INFO] 等待 30 秒后执行下一次...
```

### 截屏文件命名

格式：`{前缀}{年月日}_{时分秒}.png`

示例：`search_20250114_103005.png`

## 常见问题

### 1. 浏览器驱动版本不匹配
**问题**：`selenium.common.exceptions.SessionNotCreatedException: Message: session not created`

**解决**：下载与浏览器版本匹配的驱动

### 2. 找不到搜索栏
**问题**：`定位搜索栏失败`

**解决**：
- 检查定位方式是否正确
- 使用浏览器开发者工具（F12）查看搜索框的HTML属性
- 尝试其他定位方式（如XPATH）

### 3. 截屏目录无权限
**问题**：`截屏失败: Permission denied`

**解决**：
- 修改保存路径为有权限的目录
- 以管理员身份运行脚本

### 4. 网页加载超时
**问题**：`打开网页失败`

**解决**：
- 检查网络连接
- 增加等待时间（修改代码中的等待参数）

## 高级用法

### 自定义操作流程

如需更复杂的操作流程，可以修改 `execute_single_task()` 方法，添加更多步骤：

```python
def execute_single_task(self):
    # 1. 打开网页
    self.open_page(WEB_URL)

    # 2. 登录操作（示例）
    # self.login(username, password)

    # 3. 导航到特定页面
    # self.navigate_to_page()

    # 4. 搜索
    search_box = self.locate_search_box()
    self.input_keyword(search_box, SEARCH_KEYWORD)
    self.trigger_search(search_box)

    # 5. 截屏
    self.take_screenshot()
```

### 无头模式运行

修改配置设置为无头模式（不显示浏览器窗口）：

**内置配置版本**：
```python
HEADLESS_MODE = True
```

**配置文件版本**：
```ini
[browser]
headless = true
```

### 调整执行频率

例如每10秒执行一次，持续1分钟：

```python
TOTAL_DURATION = 60     # 1分钟
EXECUTION_INTERVAL = 10  # 每10秒
```

## 退出方式

- **自动退出**：达到设定时长后自动停止
- **手动退出**：按 `Ctrl + C` 中断执行

## 许可证

MIT License
