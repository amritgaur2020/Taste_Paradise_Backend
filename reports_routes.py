from fastapi import APIRouter
from datetime import datetime
import sqlite3

router = APIRouter()

# Database connection (adjust path if needed)
DB_PATH = "restaurant.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/api/reports/daily/{date}")
async def get_daily_report(date: str):
    """
    Get daily report for a specific date
    Format: YYYY-MM-DD (e.g., 2025-10-16)
    """
    try:
        # Parse the date
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all orders for that date
        orders_query = """
            SELECT 
                order_id,
                table_number,
                items,
                total_amount,
                status,
                payment_method,
                payment_status,
                created_at
            FROM `Order` 
            WHERE DATE(created_at) = ?
            ORDER BY created_at DESC
        """
        
        cursor.execute(orders_query, (date,))
        orders = cursor.fetchall()
        
        # Convert to list of dicts
        orders_list = []
        for order in orders:
            orders_list.append({
                "order_id": order["order_id"],
                "table_number": order["table_number"],
                "items": order["items"],
                "total_amount": order["total_amount"],
                "status": order["status"],
                "payment_method": order["payment_method"],
                "payment_status": order["payment_status"],
                "created_at": order["created_at"]
            })
        
        # Calculate totals
        online_total = sum(
            order['total_amount'] 
            for order in orders_list 
            if order['payment_method'] == 'online' and order['status'] == 'paid'
        )
        
        cash_total = sum(
            order['total_amount'] 
            for order in orders_list 
            if order['payment_method'] == 'cash' and order['status'] == 'paid'
        )
        
        conn.close()
        
        return {
            "success": True,
            "date": date,
            "orders": orders_list,
            "revenue": online_total + cash_total,
            "online_total": online_total,
            "cash_total": cash_total,
            "grand_total": online_total + cash_total,
            "total_orders": len(orders_list)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "orders": []
        }
