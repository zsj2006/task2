"""
RPA 示例 4: 多任务综合自动化
功能：综合演示网页导航、数据提取、文件保存等操作
"""

from rpa import r
from datetime import datetime

def multi_task_automation():
    """多任务综合自动化示例"""

    r.init()

    try:
        print("=== 开始多任务综合自动化 ===\n")

        # 创建日志文件
        log_file = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        r.write(f"=== 自动化执行日志 ===\n开始时间: {datetime.now()}\n\n", log_file)

        # 任务 1: 访问新闻网站
        print("【任务 1】访问新闻网站...")
        r.write(f"[{datetime.now()}] 任务1: 访问新闻网站\n", log_file)
        r.url('https://news.ycombinator.com')
        r.wait(2)
        r.snap('page', 'hacker_news.png')
        r.write(f"   - Hacker News 截图已保存\n", log_file)
        print("   ✓ Hacker News 截图已保存")

        # 任务 2: 访问 GitHub Trending
        print("\n【任务 2】访问 GitHub Trending...")
        r.write(f"[{datetime.now()}] 任务2: 访问 GitHub Trending\n", log_file)
        r.url('https://github.com/trending')
        r.wait(2)
        page_title = r.title()
        r.write(f"   - 页面标题: {page_title}\n", log_file)
        print(f"   ✓ 页面标题: {page_title}")

        # 任务 3: 访问 Python 官网
        print("\n【任务 3】访问 Python 官网...")
        r.write(f"[{datetime.now()}] 任务3: 访问 Python 官网\n", log_file)
        r.url('https://www.python.org')
        r.wait(2)
        r.snap('page', 'python_org.png')
        r.write(f"   - Python.org 截图已保存\n", log_file)
        print("   ✓ Python.org 截图已保存")

        # 任务 4: 使用 DOM 操作获取信息
        print("\n【任务 4】使用 DOM 操作...")
        r.write(f"[{datetime.now()}] 任务4: DOM 操作\n", log_file)
        r.url('https://www.example.com')
        r.wait(1)

        # 执行 JavaScript 获取页面信息
        page_info = r.dom('document.location.href')
        r.write(f"   - 当前URL: {page_info}\n", log_file)
        print(f"   ✓ 当前URL: {page_info}")

        # 任务 5: 生成总结报告
        print("\n【任务 5】生成总结报告...")
        r.write(f"\n[{datetime.now()}] 任务5: 生成总结报告\n", log_file)
        summary = f"""
========================================
自动化任务执行总结
========================================
执行时间: {datetime.now()}
完成任务数: 5
- 新闻网站访问: ✓
- GitHub Trending: ✓
- Python 官网访问: ✓
- DOM 操作: ✓
- 报告生成: ✓

生成的文件:
1. hacker_news.png - Hacker News 截图
2. python_org.png - Python.org 截图
3. {log_file} - 执行日志
========================================
"""
        r.dump(summary, 'automation_summary.txt')
        r.write(summary, log_file)
        print("   ✓ 总结报告已生成: automation_summary.txt")

        print("\n=== 多任务综合自动化完成 ===")
        print(f"日志文件: {log_file}")
        print(f"总结报告: automation_summary.txt")

    except Exception as e:
        print(f"执行出错: {e}")
        r.write(f"\n[ERROR] 执行出错: {e}\n", log_file)

    finally:
        r.close()

if __name__ == "__main__":
    multi_task_automation()
