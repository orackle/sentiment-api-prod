from fastapi import FastAPI, Response
from pydantic import BaseModel
from app.model import SentimentPredictor
import time
from typing import List
import uuid
import torch
import transformers
from app import config
from app.metrics import metrics_middleware
from prometheus_client import generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="Sentiment API", version="1.0.0")
predictor = SentimentPredictor()

app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_middleware)

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestIDMiddleware)


class TextInput(BaseModel):
    """Input model for text sentiment analysis"""
    text: str

class BatchInput(BaseModel):
    texts: List[str]

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/predict")
async def predict(input:TextInput):
    start = time.time()
    result = await predictor.predict(input.text)
    end = time.time()

    return {
        "text":input.text,
        **result,
        "latency_ms":(end-start)*1000
    }

@app.post("/predict_batch")
def predict_batch(input: BatchInput):
    start = time.time()
    # Pipeline can handle a list directly, much faster than looping
    results = predictor.pipe(input.texts)
    latency_ms = (time.time() - start) * 1000
    return {
        "results": [
            {"text": text, "label": res["label"], "score": float(res["score"])}
            for text, res in zip(input.texts, results)
        ],
        "count": len(input.texts),
        "latency_ms": latency_ms
    }


@app.get("/model-info")
def model_info():
    return {
        "model_name": config.MODEL_NAME,
        "model_version": config.MODEL_VERSION,
        "pytorch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "loaded_at": predictor.loaded_at.isoformat()
    }

@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type="text/plain")