"""
RPA-Python 简单演示
演示基本的文件操作和API功能
"""

import rpa

def main():
    print("=" * 60)
    print("RPA-Python 简单演示")
    print("=" * 60)

    # 1. 测试文件写入
    print("\n1. Testing file write...")
    test_content = """RPA-Python Demo File
====================
This is a test file demonstrating RPA-Python basic features.

Test Items:
- File write
- File read
- Text processing

Generated at:"""
    rpa.dump(test_content, 'rpa_test_output.txt')
    print("   [OK] File written: rpa_test_output.txt")

    # 2. 测试文件读取
    print("\n2. Testing file read...")
    content = rpa.load('rpa_test_output.txt')
    print(f"   [OK] File read, length: {len(content)} chars")
    print(f"   Preview: {content[:100]}...")

    # 3. 测试文件追加
    print("\n3. Testing file append...")
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rpa.write(f"\nLast modified: {timestamp}\n", 'rpa_test_output.txt')
    print("   [OK] Timestamp appended to file")

    # 4. 测试文本处理功能
    print("\n4. Testing text processing...")
    test_text = "Hello, [World]! This is a {Test}."

    # 删除指定字符
    cleaned = rpa.del_chars(test_text, "[]{}")
    print(f"   Original: {test_text}")
    print(f"   Cleaned: {cleaned}")

    # 获取中间文本
    source = "Start-CONTENT-End"
    extracted = rpa.get_text(source, "Start-", "-End")
    print(f"   Extracted: '{extracted}'")

    # 5. 测试剪贴板功能
    print("\n5. Testing clipboard...")
    rpa.clipboard("RPA-Python Demo Text")
    clipboard_content = rpa.clipboard()
    print(f"   [OK] Clipboard content: {clipboard_content}")

    # 6. 测试计时器功能
    print("\n6. Testing timer...")
    rpa.timer()  # 启动计时器
    import time
    time.sleep(0.1)  # 等待0.1秒
    elapsed = rpa.timer()  # 获取经过的时间
    print(f"   [OK] Elapsed time: {elapsed:.2f} seconds")

    # 7. 创建演示总结文件
    print("\n7. Creating summary...")
    summary = f"""
========================================
RPA-Python Demo Summary
========================================

Demo Time: {timestamp}

Tested Features:
[OK] dump() - File write
[OK] load() - File read
[OK] write() - File append
[OK] del_chars() - Remove characters
[OK] get_text() - Extract text
[OK] clipboard() - Clipboard operations
[OK] timer() - Timer function

Generated Files:
- rpa_test_output.txt (test output)
- rpa_demo_summary.txt (this summary)

========================================
"""
    rpa.dump(summary, 'rpa_demo_summary.txt')
    print("   [OK] Summary saved: rpa_demo_summary.txt")

    print("\n" + "=" * 60)
    print("RPA-Python Demo Completed!")
    print("=" * 60)
    print("\nTip: Check rpa_demo_summary.txt for results")

if __name__ == "__main__":
    main()
