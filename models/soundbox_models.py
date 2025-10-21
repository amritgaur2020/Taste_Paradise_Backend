# models/soundbox_models.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from enum import Enum
import uuid

class SoundboxProvider(str, Enum):
    PAYTM = "paytm"
    PHONEPE = "phonepe"
    GPAY = "gpay"
    OTHER = "other"

class SoundboxConfigModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: SoundboxProvider = SoundboxProvider.PAYTM
    merchant_upi_id: str
    merchant_name: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    webhook_url: Optional[str] = None
    is_active: bool = True
    last_ping: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SoundboxConfigCreate(BaseModel):
    provider: SoundboxProvider
    merchant_upi_id: str
    merchant_name: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None

class SoundboxConfigUpdate(BaseModel):
    provider: Optional[SoundboxProvider] = None
    merchant_upi_id: Optional[str] = None
    merchant_name: Optional[str] = None
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    is_active: Optional[bool] = None

class SoundboxWebhookPayload(BaseModel):
    transaction_id: str
    amount: float
    payer_vpa: Optional[str] = None
    timestamp: Optional[str] = None
    status: str = "success"
    provider: str = "paytm"
    merchant_id: Optional[str] = None

class UnmatchedPaymentModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    transaction_id: str
    amount: float
    payer_vpa: Optional[str] = None
    provider: str = "soundbox"
    status: str = "unmatched"  # unmatched, matched, refunded, misc_income
    resolution: Optional[str] = None
    matched_order_id: Optional[str] = None
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaymentMatchingSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    matching_algorithm: str = "fifo"  # fifo, amount_time, manual
    payment_timeout_minutes: int = 15
    auto_mark_paid: bool = True
    send_kot_after_payment: bool = True
    play_notification_sound: bool = True
    auto_print_bill: bool = True
    show_unmatched_popup: bool = True
    email_daily_summary: bool = False
    email_address: Optional[str] = None
    sms_unmatched_alert: bool = False
    phone_number: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
