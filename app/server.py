from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import datetime
import logging
import os
from . import engine, integrations, pdf_generator

app = FastAPI(title="Analog Algorithm Engine", version="1.0.0")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== DATA MODELS ======================

class LetterRequest(BaseModel):
    first_name: str
    birth_date: str # YYYY-MM-DD
    target_month: str # YYYY-MM

class TestWebhook(BaseModel):
    order_id: str

# ====================== ENDPOINTS ======================

@app.post("/webhook/tiktok")
async def tiktok_webhook(request: Request):
    """
    Receives order updates from TikTok Shop.
    Assuming the payload contains 'order_id' or similar structure.
    """
    try:
        data = await request.json()
        logger.info(f"Received TikTok webhook: {data}")
        
        # Determine if this is a 'Paid' order
        status = data.get("status", "PAID")
        order_id = data.get("data", {}).get("order_id", "TEST_ORDER")
        
        if status == "PAID":
            # Fetch full details (mocked)
            order = integrations.fetch_tiktok_order(order_id)
            
            # Extract customer info
            customer = order["customer"]
            bd = customer["birth_date"] # "1991-02-17"
            target_date = datetime.date.today().strftime("%Y-%m-%d") # Default to today or next month
            
            # Generate Letter Data
            # Note: birth_date parsing logic
            try:
                b_year, b_month, b_day = map(int, bd.split("-"))
            except ValueError:
                logger.error(f"Invalid birth date format: {bd}")
                return {"status": "failed", "reason": "Invalid birth date"}

            letter_data = engine.calculate_letter_data(
                customer["first_name"], b_year, b_month, b_day, target_date
            )
            
            if "error" in letter_data:
                logger.error(f"Engine Error: {letter_data['error']}")
                return {"status": "failed", "reason": letter_data['error']}
                
            # Generate PDF
            # Simple content logic for now (mocked prose generation)
            # In a real app, this would use a complex LLM or template engine
            content = f"""
This is your personalized letter for {letter_data['period']['planet']} period.

Birth Card: {letter_data['birth_card']}
Period Card: {letter_data['period']['card']}
Long Range: {letter_data['year_long']['long_range']}
Pluto: {letter_data['year_long']['pluto']}
Result: {letter_data['year_long']['result']}

(This content is a placeholder. The real system would generate 400 words based on these cards.)
            """
            
            filename = f"letter_{order_id}.pdf"
            pdf_path = os.path.join(os.getcwd(), filename)
            pdf_generator.build_pdf(pdf_path, target_date[:7], customer["first_name"], content)
            
            # Send via Lob
            lob_response = integrations.send_letter_via_lob(pdf_path, order["shipping_address"])
            
            return {
                "status": "success", 
                "lob_id": lob_response["id"],
                "data": letter_data
            }
            
        return {"status": "ignored", "reason": "Not a paid order"}
        
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/generate-test")
async def generate_test_letter(req: LetterRequest):
    """
    Manually triggers a letter generation for testing.
    """
    try:
        b_year, b_month, b_day = map(int, req.birth_date.split("-"))
        target_date = f"{req.target_month}-15"
        
        data = engine.calculate_letter_data(
            req.first_name, b_year, b_month, b_day, target_date
        )
        
        # Simple content for test
        content = f"""
Birth Card: {data['birth_card']}
Period Card: {data['period']['card']} ({data['period']['planet']})
Long Range: {data['year_long']['long_range']}

This is a test of the Analog Algorithm Engine.
        """
        
        filename = f"test_{req.first_name}_{req.target_month}.pdf"
        pdf_path = os.path.join(os.getcwd(), filename)
        pdf_generator.build_pdf(pdf_path, req.target_month, req.first_name, content)
        
        return {
            "message": "PDF Generated",
            "path": pdf_path,
            "engine_data": data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
