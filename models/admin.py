# models/admin.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Admin(BaseModel):
    admin_id: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    created_at: Optional[datetime] = None

class AdminLogin(BaseModel):
    admin_id: str
    password: str
