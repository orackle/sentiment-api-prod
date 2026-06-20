import os

MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")