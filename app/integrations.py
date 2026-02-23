import json
import logging
import random
import os

logger = logging.getLogger(__name__)

# ====================== TIKTOK SHOP INTEGRATION ======================

def fetch_tiktok_order(order_id: str):
    """
    Simulates fetching order details from TikTok Shop API.
    In production, this would use 'requests' and API keys.
    """
    logger.info(f"Fetching TikTok order {order_id}...")
    
    # MOCKED DATA
    # Simulate a user buying a letter subscription
    return {
        "order_id": order_id,
        "customer": {
            "first_name": "Cassidy", # Use 'Cassidy' to match test case for now
            "email": "cassidy@example.com",
            "birth_date": "1991-02-17" # YYYY-MM-DD (From custom field on checkout)
        },
        "shipping_address": {
            "name": "Cassidy Williams",
            "address_line1": "123 Mystic Lane",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97204",
            "country": "US"
        },
        "items": [
            {"sku": "ANALOG-LETTER-SUB", "quantity": 1}
        ]
    }

# ====================== LOB INTEGRATION ======================

def send_letter_via_lob(pdf_path: str, address: dict):
    """
    Simulates sending a physical letter via Lob API.
    In production, this uploads the PDF and creates a letter resource.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
    logger.info(f"Uploading {pdf_path} to Lob...")
    
    # MOCKED API CALL
    lob_id = f"ltr_{random.randint(100000, 999999)}"
    
    logger.info(f"Letter sent via Lob! ID: {lob_id} to {address['name']}")
    
    return {
        "id": lob_id,
        "status": "processed",
        "expected_delivery_date": "2026-03-01"
    }
