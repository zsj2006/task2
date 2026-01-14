"""
RPA 示例 2: 天气数据抓取
功能：自动打开天气网站，抓取天气信息并保存
"""

from rpa import r

def scrape_weather_data():
    """抓取天气数据示例"""

    r.init()

    try:
        print("=== 开始天气数据抓取 ===\n")

        # 打开天气网站
        print("1. 打开天气网站...")
        r.url('https://www.weather.com')

        # 等待页面加载
        print("2. 等待页面加载...")
        r.wait(3)

        # 截图
        print("3. 保存页面截图...")
        r.snap('page', 'weather_page.png')
        print("   截图已保存: weather_page.png")

        # 获取页面标题
        page_title = r.title()
        print(f"4. 页面标题: {page_title}")

        # 获取当前URL
        current_url = r.url()
        print(f"5. 当前URL: {current_url}")

        # 保存页面文本
        page_text = r.text()
        r.dump(page_text[:1000], 'weather_data.txt')
        print("6. 天气数据已保存到: weather_data.txt")

        print("\n=== 天气数据抓取完成 ===")

    except Exception as e:
        print(f"执行出错: {e}")

    finally:
        r.close()

if __name__ == "__main__":
    scrape_weather_data()
