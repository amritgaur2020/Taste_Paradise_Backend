from fastapi import APIRouter, HTTPException
from datetime import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["taste_paradise"]
orders_collection = db["orders"]

# Create router
router = APIRouter(
    prefix="/api/payments",
    tags=["payments-legacy"]
)


@router.post("/{order_id}/mark-cash")
async def mark_order_as_cash(order_id: str):
    """Mark an order as paid with cash"""
    try:
        result = orders_collection.update_one(
            {"order_id": order_id},
            {
                "$set": {
                    "payment_method": "cash",
                    "payment_status": "paid",
                    "status": "paid",
                    "paid_at": datetime.now().isoformat()
                }
            }
        )
        
        if result.modified_count > 0:
            return {
                "success": True, 
                "message": "Order marked as cash payment",
                "order_id": order_id
            }
        else:
            raise HTTPException(status_code=404, detail="Order not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}")
async def cancel_order(order_id: str):
    """Cancel/delete an order"""
    try:
        result = orders_collection.delete_one({"order_id": order_id})
        
        if result.deleted_count > 0:
            return {
                "success": True, 
                "message": "Order cancelled successfully",
                "order_id": order_id
            }
        else:
            raise HTTPException(status_code=404, detail="Order not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
