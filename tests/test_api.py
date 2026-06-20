from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict():
    response = client.post("/predict", json={"text": "This pipeline works beautifully."})
    assert response.status_code == 200
    assert response.json()["label"] == "POSITIVE"

def test_predict_batch():
    response = client.post("/predict_batch", json={"texts": ["Great!", "Terrible!"]})
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.content

def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert "model_name" in response.json()