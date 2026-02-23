# Analog Algorithm Engine Deployment

This repository contains the complete "Analog Algorithm" letter generation engine, wrapped in a FastAPI server ready for hosting.

## Components

1.  **Core Engine (`app/engine.py`):** Calculates the personalized letter based on Birth Card + Period Card + Planetary Lens.
2.  **PDF Generator (`app/pdf_generator.py`):** Creates print-ready PDFs using ReportLab.
3.  **Server (`app/server.py`):** FastAPI application that listens for webhooks.
4.  **Integrations (`app/integrations.py`):** Connects to TikTok Shop and Lob (currently mocked).

## Deployment Steps

### 1. Prerequisites

You need a Python hosting provider. Recommended: **Heroku** or **Render**.

### 2. Environment Variables

Create the following variables in your hosting dashboard:

*   `TIKTOK_APP_KEY`: Your TikTok App Key
*   `TIKTOK_APP_SECRET`: Your TikTok App Secret
*   `LOB_API_KEY`: Your Lob Live API Key

### 3. Deploy

**Heroku:**
1.  Install Heroku CLI.
2.  Login: `heroku login`
3.  Create app: `heroku create analog-algorithm-engine`
4.  Push: `git push heroku main`

**Render:**
1.  Connect your GitHub repo.
2.  Build Command: `pip install -r requirements.txt`
3.  Start Command: `uvicorn app.server:app --host 0.0.0.0 --port $PORT`

### 4. Configure Webhooks

**TikTok Shop:**
Point your TikTok Shop App webhook URL to:
`https://your-app-name.herokuapp.com/webhook/tiktok`

### 5. Verify

Send a test request to your deployed URL:
`POST /admin/generate-test`
Body:
```json
{
  "first_name": "Cassidy",
  "birth_date": "1991-02-17",
  "target_month": "2026-03"
}
```

## Customizing Logic

*   **Letter Content:** Edit `app/server.py` (lines 60-75) to customize the prose logic.
*   **PDF Layout:** Edit `app/pdf_generator.py` to change fonts/margins.
*   **Integrations:** Edit `app/integrations.py` to uncomment the real API calls.
