# src/models/employee.py
from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional, Union
from datetime import date
import pandas as pd

class Employee(BaseModel):
    emp_id: str
    name: str
    location: str
    leaves: Dict[str, List[str]] = {}
    
    @field_validator('location', 'name', mode='before')
    @classmethod
    def handle_nan(cls, v):
        """Convert NaN values to empty strings"""
        if pd.isna(v):
            return ""
        return v
    
    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "location": self.location,
            "leaves": self.leaves
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
