# src/leave_server.py
import sys
import os

# Add the project root directory to Python's module search path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from mcp.server.fastmcp import FastMCP
from src.data_manager import DataManager
from src.config import SERVER_NAME
from datetime import datetime
from typing import List, Dict, Optional

# Initialize MCP server
mcp = FastMCP(
    SERVER_NAME,
    dependencies=[
        "pandas", 
        "openpyxl", 
        "python-dotenv"
    ]
)

# Initialize data manager
data_manager = DataManager()

@mcp.tool()
def get_employee_details(emp_id: str) -> Dict:
    """
    Get employee details by employee ID
    
    Args:
        emp_id: Employee ID to search for
        
    Returns:
        Dict containing employee information or error message
    """
    employee = data_manager.get_employee_by_id(emp_id)
    if employee:
        return employee.to_dict()
    return {"error": f"Employee with ID {emp_id} not found"}

@mcp.tool()
def get_monthly_leaves(month: str) -> List[Dict]:
    """
    Get all leaves for a specific month
    
    Args:
        month: Three letter month code (Jan, Feb, etc.)
        
    Returns:
        List of employees with leaves in that month
    """
    month = month.capitalize()[:3]
    leaves = data_manager.get_leaves_by_month(month)
    return leaves

@mcp.tool()
def get_leave_balance(emp_id: str) -> Dict:
    """
    Get remaining leave balance for an employee
    
    Args:
        emp_id: Employee ID
        
    Returns:
        Dict with leave balances by type
    """
    employee = data_manager.get_employee_by_id(emp_id)
    if not employee:
        return {"error": f"Employee with ID {emp_id} not found"}
    
    balance = data_manager.get_employee_leave_balance(emp_id)
    return {
        "employee": employee.name,
        "balance": balance
    }

@mcp.tool()
def search_employees_on_leave(date_str: str) -> List[Dict]:
    """
    Find all employees on leave on a specific date
    
    Args:
        date_str: Date in YYYY-MM-DD format
        
    Returns:
        List of employees on leave
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        month = target_date.strftime("%b")
        day = target_date.day
        
        results = []
        for emp in data_manager.employees:
            if month in emp.leaves:
                for leave_entry in emp.leaves[month]:
                    if str(day) in leave_entry:
                        results.append({
                            "emp_id": emp.emp_id,
                            "name": emp.name,
                            "leave_info": leave_entry
                        })
        return results
    except Exception as e:
        return {"error": f"Error processing date: {str(e)}"}

@mcp.resource("leave://employees")
def employees_resource() -> Dict:
    """Resource providing a list of all employees"""
    return {
        "count": len(data_manager.employees),
        "employees": [emp.to_dict() for emp in data_manager.employees]
    }

@mcp.resource("leave://calendar/{month}")
def month_calendar_resource(month: str) -> Dict:
    """Resource providing leave calendar for a specific month"""
    month = month.capitalize()[:3]
    leaves = data_manager.get_leaves_by_month(month)
    return {
        "month": month,
        "leaves": leaves
    }
