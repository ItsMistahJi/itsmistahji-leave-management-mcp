import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import and run your server
from src.leave_server import mcp

if __name__ == "__main__":
    mcp.run()
