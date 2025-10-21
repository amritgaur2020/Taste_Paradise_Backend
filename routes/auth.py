# routes/auth.py
from fastapi import APIRouter, HTTPException, Form
from datetime import datetime
from models.admin import Admin
from utils.auth import hash_password, verify_password
from utils.database import get_database

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.get("/check-admin")
async def check_admin_exists():
    """Check if admin account exists"""
    db = await get_database()
    admin = await db.admins.find_one({})
    return {"exists": admin is not None}

@router.post("/signup")
async def signup(admin: Admin):
    """Create admin account (first-time only)"""
    db = await get_database()
    
    # Check if admin already exists
    existing_admin = await db.admins.find_one({})
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists. Signup is disabled.")
    
    # Hash password
    hashed_password = hash_password(admin.password)
    
    # Save to database
    admin_data = {
        "admin_id": admin.admin_id,
        "password": hashed_password,
        "created_at": datetime.now()
    }
    
    result = await db.admins.insert_one(admin_data)
    return {"message": "Admin created successfully", "admin_id": admin.admin_id}

@router.post("/login")
async def login(admin_id: str = Form(...), password: str = Form(...)):
    """Login with credentials"""
    db = await get_database()
    
    # Find admin
    admin = await db.admins.find_one({"admin_id": admin_id})
    
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful", "admin_id": admin_id}

@router.post("/logout")
async def logout():
    """Logout"""
    return {"message": "Logged out successfully"}
