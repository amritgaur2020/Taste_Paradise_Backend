from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class PaymentNotification(BaseModel):
    """Incoming payment notification from soundbox"""
    transaction_id: str
    amount: float
    upi_id: str  # Sender's UPI ID
    timestamp: str
    payment_method: Literal["upi", "card", "cash"]
    status: Literal["success", "pending", "failed"]
    merchant_transaction_id: Optional[str] = None
    remarks: Optional[str] = None

class PaymentRecord(BaseModel):
    """Payment record stored in database"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: Optional[str] = None  # Matched order
    transaction_id: str
    amount: float
    upi_id: str
    payment_method: str
    status: str
    timestamp: datetime
    matched: bool = False
    matched_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
