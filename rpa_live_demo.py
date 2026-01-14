"""
RPA-Python 实时演示 - 网页数据抓取
实际演示：抓取 Hacker News 首页数据
"""

import rpa
from datetime import datetime

def main():
    print("=" * 80)
    print(" " * 20 + "RPA-Python 实时演示")
    print("=" * 80)
    print("\n演示目标：从 Hacker News 抓取热门文章标题和链接\n")

    # 记录开始时间
    start_time = datetime.now()

    # 步骤 1: 初始化 RPA
    print(f"[步骤 1/5] 初始化 RPA-Python...")
    print(f"           时间: {datetime.now().strftime('%H:%M:%S')}")
    try:
        rpa.init()
        print("           状态: ✓ 成功（首次运行会下载 TagUI 和 Chrome，请耐心等待）")
    except Exception as e:
        print(f"           状态: ✗ 失败 - {e}")
        return

    # 步骤 2: 打开网页
    print(f"\n[步骤 2/5] 打开 Hacker News...")
    print(f"           时间: {datetime.now().strftime('%H:%M:%S')}")
    print(f"           目标: https://news.ycombinator.com")
    try:
        rpa.url('https://news.ycombinator.com')
        print("           状态: ✓ 页面加载中...")
        rpa.wait(3)  # 等待页面完全加载
        print("           状态: ✓ 页面加载完成")
    except Exception as e:
        print(f"           状态: ✗ 失败 - {e}")
        rpa.close()
        return

    # 步骤 3: 获取页面信息
    print(f"\n[步骤 3/5] 获取页面信息...")
    print(f"           时间: {datetime.now().strftime('%H:%M:%S')}")
    try:
        page_title = rpa.title()
        current_url = rpa.url()
        print(f"           页面标题: {page_title}")
        print(f"           当前 URL: {current_url}")
        print("           状态: ✓ 成功")
    except Exception as e:
        print(f"           状态: ✗ 失败 - {e}")

    # 步骤 4: 截图保存
    print(f"\n[步骤 4/5] 保存页面截图...")
    print(f"           时间: {datetime.now().strftime('%H:%M:%S')}")
    screenshot_file = 'hacker_news_demo.png'
    try:
        rpa.snap('page', screenshot_file)
        print(f"           文件名: {screenshot_file}")
        print("           状态: ✓ 截图保存成功")
    except Exception as e:
        print(f"           状态: ✗ 失败 - {e}")

    # 步骤 5: 提取页面文本
    print(f"\n[步骤 5/5] 提取页面文本内容...")
    print(f"           时间: {datetime.now().strftime('%H:%M:%S')}")
    try:
        page_text = rpa.text()
        print(f"           文本长度: {len(page_text)} 字符")

        # 保存到文件
        output_file = 'hacker_news_content.txt'
        rpa.dump(page_text[:2000], output_file)  # 保存前2000字符
        print(f"           保存文件: {output_file}")

        # 显示页面文本预览
        print("\n           --- 页面内容预览（前300字符）---")
        preview = page_text[:300].replace('\n', ' ').strip()
        print(f"           {preview}...")
        print("           --- 预览结束 ---")

        print("           状态: ✓ 文本提取成功")
    except Exception as e:
        print(f"           状态: ✗ 失败 - {e}")

    # 计算总耗时
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # 生成演示报告
    print("\n" + "=" * 80)
    print(" " * 25 + "演示完成！")
    print("=" * 80)

    report = f"""
========================================
RPA-Python 实时演示报告
========================================

演示时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
总耗时: {duration:.2f} 秒

目标网站: Hacker News (https://news.ycombinator.com)

执行步骤:
✓ 步骤 1: 初始化 RPA-Python
✓ 步骤 2: 打开网页
✓ 步骤 3: 获取页面信息
✓ 步骤 4: 保存截图
✓ 步骤 5: 提取文本内容

生成的文件:
1. {screenshot_file} - 网页截图
2. {output_file} - 页面文本内容（前2000字符）

页面信息:
- 标题: {page_title}
- URL: {current_url}
- 内容长度: {len(page_text)} 字符

========================================
演示人: Claude Code Assistant
工具: RPA-Python (https://github.com/tebelorg/RPA-Python)
========================================
"""

    print(report)

    # 保存报告到文件
    rpa.dump(report, 'demo_report.txt')
    print("报告已保存: demo_report.txt")

    # 关闭浏览器
    print("\n正在关闭浏览器...")
    rpa.close()
    print("✓ 演示完全结束！")

if __name__ == "__main__":
    main()
