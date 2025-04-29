# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Data configuration
DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
EXCEL_FILE = os.getenv("EXCEL_FILE", os.path.join(DATA_DIR, "sample_leaves.xlsx"))

# Server configuration
SERVER_NAME = os.getenv("SERVER_NAME", "LeaveManagement")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
