
from locust import HttpUser, task, between


class AnalyticsPlatformUser(HttpUser):
    # Wait 1–3 seconds between requests
    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        self.client.get("/api/v1/health", name="Health Check")

    @task(2)
    def list_records(self):
        self.client.get("/api/v1/records", name="List Records")

    @task(2)
    def analytics_summary(self):
        self.client.get(
            "/api/v1/analytics/summary",
            name="Analytics Summary",
        )

    @task(1)
    def category_analytics(self):
        self.client.get(
            "/api/v1/analytics/categories",
            name="Category Analytics",
        )

    @task(1)
    def top_products(self):
        self.client.get(
            "/api/v1/analytics/top-products",
            name="Top Products",
        )
