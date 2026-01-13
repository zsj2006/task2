# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple calculator application built with Python and Tkinter. It provides a GUI calculator with basic arithmetic operations.

## Running the Application

```bash
python calculator.py
```

## Architecture

### Single-File Structure

The entire application is contained in `calculator.py`. It follows an object-oriented design pattern:

- **Calculator class** (lines 4-215): The main application class that encapsulates all calculator logic and UI components.

### State Management

The calculator maintains state through instance variables (lines 11-18):

- `current`: The currently displayed number (as string)
- `stored`: The previously stored number for operations (as float or None)
- `operation`: The pending operation symbol ('+', '-', '×', '÷')
- `new_input`: Boolean flag indicating if the next digit press starts a new number

### UI Layout

The interface uses Tkinter's grid geometry manager:
- Display area at row 0 (spans 4 columns)
- 5 rows of buttons (rows 1-5) with 4 columns each
- Row/column weights configured for equal spacing (lines 32-35)

### Event Handling

Button presses are routed through `button_click()` (line 75) which delegates to specialized methods:
- `digit_press()`: Number input
- `decimal_press()`: Decimal point handling
- `operation_press()`: Operator handling with immediate execution if chain operation
- `equals_press()`: Execute pending operation
- `clear_press()`: Reset all state
- `sign_press()`: Toggle positive/negative
- `percent_press()`: Convert to percentage

Keyboard input is handled via `key_press()` (line 181) which maps keyboard events to button actions:
- Number keys and operators map directly
- `*` → `×`, `/` → `÷`
- Enter/`=` triggers equals
- Backspace deletes last digit
- Escape clears

### Calculation Logic

The `calculate()` method (line 126) performs the actual arithmetic:
- Handles division by zero with "错误" error message
- Converts integer results to integers for cleaner display
- Rounds floating-point results to 10 decimal places to avoid precision issues
- All exceptions caught and displayed as "错误"
