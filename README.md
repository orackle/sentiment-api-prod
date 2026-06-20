[![CI/CD Pipeline](https://github.com/orackle/sentiment-api-prod/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/orackle/sentiment-api-prod/actions/workflows/ci-cd.yml)

---

# 🎭 Sentiment Analysis Production API

A high-performance, asynchronous sentiment analysis production API built with **FastAPI**, **PyTorch (CPU)**, and **Hugging Face Transformers**. The service is fully compatible with **Python 3.14** and features multi-threaded inference offloading, request tracing, and Prometheus metrics monitoring.

---

## ✨ Features
- **Asynchronous Model Inference**: CPU-bound pipeline executions are offloaded to a thread pool executor, ensuring that the FastAPI event loop is never blocked.
- **Batch Processing**: Dedicated `/predict_batch` endpoint optimized for bulk text processing via Hugging Face pipelines.
- **Traceability**: `RequestIDMiddleware` generates and propagates trace IDs via `X-Request-ID` response headers.
- **Production Observability**: Integrated Prometheus metrics middleware tracking request rates, HTTP status codes, and latency distributions.
- **Python 3.14 Compatible**: Configured dependency resolver supporting modern Python versions on Windows environments.

---

## 🛠️ Tech Stack
- **Core**: Python 3.14, FastAPI, Uvicorn
- **ML Engine**: PyTorch (CPU), Transformers (DistilBERT fine-tuned model)
- **Monitoring**: Prometheus Client
- **Testing**: Pytest, Locust (Load Testing)

---

## 📂 Project Structure
```text
sentiment-api-prod/
├── app/
│   ├── config.py         # Configs (model name, version)
│   ├── main.py           # FastAPI application & middleware configuration
│   ├── metrics.py        # Prometheus monitoring middleware setup
│   ├── model.py          # Asynchronous Sentiment Predictor (PyTorch/Transformers wrapper)
│   └── requirements.txt  # Dependencies list compatible with Python 3.14
├── tests/
│   └── test_api.py       # API Endpoint Unit Tests
├── locustfile.py         # Locust performance load test scenario
└── README.md             # Project documentation
```

---

## 🚀 Setup & Installation

### 1. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r app/requirements.txt
```

---

## 🏃 Running the API Server

Start the production server using Uvicorn:
```powershell
uvicorn app.main:app --port 8000
```
The interactive Swagger API documentation will be available at `http://localhost:8000/docs`.

---

## 🔌 API Endpoints

### 1. Health Check
* **Method**: `GET`
* **Route**: `/health`
* **Response**: `{"status": "ok"}`

### 2. Single Sentiment Prediction
* **Method**: `POST`
* **Route**: `/predict`
* **Body**:
  ```json
  {
    "text": "The performance of the API is extremely fast!"
  }
  ```
* **Response**:
  ```json
  {
    "text": "The performance of the API is extremely fast!",
    "label": "POSITIVE",
    "score": 0.9998,
    "latency_ms": 42.1
  }
  ```

### 3. Batch Predictions
* **Method**: `POST`
* **Route**: `/predict_batch`
* **Body**:
  ```json
  {
    "texts": ["This is great!", "Terrible experience."]
  }
  ```
* **Response**:
  ```json
  {
    "results": [
      { "text": "This is great!", "label": "POSITIVE", "score": 0.9998 },
      { "text": "Terrible experience.", "label": "NEGATIVE", "score": 0.9995 }
    ],
    "count": 2,
    "latency_ms": 85.5
  }
  ```

### 4. Metrics (Prometheus Export)
* **Method**: `GET`
* **Route**: `/metrics`
* **Response**: Plain text with format compatible with Prometheus scrapers.

### 5. Model Information
* **Method**: `GET`
* **Route**: `/model-info`

---

## 🧪 Testing

### Running Unit Tests
Always run with the module flag (`python -m`) to ensure local module paths resolve correctly:
```powershell
python -m pytest tests/
```

### Running Performance Load Tests
Execute Locust to benchmark the endpoints under load:
```powershell
locust -f locustfile.py
```
This starts the Locust web interface at `http://localhost:8089`.

---

## 📊 Performance & Load Testing Results

Locust Tests:
<img width="1877" height="631" alt="image" src="https://github.com/user-attachments/assets/8a8f201e-24ff-41b9-be8c-4b44f94cbc70" />

<img width="1875" height="450" alt="image" src="https://github.com/user-attachments/assets/7155e119-54e5-41b0-9933-5c880256466f" />

<img width="1833" height="457" alt="image" src="https://github.com/user-attachments/assets/8ccd2c7d-956a-493c-9303-ae5be4b6be24" />

