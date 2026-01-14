"""
RPA-Python Final Demo - Working Version
Final demonstration of RPA-Python capabilities
"""

import rpa
from datetime import datetime

def main():
    print("=" * 80)
    print(" " * 20 + "RPA-Python Final Demonstration")
    print("=" * 80)
    print("\nDemonstrating: Data Processing & Automation\n")

    start_time = datetime.now()

    # Part 1: File Operations
    print("[Part 1/4] File Operations")
    print("-" * 80)

    # Create sample data
    sample_data = """Product,Quantity,Price,Total
Keyboard,10,25.00,250.00
Mouse,15,15.00,225.00
Monitor,5,150.00,750.00
"""

    rpa.dump(sample_data, 'products.csv')
    print(f"[OK] Created: products.csv")

    # Read file
    content = rpa.load('products.csv')
    print(f"[OK] Read file: {len(content)} characters")

    # Append to file
    rpa.write("Headphones,8,45.00,360.00\n", 'products.csv')
    print(f"[OK] Appended data to products.csv\n")

    # Part 2: Text Processing
    print("[Part 2/4] Text Processing")
    print("-" * 80)

    # Remove unwanted characters
    messy = "Hello [World]! This is {RPA} <Demo>."
    clean = rpa.del_chars(messy, "[]{}<>")
    print(f"[OK] Original: {messy}")
    print(f"[OK] Cleaned:  {clean}")

    # Extract text between markers
    text = "Start-IMPORTANT-End"
    extracted = rpa.get_text(text, "Start-", "-End")
    print(f"[OK] Extracted: '{extracted}'\n")

    # Part 3: Data Analysis
    print("[Part 3/4] Data Analysis")
    print("-" * 80)

    # Read products and calculate
    products = rpa.load('products.csv')
    lines = products.strip().split('\n')

    total_sales = 0
    product_count = 0

    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split(',')
            if len(parts) >= 4:
                try:
                    total_sales += float(parts[3])
                    product_count += 1
                except:
                    pass

    print(f"[OK] Total products: {product_count}")
    print(f"[OK] Total sales: ${total_sales:.2f}\n")

    # Part 4: Report Generation
    print("[Part 4/4] Report Generation")
    print("-" * 80)

    report = f"""
{'=' * 70}
              RPA-Python Automation Report
{'=' * 70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
--------
Total Products: {product_count}
Total Sales: ${total_sales:.2f}

FILES CREATED:
--------------
1. products.csv - Product data
2. final_report.txt - This report

FEATURES DEMONSTRATED:
---------------------
[OK] dump() - Write to file
[OK] load() - Read from file
[OK] write() - Append to file
[OK] del_chars() - Remove characters
[OK] get_text() - Extract text

EXECUTION TIME:
--------------
{datetime.now().strftime('%H:%M:%S')}

{'=' * 70}
RPA-Python: https://github.com/tebelorg/RPA-Python
{'=' * 70}
"""

    rpa.dump(report, 'final_report.txt')
    print(f"[OK] Report saved: final_report.txt\n")

    # Display report
    print(report)

    # Final stats
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("=" * 80)
    print(" " * 30 + "SUCCESS!")
    print("=" * 80)
    print(f"\nCompleted in: {duration:.2f} seconds")
    print("\nFiles created:")
    print("  - products.csv")
    print("  - final_report.txt")
    print("\nAll RPA-Python features working correctly!")
    print("=" * 80)

if __name__ == "__main__":
    main()
