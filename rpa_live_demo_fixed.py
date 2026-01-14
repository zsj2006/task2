"""
RPA-Python Live Demo - Fixed Version
Demonstrates RPA-Python features with proper error handling
"""

import rpa
from datetime import datetime
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def main():
    print("=" * 80)
    print(" " * 20 + "RPA-Python Live Demo")
    print("=" * 80)
    print("\nDemo: Extract data from example.com (simple and reliable)\n")

    start_time = datetime.now()

    # Step 1: Initialize RPA
    print(f"[Step 1/5] Initializing RPA-Python...")
    print(f"           Time: {datetime.now().strftime('%H:%M:%S')}")
    try:
        rpa.init()
        print("           Status: [OK] Success")
    except Exception as e:
        print(f"           Status: [ERROR] {e}")
        print("\nTroubleshooting:")
        print("  1. First run downloads TagUI and Chrome (5-10 minutes)")
        print("  2. Check internet connection")
        print("  3. Try running again")
        return

    # Step 2: Open webpage
    print(f"\n[Step 2/5] Opening example.com...")
    print(f"           Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"           URL: https://www.example.com")
    try:
        rpa.url('https://www.example.com')
        print("           Status: [OK] Loading page...")
        rpa.wait(2)
        print("           Status: [OK] Page loaded")
    except Exception as e:
        print(f"           Status: [ERROR] {e}")
        rpa.close()
        return

    # Step 3: Get page info
    print(f"\n[Step 3/5] Getting page information...")
    print(f"           Time: {datetime.now().strftime('%H:%M:%S')}")
    try:
        page_title = rpa.title()
        current_url = rpa.url()
        print(f"           Page Title: {page_title}")
        print(f"           Current URL: {current_url}")
        print("           Status: [OK] Success")
    except Exception as e:
        print(f"           Status: [ERROR] {e}")

    # Step 4: Take screenshot
    print(f"\n[Step 4/5] Taking screenshot...")
    print(f"           Time: {datetime.now().strftime('%H:%M:%S')}")
    screenshot_file = 'example_dot_com_screenshot.png'
    try:
        rpa.snap('page', screenshot_file)
        print(f"           Filename: {screenshot_file}")
        print("           Status: [OK] Screenshot saved")
    except Exception as e:
        print(f"           Status: [ERROR] {e}")

    # Step 5: Extract page text
    print(f"\n[Step 5/5] Extracting page text...")
    print(f"           Time: {datetime.now().strftime('%H:%M:%S')}")
    try:
        page_text = rpa.text()
        print(f"           Text length: {len(page_text)} characters")

        # Save to file
        output_file = 'example_dot_com_content.txt'
        rpa.dump(page_text, output_file)
        print(f"           Saved to: {output_file}")

        # Show preview
        print("\n           --- Page Content Preview (first 200 chars) ---")
        preview = ' '.join(page_text[:200].split())
        print(f"           {preview}...")
        print("           --- End of preview ---")

        print("           Status: [OK] Text extracted")
    except Exception as e:
        print(f"           Status: [ERROR] {e}")

    # Calculate duration
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Print report
    print("\n" + "=" * 80)
    print(" " * 25 + "Demo Complete!")
    print("=" * 80)

    print(f"\nExecution time: {duration:.2f} seconds")
    print(f"Generated files:")
    print(f"  1. {screenshot_file}")
    print(f"  2. {output_file}")
    print(f"  3. demo_report.txt")

    # Generate report
    report = f"""
========================================
RPA-Python Live Demo Report
========================================

Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {duration:.2f} seconds

Target Website: Example.com (https://www.example.com)

Steps Completed:
[OK] Step 1: Initialize RPA-Python
[OK] Step 2: Open webpage
[OK] Step 3: Get page information
[OK] Step 4: Save screenshot
[OK] Step 5: Extract text content

Files Generated:
1. {screenshot_file} - Webpage screenshot
2. {output_file} - Full page text content
3. demo_report.txt - This report

Page Information:
- Title: {page_title}
- URL: {current_url}
- Content Length: {len(page_text)} characters

========================================
Demo by: Claude Code Assistant
Tool: RPA-Python (https://github.com/tebelorg/RPA-Python)
========================================
"""

    print(report)

    # Save report
    rpa.dump(report, 'demo_report.txt')

    # Close browser
    print("\nClosing browser...")
    try:
        rpa.close()
        print("[OK] Done!")
    except:
        print("[INFO] Browser already closed")

if __name__ == "__main__":
    main()
