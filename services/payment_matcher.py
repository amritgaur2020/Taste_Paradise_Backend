# services/payment_matcher.py
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PaymentMatcher:
    """Service to handle payment matching logic"""
    
    def __init__(self, db):
        self.db = db
    
    async def find_matching_order(
        self, 
        amount: float, 
        timeout_minutes: int = 15,
        algorithm: str = "fifo"
    ) -> Optional[Dict[str, Any]]:
        """
        Find a pending order that matches the payment amount
        
        Args:
            amount: Payment amount to match
            timeout_minutes: Time window to search for pending orders
            algorithm: Matching algorithm (fifo, amount_time, manual)
        
        Returns:
            Matched order dict or None
        """
        try:
            # Calculate cutoff time
            cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)
            
            # Build query
            query = {
                "payment_status": "pending",
                "total": amount,
                "created_at": {"$gte": cutoff_time.isoformat()},
                "status": {"$ne": "cancelled"}
            }
            
            # Apply matching algorithm
            if algorithm == "fifo":
                # First In First Out - oldest order first
                sort_order = [("created_at", 1)]
            elif algorithm == "amount_time":
                # Closest to current time
                sort_order = [("created_at", -1)]
            else:
                # Manual - just return first match
                sort_order = [("created_at", 1)]
            
            # Find matching order
            matching_order = await self.db.orders.find_one(query, sort=sort_order)
            
            if matching_order:
                logger.info(f"Match found: Order {matching_order.get('orderid')} for ₹{amount}")
            else:
                logger.warning(f"No match found for amount ₹{amount}")
            
            return matching_order
            
        except Exception as e:
            logger.error(f"Error in payment matching: {str(e)}")
            return None
    
    async def mark_order_as_paid(
        self,
        order_id: str,
        transaction_id: str,
        payer_vpa: Optional[str] = None
    ) -> bool:
        """Mark an order as paid with transaction details"""
        try:
            update_data = {
                "payment_status": "paid",
                "payment_method": "online",
                "status": "served",
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "transaction_id": transaction_id
            }
            
            if payer_vpa:
                update_data["payer_vpa"] = payer_vpa
            
            result = await self.db.orders.update_one(
                {"_id": order_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error marking order as paid: {str(e)}")
            return False
    
    async def store_unmatched_payment(
        self,
        transaction_id: str,
        amount: float,
        payer_vpa: Optional[str] = None,
        provider: str = "soundbox"
    ) -> str:
        """Store an unmatched payment for later resolution"""
        try:
            from models.soundbox_models import UnmatchedPaymentModel
            
            unmatched = UnmatchedPaymentModel(
                transaction_id=transaction_id,
                amount=amount,
                payer_vpa=payer_vpa,
                provider=provider
            )
            
            # Convert to dict and handle datetime serialization
            payment_dict = unmatched.model_dump()
            for key, value in payment_dict.items():
                if isinstance(value, datetime):
                    payment_dict[key] = value.isoformat()
            
            result = await self.db.unmatched_payments.insert_one(payment_dict)
            
            logger.info(f"Stored unmatched payment: {transaction_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error storing unmatched payment: {str(e)}")
            raise
