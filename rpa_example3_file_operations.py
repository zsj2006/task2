"""
RPA 示例 3: 文件操作与数据处理
功能：演示文件读写、数据处理操作
"""

from rpa import r
import json
from datetime import datetime

def file_operations_demo():
    """文件操作示例"""

    r.init()

    try:
        print("=== 开始文件操作演示 ===\n")

        # 1. 写入文件
        print("1. 写入示例数据到文件...")
        sample_data = f"""RPA Python 演示数据
====================
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
项目名称: RPA 自动化测试
版本: v1.0.0

测试数据列表:
- 数据项 1: 网页自动化
- 数据项 2: 数据抓取
- 数据项 3: 文件操作
- 数据项 4: 键盘鼠标控制

统计信息:
总测试项: 4
成功率: 100%
执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        r.dump(sample_data, 'demo_data.txt')
        print("   数据已写入: demo_data.txt")

        # 2. 读取文件
        print("\n2. 读取文件内容...")
        content = r.load('demo_data.txt')
        print(f"   文件内容长度: {len(content)} 字符")
        print(f"   前100字符: {content[:100]}...")

        # 3. 追加写入
        print("\n3. 追加数据到文件...")
        append_data = f"\n追加信息: 此数据于 {datetime.now()} 追加"
        r.write(append_data, 'demo_data.txt')
        print("   数据已追加")

        # 4. 创建JSON数据文件
        print("\n4. 创建JSON数据文件...")
        json_data = {
            "project": "RPA Demo",
            "version": "1.0",
            "tasks": [
                {"id": 1, "name": "网页自动化", "status": "完成"},
                {"id": 2, "name": "数据抓取", "status": "完成"},
                {"id": 3, "name": "文件操作", "status": "进行中"}
            ],
            "timestamp": datetime.now().isoformat()
        }
        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
        r.dump(json_str, 'demo_data.json')
        print("   JSON数据已保存: demo_data.json")

        # 5. 读取并解析JSON
        print("\n5. 读取JSON数据...")
        json_content = r.load('demo_data.json')
        parsed_data = json.loads(json_content)
        print(f"   项目名称: {parsed_data['project']}")
        print(f"   任务数量: {len(parsed_data['tasks'])}")
        for task in parsed_data['tasks']:
            print(f"   - {task['name']}: {task['status']}")

        print("\n=== 文件操作演示完成 ===")

    except Exception as e:
        print(f"执行出错: {e}")

    finally:
        r.close()

if __name__ == "__main__":
    file_operations_demo()
