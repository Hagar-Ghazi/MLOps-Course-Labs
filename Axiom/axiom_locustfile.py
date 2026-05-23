from locust import HttpUser, task, between
import random


# ==============================================================
# Regular customers - LOW churn risk
# ==============================================================
class RegularUser(HttpUser):
    wait_time = between(1, 3)
    weight = 3

    @task(3)
    def predict_average_customer(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": random.uniform(580, 700),
                "Age": random.uniform(30, 45),
                "Tenure": random.uniform(3, 7),
                "Balance": random.uniform(40000, 80000),
                "NumOfProducts": 2.0,
                "HasCrCard": 1.0,
                "IsActiveMember": 1.0,
                "EstimatedSalary": random.uniform(60000, 100000),
                "Geography_Germany": 0.0,
                "Geography_Spain": 0.0,
                "Gender_Male": random.choice([0.0, 1.0]),
            },
        )

    @task(1)
    def predict_low_risk(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": random.uniform(750, 850),
                "Age": random.uniform(25, 35),
                "Tenure": random.uniform(5, 10),
                "Balance": random.uniform(10000, 30000),
                "NumOfProducts": 1.0,
                "HasCrCard": 1.0,
                "IsActiveMember": 1.0,
                "EstimatedSalary": random.uniform(50000, 70000),
                "Geography_Germany": 0.0,
                "Geography_Spain": 1.0,
                "Gender_Male": 1.0,
            },
        )

    @task(1)
    def check_health(self):
        self.client.get("/health")

    @task(1)
    def check_home(self):
        self.client.get("/")


# ==============================================================
# High risk customers - HIGH churn risk → triggers Monitor 1
# ==============================================================
class HighRiskUser(HttpUser):
    wait_time = between(0.5, 1.5)
    weight = 2

    @task(2)
    def predict_high_churn_risk(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": random.uniform(400, 550),
                "Age": random.uniform(50, 65),
                "Tenure": random.uniform(0, 3),
                "Balance": random.uniform(100000, 200000),
                "NumOfProducts": random.choice([1.0, 4.0]),
                "HasCrCard": 0.0,
                "IsActiveMember": 0.0,
                "EstimatedSalary": random.uniform(20000, 50000),
                "Geography_Germany": 1.0,
                "Geography_Spain": 0.0,
                "Gender_Male": 0.0,
            },
        )

    @task(1)
    def predict_inactive_member(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": random.uniform(500, 600),
                "Age": random.uniform(45, 60),
                "Tenure": random.uniform(1, 4),
                "Balance": random.uniform(80000, 150000),
                "NumOfProducts": 1.0,
                "HasCrCard": 1.0,
                "IsActiveMember": 0.0,
                "EstimatedSalary": random.uniform(30000, 60000),
                "Geography_Germany": 0.0,
                "Geography_Spain": 0.0,
                "Gender_Male": random.choice([0.0, 1.0]),
            },
        )


# ==============================================================
# Heavy burst users → triggers Monitor 2 (High Latency)
# ==============================================================
class HeavyUser(HttpUser):
    wait_time = between(0.1, 0.5)
    weight = 1

    @task
    def stress_test_burst(self):
        self.client.post(
            "/predict",
            json={
                "CreditScore": random.uniform(300, 900),
                "Age": random.uniform(18, 70),
                "Tenure": random.uniform(0, 10),
                "Balance": random.uniform(0, 250000),
                "NumOfProducts": random.choice([1.0, 2.0, 3.0, 4.0]),
                "HasCrCard": random.choice([0.0, 1.0]),
                "IsActiveMember": random.choice([0.0, 1.0]),
                "EstimatedSalary": random.uniform(10000, 200000),
                "Geography_Germany": random.choice([0.0, 1.0]),
                "Geography_Spain": random.choice([0.0, 1.0]),
                "Gender_Male": random.choice([0.0, 1.0]),
            },
        )


# ==============================================================
# Bad requests → triggers Monitor 3 (Error Rate)
# ==============================================================
class BadRequestUser(HttpUser):
    wait_time = between(2, 5)
    weight = 1

    @task(1)
    def send_invalid_request(self):
        # Missing fields → causes 400 error
        self.client.post(
            "/predict",
            json={
                "CreditScore": "invalid_string",
                "Age": None,
            },
            name="/predict [BAD REQUEST]",
        )

    @task(1)
    def send_empty_request(self):
        self.client.post("/predict", json={}, name="/predict [EMPTY]")

    @task(1)
    def send_extreme_values(self):
        # Extreme values that may cause issues
        self.client.post(
            "/predict",
            json={
                "CreditScore": -999,
                "Age": 999,
                "Tenure": -1,
                "Balance": -99999,
                "NumOfProducts": 100,
                "HasCrCard": 5,
                "IsActiveMember": 5,
                "EstimatedSalary": -1,
                "Geography_Germany": 2,
                "Geography_Spain": 2,
                "Gender_Male": 5,
            },
            name="/predict [EXTREME VALUES]",
        )
