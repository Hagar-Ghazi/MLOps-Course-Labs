"""
Tests for the Churn Prediction API.
Run with:
    pytest tests/ -v
    pytest tests/ -v --cov = app --cov=main --cov-report=term-missing
"""

from litestar.testing import TestClient
from app.model_utils import predict_churn
from main import app


SAMPLE = [600.0, 35.0, 5.0, 50000.0, 2.0, 1.0, 1.0, 80000.0, 0.0, 0.0, 1.0]

VALID_JSON = {
    "CreditScore": 600.0,
    "Age": 35.0,
    "Tenure": 5.0,
    "Balance": 50000.0,
    "NumOfProducts": 2.0,
    "HasCrCard": 1.0,
    "IsActiveMember": 1.0,
    "EstimatedSalary": 80000.0,
    "Geography_Germany": 0.0,
    "Geography_Spain": 0.0,
    "Gender_Male": 1.0,
}

# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------


# Function test for predict_churn
def test_predict_churn_returns_0_or_1():
    result = predict_churn(SAMPLE)
    assert result in (0, 1)


# (bonus): Edge case function test
def test_predict_churn_all_zeros():
    result = predict_churn([0.0] * 11)
    assert result in (0, 1)


def test_predict_churn_high_risk():
    result = predict_churn(
        [300.0, 60.0, 1.0, 0.0, 1.0, 0.0, 0.0, 10000.0, 1.0, 0.0, 0.0]
    )
    assert result in (0, 1)


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------


# POST /predict
def test_predict_endpoint():
    with TestClient(app=app) as client:
        response = client.post("/predict", json=VALID_JSON)
    assert response.status_code == 201
    assert "churn" in response.json()


# GET /health
def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# GET /
def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# (bonus): Invalid input returns 400
def test_invalid_input_returns_400():
    with TestClient(app=app) as client:
        response = client.post("/predict", json={"CreditScore": "not_a_number"})
    assert response.status_code == 400
