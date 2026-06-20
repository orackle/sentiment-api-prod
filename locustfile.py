from locust import HttpUser, task, between

class SentimentUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def predict_single(self):
        self.client.post("/predict", json={"text": "I am thrilled with this upgrade!"})

    @task(1)
    def predict_batch(self):
        self.client.post("/predict_batch", json={
            "texts": ["Awesome!", "Terrible.", "Just average."]
        })

    @task(1)
    def health(self):
        self.client.get("/health")