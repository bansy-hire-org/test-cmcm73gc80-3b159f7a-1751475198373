from locust import HttpUser, task, between

class FeatureFlagUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def get_all_features(self):
        self.client.get("/features")

    @task
    def get_specific_feature(self):
        self.client.get("/features/sample_feature")
