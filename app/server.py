from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
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

# ====================== ENDPOINTS ======================

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serves the Writer's Dashboard."""
    # Look for templates folder relative to this file
    path = os.path.join(os.path.dirname(__file__), "..", "templates", "index.html")
    if not os.path.exists(path):
        return "<h1>Template not found</h1>"
    with open(path, "r") as f:
        return f.read()

@app.post("/admin/generate-test")
async def generate_test_letter(req: LetterRequest):
    """
    Manually triggers a letter generation and mails it via Lob.
    """
    try:
        b_year, b_month, b_day = map(int, req.birth_date.split("-"))
        target_date = f"{req.target_month}-15"
        
        data = engine.calculate_letter_data(
            req.first_name, b_year, b_month, b_day, target_date
        )
        
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
            
        # Expanded content for dashboard testing
        content = f"""
Your Analog Algorithm Reading for {req.target_month}

Birth Card: {data['birth_card']}
Period Card: {data['period']['card']} ({data['period']['planet']})
Long Range: {data['year_long']['long_range']}

This month, the {data['period']['planet']} influence brings the {data['period']['card']} to the forefront of your experience. 
As an {data['birth_card']}, you will find that your natural Material and Commander traits are 
augmented by the seeker energy of your period card. 

The Long Range focus on the {data['year_long']['long_range']} suggests this is a time for 
foundational shifts that will echo for the next 52 days.
        """
        
        filename = f"manual_{req.first_name}_{req.target_month}.pdf"
        pdf_path = os.path.join(os.getcwd(), filename)
        pdf_generator.build_pdf(pdf_path, req.target_month, req.first_name, content)
        
        # Default shipping address for manual dashboard
        shipping_address = {
            "name": req.first_name,
            "address_line1": "123 Mystic Lane",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97204"
        }
        
        # Mail it via Lob (using the key we set earlier)
        lob_response = integrations.send_letter_via_lob(pdf_path, shipping_address)
        
        return {
            "message": "Letter Generated and Mailed",
            "lob_id": lob_response.get("id"),
            "engine_data": data
        }
        
    except Exception as e:
        logger.error(f"Manual Gen Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/tiktok")
async def tiktok_webhook(request: Request):
    """Legacy endpoint for TikTok integration."""
    return {"status": "success", "message": "Manual mode active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
