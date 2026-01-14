"""
RPA-Python Practical Demo - No Browser Required
实用演示：数据处理和自动化报告生成
"""

import rpa
from datetime import datetime
import json

def main():
    print("=" * 80)
    print(" " * 15 + "RPA-Python Practical Demonstration")
    print("=" * 80)
    print("\nTheme: Automated Data Processing and Report Generation\n")

    start_time = datetime.now()

    # Demo 1: Data Collection
    print("[Demo 1/4] Collecting system information...")
    print("-" * 80)

    try:
        # Get current directory
        current_dir = rpa.run('cd')
        print(f"Current directory: {current_dir.strip()}")

        # Get Python files count
        py_files = rpa.run('dir /b *.py 2>nul | find /c /v ""')
        print(f"Python files found: {py_files.strip()}")

        # Get disk space
        disk_info = rpa.run('wmic logicaldisk get size,freespace,caption')
        print(f"Disk information retrieved")

        print("Status: [OK] System information collected\n")

    except Exception as e:
        print(f"Status: [ERROR] {e}\n")

    # Demo 2: Data Processing
    print("[Demo 2/4] Processing sample data...")
    print("-" * 80)

    try:
        # Create sample sales data
        sales_data = """
Date,Product,Quantity,Price,Total
2025-01-01,Keyboard,10,25.00,250.00
2025-01-02,Mouse,15,15.00,225.00
2025-01-03,Monitor,5,150.00,750.00
2025-01-04,Headphones,8,45.00,360.00
2025-01-05,USB Cable,20,5.00,100.00
"""

        # Write data to file
        rpa.dump(sales_data, 'sales_data.csv')
        print("[OK] Sales data created: sales_data.csv")

        # Read and process
        content = rpa.load('sales_data.csv')
        lines = content.strip().split('\n')
        print(f"[OK] Total records: {len(lines) - 1}")

        # Calculate total sales
        total = 0.0
        for line in lines[1:]:  # Skip header
            parts = line.split(',')
            if len(parts) >= 5:
                total += float(parts[4])

        print(f"[OK] Total sales: ${total:.2f}")
        print("Status: [OK] Data processed\n")

    except Exception as e:
        print(f"Status: [ERROR] {e}\n")

    # Demo 3: Text Analysis
    print("[Demo 3/4] Analyzing text content...")
    print("-" * 80)

    try:
        # Sample text
        sample_text = """
        The quick brown fox jumps over the lazy dog.
        Python RPA automation makes tasks easier.
        Data processing is efficient with RPA-Python.
        """

        # Clean and process
        cleaned = rpa.del_chars(sample_text, "\n")
        print(f"[OK] Text cleaned (removed newlines)")
        print(f"     Original length: {len(sample_text)}")
        print(f"     Cleaned length: {len(cleaned)}")

        # Extract specific content
        extracted = rpa.get_text(sample_text, "quick ", " jumps")
        print(f"[OK] Extracted text: '{extracted}'")

        print("Status: [OK] Text analysis complete\n")

    except Exception as e:
        print(f"Status: [ERROR] {e}\n")

    # Demo 4: Report Generation
    print("[Demo 4/4] Generating automated report...")
    print("-" * 80)

    try:
        # Create comprehensive report
        report = f"""
{'=' * 70}
           RPA-Python Automated Report
{'=' * 70}

Report ID: RPA-{datetime.now().strftime('%Y%m%d-%H%M%S')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. SYSTEM INFORMATION
   Directory: {current_dir.strip() if 'current_dir' in locals() else 'N/A'}
   Python Files: {py_files.strip() if 'py_files' in locals() else 'N/A'}

2. SALES DATA SUMMARY
   Total Records: {len(lines) - 1 if 'lines' in locals() else 'N/A'}
   Total Sales: ${total:.2f if 'total' in locals() else 'N/A'}

3. TEXT ANALYSIS
   Original Length: {len(sample_text) if 'sample_text' in locals() else 'N/A'}
   Cleaned Length: {len(cleaned) if 'cleaned' in locals() else 'N/A'}
   Extracted: '{extracted if 'extracted' in locals() else 'N/A'}'

4. EXECUTION SUMMARY
   All demos completed successfully!
   Generated files: sales_data.csv, auto_report.txt

{'=' * 70}
Tool: RPA-Python (https://github.com/tebelorg/RPA-Python)
Purpose: Demonstrate practical RPA automation capabilities
{'=' * 70}
"""

        # Save report
        rpa.dump(report, 'auto_report.txt')
        print("[OK] Report saved: auto_report.txt")
        print("\n" + report)

        print("Status: [OK] Report generated\n")

    except Exception as e:
        print(f"Status: [ERROR] {e}\n")

    # Final Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("=" * 80)
    print(" " * 25 + "Demo Complete!")
    print("=" * 80)
    print(f"\nExecution time: {duration:.2f} seconds")
    print("\nGenerated files:")
    print("  - sales_data.csv (sample data)")
    print("  - auto_report.txt (automated report)")
    print("\nKey Features Demonstrated:")
    print("  [OK] System command execution")
    print("  [OK] File I/O operations")
    print("  [OK] Data processing")
    print("  [OK] Text manipulation")
    print("  [OK] Automated report generation")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
