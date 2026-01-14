"""
RPA-Python Web Automation Demo
Demonstrates practical web automation using RPA-Python
"""

import rpa

def main():
    print("=" * 70)
    print("RPA-Python Web Automation Demo")
    print("=" * 70)

    # Initialize RPA
    print("\n[1/6] Initializing RPA-Python...")
    rpa.init()
    print("       [OK] RPA initialized successfully")

    try:
        # Navigate to example.com
        print("\n[2/6] Navigating to example.com...")
        rpa.url('https://www.example.com')
        rpa.wait(2)
        print("       [OK] Page loaded")

        # Get page title
        print("\n[3/6] Getting page information...")
        page_title = rpa.title()
        current_url = rpa.url()
        print(f"       [OK] Title: {page_title}")
        print(f"       [OK] URL: {current_url}")

        # Get page text
        print("\n[4/6] Extracting page content...")
        page_text = rpa.text()
        print(f"       [OK] Page text length: {len(page_text)} characters")

        # Save screenshot
        print("\n[5/6] Taking screenshot...")
        rpa.snap('page', 'example_com_screenshot.png')
        print("       [OK] Screenshot saved: example_com_screenshot.png")

        # Use DOM operation to get page info
        print("\n[6/6] Using DOM operations...")
        domain = rpa.dom('document.domain')
        print(f"       [OK] Domain: {domain}")

        # Save results to file
        print("\n[7/7] Saving results...")
        result = f"""
========================================
RPA-Python Web Automation Result
========================================

Execution Time: {rpa.timer()}

Page Information:
- Title: {page_title}
- URL: {current_url}
- Domain: {domain}
- Content Length: {len(page_text)} characters

Files Generated:
- example_com_screenshot.png (screenshot)
- web_automation_result.txt (this file)

========================================
"""
        rpa.dump(result, 'web_automation_result.txt')
        print("       [OK] Results saved: web_automation_result.txt")

        print("\n" + "=" * 70)
        print("Web Automation Demo Completed Successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] {e}")

    finally:
        # Close browser
        print("\nClosing browser...")
        rpa.close()
        print("[OK] Done!")

if __name__ == "__main__":
    main()
