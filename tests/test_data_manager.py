# src/data_manager.py
import pandas as pd
import os
from datetime import datetime
from src.config import EXCEL_FILE
from src.models.employee import Employee

class DataManager:
    def __init__(self, excel_file=EXCEL_FILE):
        self.excel_file = excel_file
        self.employees = []
        self.load_data()
        
    def load_data(self):
        """Load employee data from Excel"""
        try:
            df = pd.read_excel(self.excel_file)
            
            # Clean column names
            df.columns = [col.strip() for col in df.columns]
            
            # Convert to list of Employee objects
            self.employees = []
            for _, row in df.iterrows():
                emp = {
                    "emp_id": str(row.get("EMP ID", "")),
                    "name": row.get("Name", ""),
                    "location": row.get("Location", ""),
                    "leaves": {}
                }
                
                # Parse monthly leave data
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                
                for month in months:
                    if month in df.columns and pd.notna(row[month]):
                        emp["leaves"][month] = str(row[month]).split(",")
                
                self.employees.append(Employee.from_dict(emp))
                
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def get_employee_by_id(self, emp_id):
        """Find employee by ID"""
        for emp in self.employees:
            if emp.emp_id == emp_id:
                return emp
        return None
    
    def get_leaves_by_month(self, month):
        """Get all leaves for a specific month"""
        result = []
        for emp in self.employees:
            if month in emp.leaves and emp.leaves[month]:
                result.append({
                    "emp_id": emp.emp_id,
                    "name": emp.name,
                    "leaves": emp.leaves[month]
                })
        return result
    
    def get_employee_leave_balance(self, emp_id):
        """Calculate remaining leave balance"""
        # Implementation would depend on your business rules
        # This is a placeholder
        return {"annual": 10, "sick": 5, "personal": 3}
