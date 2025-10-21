# utils/database.py
import subprocess
import sys
import time
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

# Global variables
mongodb_process = None
mongo_client = None
db = None

# Paths
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys._MEIPASS)
else:
    APP_DIR = Path(__file__).parent.parent

MONGODB_BIN = APP_DIR / "mongodb" / "bin" / "mongod.exe"
MONGODB_DATA = APP_DIR / "mongodb" / "data"

def start_mongodb():
    """Start MongoDB server"""
    global mongodb_process
    
    print("Starting MongoDB...")
    MONGODB_DATA.mkdir(parents=True, exist_ok=True)
    
    mongodb_process = subprocess.Popen(
        [str(MONGODB_BIN), "--dbpath", str(MONGODB_DATA), "--port", "27017", "--bind_ip", "127.0.0.1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    
    # Wait for MongoDB to start
    max_retries = 15
    for i in range(max_retries):
        time.sleep(1)
        try:
            import pymongo
            client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=1000)
            client.server_info()
            client.close()
            print(f"MongoDB started successfully after {i+1} seconds")
            return
        except:
            if i < max_retries - 1:
                print(f"Waiting for MongoDB... ({i+1}/{max_retries})")
            else:
                print("WARNING: MongoDB may not be fully started yet")

def stop_mongodb():
    """Stop MongoDB server"""
    global mongodb_process
    if mongodb_process:
        mongodb_process.terminate()
        mongodb_process.wait()

async def get_database():
    """Get database instance"""
    global mongo_client, db
    
    if db is None:
        mongo_client = AsyncIOMotorClient(
            "mongodb://localhost:27017",
            serverSelectionTimeoutMS=5000
        )
        await mongo_client.admin.command('ping')
        db = mongo_client.taste_paradise
        logger.info("Connected to database successfully")
    
    return db
