import os
import pickle
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load model and vectorizer using absolute paths based on this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

app = FastAPI(title="Email Classifier")

# Allow all origins for React/frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    confidence: float

class SuggestReplyRequest(BaseModel):
    label: str

class SuggestReplyResponse(BaseModel):
    suggested_reply: str


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    text = req.text or ""
    text_lower = text.lower()

    # Keyword-based override (high precision heuristics)
    urgent_keywords = ["urgent", "invoice", "payment", "due", "asap", "deadline", "escalation", "overdue"]
    spam_keywords = ["free", "offer", "discount", "click", "loan", "prize", "congratulations", "claim", "act now"]

    if any(word in text_lower for word in urgent_keywords):
        pred = "high_priority"
    elif any(word in text_lower for word in spam_keywords):
        pred = "spam"
    else:
        # ML fallback for ambiguous text
        try:
            X = vectorizer.transform([text])
            pred = model.predict(X)[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    prob = 1.0  # dummy confidence

    return {"label": str(pred), "confidence": float(prob)}


@app.post("/suggest_reply", response_model=SuggestReplyResponse)
async def suggest_reply(req: SuggestReplyRequest):
    """Generate a professional reply suggestion based on email classification."""
    label = req.label.lower()
    
    reply_templates = {
        "high_priority": "Thank you for bringing this to my attention. I will prioritize this and get back to you shortly.",
        "normal": "Thank you for your message. I appreciate you reaching out.",
        "spam": "This email does not appear relevant to me. Please remove me from your mailing list."
    }
    
    suggested_reply = reply_templates.get(label, "Thank you for your message.")
    
    return {"suggested_reply": suggested_reply}


@app.get("/health")
async def health() -> Dict[str, str]:
    status = "ok"
    details = {"model_path": model_path, "vectorizer_path": vectorizer_path}
    return {"status": status, "details": details}
