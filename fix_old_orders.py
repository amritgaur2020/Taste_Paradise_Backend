# fix_old_orders.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

async def fix_existing_orders():
    """Fix orders that were paid via webhook but show no payment method"""
    
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.tasteparadise
    
    # Target specific orders
    order_ids = ["88a9c2f5", "1e1acdf5"]
    
    print(f"🔧 Fixing {len(order_ids)} orders...")
    
    for order_id in order_ids:
        result = await db.orders.update_one(
            {"order_id": order_id},
            {"$set": {
                "payment_method": "online",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        if result.modified_count > 0:
            print(f"✅ Fixed order: {order_id}")
        else:
            print(f"⚠️  Order not found or already fixed: {order_id}")
    
    print(f"\n✨ Done!")
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_existing_orders())
