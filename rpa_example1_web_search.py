"""
RPA 示例 1: 网页搜索自动化
功能：打开百度搜索关键词，获取结果并截图
"""

import rpa

def web_search_automation():
    """网页搜索自动化示例"""

    # 初始化 RPA
    rpa.init()

    try:
        print("=== 开始网页搜索自动化 ===\n")

        # 1. 打开百度
        print("1. 打开百度首页...")
        rpa.url('https://www.baidu.com')

        # 2. 在搜索框输入关键词
        print("2. 输入搜索关键词 'Python RPA'...")
        rpa.type('//*[@id="kw"]', 'Python RPA[enter]')

        # 3. 等待搜索结果加载
        print("3. 等待搜索结果加载...")
        rpa.wait(3)

        # 4. 获取页面标题
        print("4. 获取页面标题...")
        page_title = rpa.title()
        print(f"   页面标题: {page_title}")

        # 5. 截图保存
        print("5. 保存截图...")
        rpa.snap('page', 'baidu_search_result.png')
        print(f"   截图已保存: baidu_search_result.png")

        # 6. 获取搜索结果文本
        print("6. 获取搜索结果文本...")
        page_text = rpa.text()
        print(f"   页面文本长度: {len(page_text)} 字符")

        # 保存到文件
        rpa.dump(page_text[:500], 'search_result.txt')
        print("   搜索结果前500字符已保存到: search_result.txt")

        print("\n=== 网页搜索自动化完成 ===")

    except Exception as e:
        print(f"执行出错: {e}")

    finally:
        # 关闭浏览器
        rpa.close()

if __name__ == "__main__":
    web_search_automation()
