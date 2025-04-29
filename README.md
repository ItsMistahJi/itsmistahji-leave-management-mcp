# Leave Management MCP Server

This repository contains a Model Context Protocol (MCP) server for managing employee leave in an organization. The server integrates with Excel workbooks containing employee leave data and provides tools for querying and analyzing leave records.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Troubleshooting](#troubleshooting)
- [Example Queries](#example-queries)


## Prerequisites

- Python 3.9+
- UV package manager
- Claude Desktop (or another MCP client)
- Excel workbook with leave data


## Project Structure

```
leave-management-mcp/
├── src/
│   ├── __init__.py
│   ├── config.py                # Configuration settings
│   ├── leave_server.py          # Main MCP server
│   ├── data_manager.py          # Data processing module
│   └── models/
│       ├── __init__.py
│       └── employee.py          # Employee data models
├── data/
│   └── leave_tracker.xlsx       # Excel workbook with leave data
├── main.py                      # Entry point wrapper
├── __init__.py                  # Root package marker
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation
```


## Installation

1. Clone this repository:

```bash
git clone https://github.com/ItsMistahJi/itsmistahji-leave-management-mcp.git
cd leave-management-mcp
```

2. Set up the Python environment with UV:

```bash
pip install uv
uv init .
```

3. Install dependencies:

```bash
uv add "mcp[cli]" pandas openpyxl python-dotenv PyPDF2
```


## Configuration

1. Create a `.env` file in the project root:

```
DATA_DIR=/path/to/your/data/directory
EXCEL_FILE=/path/to/your/data/directory/leave_tracker.xlsx
SERVER_NAME=LeaveManagement
DEBUG_MODE=True
```

2. Ensure your Excel workbook has the correct structure:
    - A sheet named "Leaves-2025" (or modify `data_manager.py` to use your sheet name)
    - Columns for "Sl No", "Name", "EMP ID", "Location", and month names ("Jan", "Feb", etc.)

## Running the Server

### Local Development Testing

```bash
# Test the server locally
uv run python -m src.leave_server

# Install in Claude Desktop for testing
uv run mcp install src/leave_server.py --name "Leave Management"
```


### VS Code Integration

Add this configuration to your VS Code settings:

```json
"mcpServers": {
  "LeaveManagement": {
    "type": "stdio",
    "command": "uv",
    "args": [
      "run",
      "--with",
      "mcp[cli],pandas,openpyxl,python-dotenv,PyPDF2",
      "mcp",
      "run",
      "/path/to/leave-management-mcp/src/leave_server.py"
    ]
  }
}
```

[

**Note:** Replace `/path/to/leave-management-mcp` with your actual project path.

## Troubleshooting

### "No module named 'src'" Error

This error occurs when Python can't find the 'src' package in its module search path.

**Solutions:**

1. Add `__init__.py` files to make src a proper package:

```bash
touch __init__.py
touch src/__init__.py
touch src/models/__init__.py
```

2. Modify your server script (leave_server.py) to include the path:

```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
```

3. Use the main.py wrapper in the root directory:

```python
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from src.leave_server import mcp
if __name__ == "__main__":
    mcp.run()
```


### "No module named 'pandas'" Error

This occurs when the environment running your server doesn't have pandas installed.

**Solutions:**

1. Ensure all dependencies are installed in the same environment:

```bash
uv add pandas openpyxl python-dotenv PyPDF2
```

2. Use the `--with` flag when running the server:

```bash
uv run --with "mcp[cli],pandas,openpyxl,python-dotenv,PyPDF2" mcp run src/leave_server.py
```


### Excel Data Loading Issues

If you encounter validation errors with Excel data:

1. Review and modify the `load_data` function in `data_manager.py` to match your Excel structure
2. Ensure the sheet name matches your Excel file
3. Check column names and handle NaN values properly

## Example Queries

Once your server is running, you can ask Claude:

- "Who is on leave today?"
- "Show me the leave balance for employee 12345"
- "List all employees on leave in April"
- "Get leave details for Arun S"
- "When did Jeeva Rao take leave in March?"


## Finding Logs for Debugging

- **Claude Desktop Logs:**
    - macOS: `~/Library/Logs/Claude/mcp.log`
    - Windows: `%APPDATA%\Claude\logs\mcp.log`
- **Print Statements:** Any `print()` statements in your server code will appear in the logs.

<div style="text-align: center">⁂</div>

[^1]: https://pplx-res.cloudinary.com/image/upload/v1745853684/user_uploads/YsPURfUCkpJOGgc/image.jpg

