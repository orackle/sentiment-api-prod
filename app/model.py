from transformers import pipeline
import asyncio
from concurrent.futures import ThreadPoolExecutor

class SentimentPredictor:
    def __init__(self):
        # Cache model locally on first initialization
        self.pipe = pipeline("sentiment-analysis",
                             model="distilbert-base-uncased-finetuned-sst-2-english")
        self.executor = ThreadPoolExecutor(max_workers=2)
        from datetime import datetime
        self.loaded_at = datetime.now()

    async def predict(self, text: str) -> dict:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, self.pipe, text)
        return {"label": result[0]["label"], "score": float(result[0]["score"])}
