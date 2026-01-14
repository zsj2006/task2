"""
网页自动化截屏脚本 - 配置文件版本
功能：通过配置文件管理所有参数，定时执行网页搜索和截屏
"""

import time
import os
import configparser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================== 配置管理 ====================

class Config:
    """配置管理器"""

    def __init__(self, config_file="config_automation.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        self.config.read(self.config_file, encoding='utf-8')
        self.log(f"配置文件加载成功: {self.config_file}")

    def get(self, section, key, fallback=None):
        """获取配置值"""
        try:
            return self.config.get(section, key)
        except:
            return fallback

    def getint(self, section, key, fallback=0):
        """获取整数配置值"""
        try:
            return self.config.getint(section, key)
        except:
            return fallback

    def getboolean(self, section, key, fallback=False):
        """获取布尔配置值"""
        try:
            return self.config.getboolean(section, key)
        except:
            return fallback

    @property
    def web_url(self):
        return self.get('web', 'url')

    @property
    def search_keyword(self):
        return self.get('web', 'keyword')

    @property
    def search_locator_type(self):
        return self.get('search_box', 'locator_type')

    @property
    def search_locator_value(self):
        return self.get('search_box', 'locator_value')

    @property
    def screenshot_dir(self):
        return self.get('screenshot', 'dir')

    @property
    def screenshot_prefix(self):
        return self.get('screenshot', 'prefix')

    @property
    def total_duration(self):
        return self.getint('execution', 'total_duration')

    @property
    def execution_interval(self):
        return self.getint('execution', 'interval')

    @property
    def browser_type(self):
        return self.get('browser', 'type')

    @property
    def headless_mode(self):
        return self.getboolean('browser', 'headless')

    @property
    def window_size(self):
        return self.get('browser', 'window_size')

    @property
    def log_file(self):
        return self.get('log', 'file')

    @property
    def log_level(self):
        return self.get('log', 'level')

    def log(self, message):
        """临时输出日志"""
        print(f"[Config] {message}")


# ==================== 日志工具 ====================

class Logger:
    """日志记录器"""

    def __init__(self, config):
        self.config = config
        self.log_file = config.log_file
        self.log_level = config.log_level

    def log(self, message, level="INFO"):
        """输出日志"""
        # 日志级别检查
        levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
        current_level = levels.get(self.log_level, 1)
        msg_level = levels.get(level, 1)

        if msg_level < current_level:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"

        # 输出到控制台
        print(log_message)

        # 输出到文件
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")


# ==================== 浏览器管理 ====================

class BrowserManager:
    """浏览器管理器"""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.driver = None

    def init_browser(self):
        """初始化浏览器"""
        try:
            self.logger.log(f"正在初始化 {self.config.browser_type.upper()} 浏览器...")

            if self.config.browser_type.lower() == "chrome":
                options = webdriver.ChromeOptions()

                if self.config.window_size:
                    options.add_argument(f"--window-size={self.config.window_size}")

                if self.config.headless_mode:
                    options.add_argument("--headless")

                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option("useAutomationExtension", False)

                self.driver = webdriver.Chrome(options=options)

            elif self.config.browser_type.lower() == "firefox":
                options = webdriver.FirefoxOptions()

                if self.config.headless_mode:
                    options.add_argument("--headless")

                self.driver = webdriver.Firefox(options=options)
            else:
                raise ValueError(f"不支持的浏览器类型: {self.config.browser_type}")

            self.driver.implicitly_wait(10)
            self.logger.log(f"{self.config.browser_type.upper()} 浏览器初始化成功")
            return True

        except Exception as e:
            self.logger.log(f"浏览器初始化失败: {e}", "ERROR")
            return False

    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.log("浏览器已关闭")
            except Exception as e:
                self.logger.log(f"关闭浏览器时出错: {e}", "ERROR")


# ==================== 自动化执行器 ====================

class WebAutomationExecutor:
    """网页自动化执行器"""

    def __init__(self, config, logger, driver):
        self.config = config
        self.logger = logger
        self.driver = driver
        self.execution_count = 0

    def open_page(self, url):
        """打开指定网页"""
        try:
            self.logger.log(f"正在打开网页: {url}")
            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
            )

            self.logger.log("网页加载成功")
            return True

        except Exception as e:
            self.logger.log(f"打开网页失败: {e}", "ERROR")
            return False

    def locate_search_box(self):
        """定位搜索栏"""
        try:
            locator_map = {
                "ID": By.ID,
                "NAME": By.NAME,
                "CLASS_NAME": By.CLASS_NAME,
                "XPATH": By.XPATH,
                "CSS_SELECTOR": By.CSS_SELECTOR,
                "TAG_NAME": By.TAG_NAME
            }

            locator_type = locator_map.get(self.config.search_locator_type.upper())
            if not locator_type:
                raise ValueError(f"不支持的定位方式: {self.config.search_locator_type}")

            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((locator_type, self.config.search_locator_value))
            )

            self.logger.log(f"搜索栏定位成功（方式: {self.config.search_locator_type}, 值: {self.config.search_locator_value}）")
            return search_box

        except Exception as e:
            self.logger.log(f"定位搜索栏失败: {e}", "ERROR")
            return None

    def input_keyword(self, search_box, keyword):
        """输入搜索关键词"""
        try:
            search_box.clear()
            search_box.send_keys(keyword)
            self.logger.log(f"已输入搜索关键词: {keyword}")
            return True

        except Exception as e:
            self.logger.log(f"输入关键词失败: {e}", "ERROR")
            return False

    def trigger_search(self, search_box):
        """触发搜索操作"""
        try:
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            self.logger.log("搜索已触发")
            return True

        except Exception as e:
            self.logger.log(f"触发搜索失败: {e}", "ERROR")
            try:
                search_box.submit()
                time.sleep(2)
                self.logger.log("搜索已触发（使用submit方法）")
                return True
            except:
                return False

    def take_screenshot(self):
        """截屏并保存"""
        try:
            os.makedirs(self.config.screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.config.screenshot_prefix}{timestamp}.png"
            filepath = os.path.join(self.config.screenshot_dir, filename)

            self.driver.save_screenshot(filepath)

            self.logger.log(f"截屏已保存: {filepath}")
            return filepath

        except Exception as e:
            self.logger.log(f"截屏失败: {e}", "ERROR")
            return None

    def execute_single_task(self):
        """执行单次完整任务"""
        try:
            self.execution_count += 1
            self.logger.log(f"========== 第 {self.execution_count} 次执行开始 ==========")

            if not self.open_page(self.config.web_url):
                return False

            search_box = self.locate_search_box()
            if not search_box:
                return False

            if not self.input_keyword(search_box, self.config.search_keyword):
                return False

            if not self.trigger_search(search_box):
                return False

            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return False

            self.logger.log(f"第 {self.execution_count} 次执行完成")
            return True

        except Exception as e:
            self.logger.log(f"执行任务时出错: {e}", "ERROR")
            return False


# ==================== 主程序 ====================

def main():
    """主程序入口"""
    # 加载配置
    try:
        config = Config()
    except Exception as e:
        print(f"配置加载失败: {e}")
        return

    # 初始化日志
    logger = Logger(config)

    logger.log("=" * 60)
    logger.log("网页自动化截屏脚本启动")
    logger.log("=" * 60)
    logger.log(f"目标网页: {config.web_url}")
    logger.log(f"搜索关键词: {config.search_keyword}")
    logger.log(f"总执行时长: {config.total_duration} 秒")
    logger.log(f"执行间隔: {config.execution_interval} 秒")
    logger.log(f"预计执行次数: {config.total_duration // config.execution_interval}")
    logger.log("=" * 60)

    # 初始化浏览器
    browser_manager = BrowserManager(config, logger)
    if not browser_manager.init_browser():
        logger.log("浏览器初始化失败，程序退出", "ERROR")
        return

    # 创建执行器
    executor = WebAutomationExecutor(config, logger, browser_manager.driver)

    # 记录开始时间
    start_time = time.time()
    end_time = start_time + config.total_duration

    # 主循环
    try:
        while time.time() < end_time:
            remaining_time = int(end_time - time.time())
            logger.log(f"剩余执行时间: {remaining_time} 秒 ({remaining_time // 60} 分 {remaining_time % 60} 秒)")

            success = executor.execute_single_task()

            if not success:
                logger.log("本次执行失败，将在间隔后继续重试", "WARN")

            if time.time() + config.execution_interval >= end_time:
                logger.log("时间不足，即将结束执行")
                break

            logger.log(f"等待 {config.execution_interval} 秒后执行下一次...")
            time.sleep(config.execution_interval)

    except KeyboardInterrupt:
        logger.log("用户中断执行", "WARN")

    finally:
        browser_manager.close_browser()

        logger.log("=" * 60)
        logger.log("执行完成")
        logger.log(f"总执行次数: {executor.execution_count}")
        logger.log(f"总运行时长: {int(time.time() - start_time)} 秒")
        logger.log(f"截屏保存目录: {os.path.abspath(config.screenshot_dir)}")
        logger.log("=" * 60)


if __name__ == "__main__":
    main()
