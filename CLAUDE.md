# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese invoice OCR recognition system built with Python. The project contains multiple tools:

1. **OCR Scripts** - Extract invoice information from PDF files using PaddleOCR
2. **Interactive Viewer** - GUI application for viewing and editing OCR results
3. **Calculator** - Simple calculator application

## Core Dependencies

- **PaddleOCR** - OCR recognition (Chinese/English)
- **PyMuPDF (fitz)** - PDF to image conversion
- **pandas/openpyxl** - Excel file generation and manipulation
- **Tkinter** - GUI framework
- **Pillow (PIL)** - Image processing

Install dependencies:
```bash
pip install paddleocr pymupdf pandas openpyxl pillow
```

## Running the Applications

### Interactive Invoice Viewer
```bash
python interactive_viewer.py
```
- Launches a GUI viewer for inspecting PDF pages and editing OCR results
- Automatically prompts for PDF file selection on startup
- Generates high-resolution PNG cache in `{pdf_name}_pages_cache/` directory

### OCR Recognition Scripts

For 234.pdf:
```bash
python cloudcode_ocr_234.py
```

For 345.pdf:
```bash
python cloudcode_ocr_345.py
```

Enhanced OCR with debug output:
```bash
python improved_ocr.py
```

### Calculator
```bash
python calculator.py
```

## Building Executable

### Quick Build
```bash
快速打包.bat
```
Silent build with minimal output.

### Full Build
```bash
打包程序.bat
```
Verbose build with progress indicators and error handling.

Both scripts:
1. Check/install PyInstaller
2. Clean old build files
3. Build `interactive_viewer.py` into `通用票据识别查看器.exe`
4. Copy executable to current directory
5. Clean up temporary files

## Architecture

### OCR Pipeline Pattern

All OCR scripts follow a common three-stage pipeline:

1. **PDF to Image Conversion** (`pdf_to_ocr_images`)
   - Opens PDF with PyMuPDF
   - Renders each page at 2-3x zoom for clarity
   - Converts to numpy array for PaddleOCR

2. **Text Recognition** (PaddleOCR)
   - Uses Chinese language model (`lang='ch'`)
   - Returns text fragments with confidence scores
   - Filters low-confidence results (threshold ~0.3-0.5)

3. **Information Extraction** (`parse_invoice_text`)
   - Regex-based field extraction from OCR text
   - Handles multiple invoice formats (VAT special, VAT ordinary, electronic, generic)
   - Calculates derived fields (tax amount, pre-tax amount)

### Data Schema

Standard invoice output fields:
- 票据序号 - Sequential page number
- 票据类型 - Invoice type classification
- 购买方名称/购买方统一信用代码 - Buyer information
- 销售方名称/销售方统一信用代码 - Seller information
- 项目名称 - Description of goods/services
- 金额（不含税）/税率(%)/税额/价税合计 - Financial breakdown

### Interactive Viewer Architecture

The `interactive_viewer.py` implements a split-pane GUI:

**Left Panel - Data Table:**
- Uses `ttk.Treeview` with dual scrollbars (horizontal + vertical)
- Loads Excel data with `skiprows=[0,1]` to bypass title rows
- Supports inline editing via double-click or F2
- Row operations: add, delete, sort

**Right Panel - PDF Preview:**
- Canvas-based PNG viewer with pan/zoom
- Image transformation: zoom (50%-300%), rotate (90°), flip (horizontal/vertical)
- High-resolution source images (4x DPI generation)
- Mouse wheel zoom, slider control, fit-to-window

**State Management:**
- `base_image` - Original PIL Image (unscaled reference)
- `zoom_factor` - Display scaling multiplier
- `rotation_angle/flip_horizontal/flip_vertical` - Transform state
- PNG cache directory auto-created on first load

### Excel Generation Pattern

All OCR scripts generate formatted Excel files:
- Title row with generation date and page count
- Styled header row (blue background #4472C4, white text)
- Thin borders on all cells
- Column width auto-adjustment
- Frozen header row for scrolling
- Auto-open with `os.startfile()`

## PDF Path Configuration

Scripts reference PDF files in parent directory:
- `cloudcode_ocr_234.py`: `../task1/批量发票/234.pdf`
- `cloudcode_ocr_345.py`: `../task1/345.pdf`
- `improved_ocr.py`: `../task1/345.pdf`

Adjust paths if project structure differs.
