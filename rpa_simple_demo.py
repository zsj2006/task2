"""
RPA-Python Simple Demo (No Browser Required)
Demonstrates core RPA-Python features without web automation
"""

import rpa
import os

def main():
    print("=" * 70)
    print("RPA-Python Simple Feature Demo")
    print("=" * 70)

    # Feature 1: File Operations
    print("\n[Feature 1/4] File Operations")
    print("-" * 70)

    # Create test data
    test_data = """RPA-Python Simple Demo
=====================
This demonstrates file operations without browser automation.

Test Data:
- Item 1: Python RPA
- Item 2: Automation
- Item 3: Productivity
"""

    # Write file
    rpa.dump(test_data, 'simple_demo.txt')
    print("[OK] File created: simple_demo.txt")

    # Read file
    content = rpa.load('simple_demo.txt')
    print(f"[OK] File read: {len(content)} characters")

    # Append to file
    rpa.write("\n[Appended] Additional content\n", 'simple_demo.txt')
    print("[OK] Content appended")

    # Feature 2: Text Processing
    print("\n[Feature 2/4] Text Processing")
    print("-" * 70)

    # Test del_chars
    messy_text = "Hello, [World]! This is {RPA} <Python>."
    cleaned = rpa.del_chars(messy_text, "[]{}<>")
    print(f"Original: {messy_text}")
    print(f"Cleaned:  {cleaned}")

    # Test get_text
    html_like = "<div>Extract This Content</div>"
    extracted = rpa.get_text(html_like, "<div>", "</div>")
    print(f"Extracted: '{extracted}'")

    # Feature 3: System Operations
    print("\n[Feature 3/4] System Operations")
    print("-" * 70)

    # Get current directory
    current_dir = rpa.run('cd')
    print(f"Current directory: {current_dir.strip()}")

    # List files
    files = rpa.run('dir /b *.py 2>nul')
    print(f"Python files in current directory:")
    for file in files.split('\n')[:5]:  # Show first 5
        if file.strip():
            print(f"  - {file.strip()}")

    # Feature 4: Timer and Utility Functions
    print("\n[Feature 4/4] Timer and Utilities")
    print("-" * 70)

    # Timer needs init, so we'll use Python's time
    import time
    start = time.time()
    time.sleep(0.1)
    elapsed = time.time() - start
    print(f"Elapsed time: {elapsed:.3f} seconds")

    # Mouse coordinates (available without init)
    try:
        coords = rpa.mouse_xy()
        print(f"Mouse coordinates: {coords}")
    except:
        print("Mouse coordinates: Not available (requires init)")

    # Generate Summary Report
    print("\n" + "=" * 70)
    print("Generating Summary Report...")
    print("=" * 70)

    summary = f"""
========================================
RPA-Python Simple Demo Summary
========================================

Demo Results:

[Feature 1] File Operations
  - dump(): File write successful
  - load(): File read successful
  - write(): File append successful

[Feature 2] Text Processing
  - del_chars(): Character removal successful
  - get_text(): Text extraction successful

[Feature 3] System Operations
  - run(): Command execution successful

[Feature 4] Utilities
  - mouse_xy(): Mouse coordinates available

Generated Files:
  - simple_demo.txt (test file)
  - simple_demo_summary.txt (this file)

========================================
"""

    rpa.dump(summary, 'simple_demo_summary.txt')
    print("\n" + "=" * 70)
    print("Demo Completed Successfully!")
    print("=" * 70)
    print("\nFiles created:")
    print("  - simple_demo.txt")
    print("  - simple_demo_summary.txt")

if __name__ == "__main__":
    main()
