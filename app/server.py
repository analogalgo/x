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

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ====================== DATA MODELS ======================

class LetterRequest(BaseModel):
    first_name: str
    birth_date: str # YYYY-MM-DD
    target_month: str # YYYY-MM

# ====================== ENDPOINTS ======================

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serves the Writer's Dashboard."""
    template_path = os.path.join(BASE_DIR, "templates", "dashboard.html")
    logger.info(f"Serving dashboard from: {template_path}")
    
    if not os.path.exists(template_path):
        logger.error(f"Template not found: {template_path}")
        return HTMLResponse(content="<h1>Writer's Dashboard Template Not Found</h1>", status_code=404)
        
    with open(template_path, "r") as f:
        return HTMLResponse(content=f.read())

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
            
        # Simplified content logic for manual generation
        content = f"""
Personalized Analysis for {req.first_name}
Target: {req.target_month}

Your Birth Card is the {data['birth_card']}.
In this {data['period']['planet']} period, your primary card is the {data['period']['card']}.

This cycle emphasizes material stability and the pursuit of your higher purpose.
Your Long Range card ({data['year_long']['long_range']}) suggests a theme of transition.
        """
        
        filename = f"manual_{req.first_name}_{req.target_month}.pdf"
        pdf_path = os.path.join(os.getcwd(), filename)
        pdf_generator.build_pdf(pdf_path, req.target_month, req.first_name, content)
        
        # Default shipping address
        shipping_address = {
            "name": req.first_name,
            "address_line1": "123 Mystic Lane",
            "city": "Portland",
            "state": "OR",
            "zip_code": "97204"
        }
        
        # Attempt to mail via Lob
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
    return {"status": "success", "mode": "manual_active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
