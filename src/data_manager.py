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
        try:
            # Load the correct sheet (e.g., "Leaves-2025")
            df = pd.read_excel(self.excel_file, sheet_name="Leaves-2025")
            print(f"Successfully loaded Excel file: {self.excel_file}")
            print(f"Columns found: {df.columns.tolist()}")
            print(df.head())

            # Clean column names
            df.columns = [col.strip() for col in df.columns]

            # Prepare employee list
            self.employees = []
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            for idx, row in df.iterrows():
                emp_id = str(row.get("EMP ID", "")).strip() if not pd.isna(row.get("EMP ID")) else ""
                name = str(row.get("Name", "")).strip() if not pd.isna(row.get("Name")) else ""
                location = str(row.get("Location", "")).strip() if not pd.isna(row.get("Location")) else ""

                # Skip rows without an employee ID or name
                if not emp_id or not name:
                    print(f"Skipping row {idx} due to missing EMP ID or Name")
                    continue

                emp = {
                    "emp_id": emp_id,
                    "name": name,
                    "location": location,
                    "leaves": {}
                }

                for month in months:
                    if month in df.columns:
                        cell = row[month]
                        if pd.notna(cell) and str(cell).strip().upper() != "NIL":
                            # Normalize and split leave entries
                            leave_entries = [entry.strip() for entry in str(cell).split(",") if entry.strip()]
                            emp["leaves"][month] = leave_entries

                try:
                    self.employees.append(Employee.from_dict(emp))
                except Exception as e:
                    print(f"Error creating Employee for row {idx}: {emp}")
                    print(str(e))

            print(f"Loaded {len(self.employees)} employees.")
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            import traceback
            traceback.print_exc()
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
