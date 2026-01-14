"""
网页自动化截屏脚本
功能：定时打开指定网页，搜索关键词，并保存截屏
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import Exception as SeleniumException


# ==================== 配置区域 ====================

# 网页配置
WEB_URL = "https://www.baidu.com"  # 目标网页地址
SEARCH_KEYWORD = "2025年1月14日"   # 搜索关键词

# 搜索栏定位配置（支持多种定位方式）
SEARCH_LOCATOR_TYPE = "ID"        # 定位方式: "ID", "NAME", "CLASS_NAME", "XPATH", "CSS_SELECTOR"
SEARCH_LOCATOR_VALUE = "kw"       # 定位值（百度搜索框的ID）

# 截屏保存路径配置
SCREENSHOT_DIR = "./screenshots"  # 截屏保存目录
SCREENSHOT_PREFIX = "search_"     # 截屏文件名前缀

# 执行时间配置
TOTAL_DURATION = 300              # 总执行时长（秒），默认5分钟
EXECUTION_INTERVAL = 30           # 单次执行间隔（秒），默认30秒

# 浏览器配置
BROWSER_TYPE = "chrome"           # 浏览器类型: "chrome" 或 "firefox"
HEADLESS_MODE = False             # 是否无头模式（不显示浏览器窗口）
WINDOW_SIZE = "1920,1080"         # 浏览器窗口大小

# 日志配置
LOG_FILE = "./automation.log"     # 日志文件路径


# ==================== 日志工具 ====================

class Logger:
    """简单的日志记录器"""

    @staticmethod
    def log(message, level="INFO"):
        """输出日志到控制台和文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"

        # 输出到控制台
        print(log_message)

        # 输出到文件
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")


# ==================== 浏览器管理 ====================

class BrowserManager:
    """浏览器管理器"""

    def __init__(self):
        self.driver = None

    def init_browser(self):
        """初始化浏览器"""
        try:
            Logger.log(f"正在初始化 {BROWSER_TYPE.upper()} 浏览器...")

            if BROWSER_TYPE.lower() == "chrome":
                options = webdriver.ChromeOptions()

                # 设置窗口大小
                if WINDOW_SIZE:
                    options.add_argument(f"--window-size={WINDOW_SIZE}")

                # 无头模式
                if HEADLESS_MODE:
                    options.add_argument("--headless")

                # 禁用自动化提示
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)

                self.driver = webdriver.Chrome(options=options)

            elif BROWSER_TYPE.lower() == "firefox":
                options = webdriver.FirefoxOptions()

                if WINDOW_SIZE:
                    width, height = WINDOW_SIZE.split(',')
                    options.set_preference("layout.css.devPixelsPerPx", "1.0")

                if HEADLESS_MODE:
                    options.add_argument("--headless")

                self.driver = webdriver.Firefox(options=options)
            else:
                raise ValueError(f"不支持的浏览器类型: {BROWSER_TYPE}")

            # 设置隐式等待
            self.driver.implicitly_wait(10)

            Logger.log(f"{BROWSER_TYPE.upper()} 浏览器初始化成功")
            return True

        except Exception as e:
            Logger.log(f"浏览器初始化失败: {e}", "ERROR")
            return False

    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                Logger.log("浏览器已关闭")
            except Exception as e:
                Logger.log(f"关闭浏览器时出错: {e}", "ERROR")


# ==================== 自动化执行器 ====================

class WebAutomationExecutor:
    """网页自动化执行器"""

    def __init__(self, browser_manager):
        self.browser_manager = browser_manager
        self.driver = browser_manager.driver
        self.execution_count = 0

    def open_page(self, url):
        """打开指定网页"""
        try:
            Logger.log(f"正在打开网页: {url}")
            self.driver.get(url)

            # 等待页面加载完成
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )

            Logger.log("网页加载成功")
            return True

        except Exception as e:
            Logger.log(f"打开网页失败: {e}", "ERROR")
            return False

    def locate_search_box(self):
        """定位搜索栏"""
        try:
            # 根据配置的定位方式查找搜索框
            locator_map = {
                "ID": By.ID,
                "NAME": By.NAME,
                "CLASS_NAME": By.CLASS_NAME,
                "XPATH": By.XPATH,
                "CSS_SELECTOR": By.CSS_SELECTOR,
                "TAG_NAME": By.TAG_NAME
            }

            locator_type = locator_map.get(SEARCH_LOCATOR_TYPE.upper())
            if not locator_type:
                raise ValueError(f"不支持的定位方式: {SEARCH_LOCATOR_TYPE}")

            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((locator_type, SEARCH_LOCATOR_VALUE))
            )

            Logger.log(f"搜索栏定位成功（方式: {SEARCH_LOCATOR_TYPE}, 值: {SEARCH_LOCATOR_VALUE}）")
            return search_box

        except Exception as e:
            Logger.log(f"定位搜索栏失败: {e}", "ERROR")
            return None

    def input_keyword(self, search_box, keyword):
        """输入搜索关键词"""
        try:
            # 清空搜索框
            search_box.clear()

            # 输入关键词
            search_box.send_keys(keyword)

            Logger.log(f"已输入搜索关键词: {keyword}")
            return True

        except Exception as e:
            Logger.log(f"输入关键词失败: {e}", "ERROR")
            return False

    def trigger_search(self, search_box):
        """触发搜索操作"""
        try:
            # 方法1: 按回车键
            search_box.send_keys(Keys.RETURN)

            # 等待搜索结果加载
            time.sleep(2)

            Logger.log("搜索已触发")
            return True

        except Exception as e:
            Logger.log(f"触发搜索失败: {e}", "ERROR")
            # 尝试方法2: 点击搜索按钮
            try:
                search_box.submit()
                time.sleep(2)
                Logger.log("搜索已触发（使用submit方法）")
                return True
            except:
                return False

    def take_screenshot(self):
        """截屏并保存"""
        try:
            # 创建保存目录
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{SCREENSHOT_PREFIX}{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)

            # 截屏
            self.driver.save_screenshot(filepath)

            Logger.log(f"截屏已保存: {filepath}")
            return filepath

        except Exception as e:
            Logger.log(f"截屏失败: {e}", "ERROR")
            return None

    def execute_single_task(self):
        """执行单次完整任务"""
        try:
            self.execution_count += 1
            Logger.log(f"========== 第 {self.execution_count} 次执行开始 ==========")

            # 1. 打开网页
            if not self.open_page(WEB_URL):
                return False

            # 2. 定位搜索栏
            search_box = self.locate_search_box()
            if not search_box:
                return False

            # 3. 输入关键词
            if not self.input_keyword(search_box, SEARCH_KEYWORD):
                return False

            # 4. 触发搜索
            if not self.trigger_search(search_box):
                return False

            # 5. 截屏保存
            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return False

            Logger.log(f"第 {self.execution_count} 次执行完成")
            return True

        except Exception as e:
            Logger.log(f"执行任务时出错: {e}", "ERROR")
            return False


# ==================== 主程序 ====================

def main():
    """主程序入口"""
    Logger.log("=" * 60)
    Logger.log("网页自动化截屏脚本启动")
    Logger.log("=" * 60)
    Logger.log(f"目标网页: {WEB_URL}")
    Logger.log(f"搜索关键词: {SEARCH_KEYWORD}")
    Logger.log(f"总执行时长: {TOTAL_DURATION} 秒")
    Logger.log(f"执行间隔: {EXECUTION_INTERVAL} 秒")
    Logger.log(f"预计执行次数: {TOTAL_DURATION // EXECUTION_INTERVAL}")
    Logger.log("=" * 60)

    # 初始化浏览器
    browser_manager = BrowserManager()
    if not browser_manager.init_browser():
        Logger.log("浏览器初始化失败，程序退出", "ERROR")
        return

    # 创建执行器
    executor = WebAutomationExecutor(browser_manager)

    # 记录开始时间
    start_time = time.time()
    end_time = start_time + TOTAL_DURATION

    # 主循环
    try:
        while time.time() < end_time:
            # 计算剩余时间
            remaining_time = int(end_time - time.time())
            Logger.log(f"剩余执行时间: {remaining_time} 秒 ({remaining_time // 60} 分 {remaining_time % 60} 秒)")

            # 执行单次任务
            success = executor.execute_single_task()

            if not success:
                Logger.log("本次执行失败，将在间隔后继续重试", "WARN")

            # 检查是否还有时间继续执行
            if time.time() + EXECUTION_INTERVAL >= end_time:
                Logger.log("时间不足，即将结束执行")
                break

            # 等待指定间隔
            Logger.log(f"等待 {EXECUTION_INTERVAL} 秒后执行下一次...")
            time.sleep(EXECUTION_INTERVAL)

    except KeyboardInterrupt:
        Logger.log("用户中断执行", "WARN")

    finally:
        # 关闭浏览器
        browser_manager.close_browser()

        # 输出统计信息
        Logger.log("=" * 60)
        Logger.log("执行完成")
        Logger.log(f"总执行次数: {executor.execution_count}")
        Logger.log(f"总运行时长: {int(time.time() - start_time)} 秒")
        Logger.log(f"截屏保存目录: {os.path.abspath(SCREENSHOT_DIR)}")
        Logger.log("=" * 60)


if __name__ == "__main__":
    main()
