"""
Churn Prediction API
Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar, get, post
from pydantic import BaseModel
from app.logger_setup import setup_logging
from app.model_utils import predict_churn

logger = setup_logging()


# Add one field (type float) per feature your model expects
class ChurnRequest(BaseModel):
    CreditScore: float
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float
    Geography_Germany: float
    Geography_Spain: float
    Gender_Male: float


# Endpoints


# GET /
@get("/")
async def home() -> dict:
    logger.info("Home endpoint was accessed")
    return {"message": "Churn Prediction API", "version": "1.0.0"}


# GET /health
@get("/health")
async def health() -> dict:
    logger.info("Health endpoint was accessed")
    return {"status": "healthy"}


# POST /predict
@post("/predict")
async def predict(data: ChurnRequest) -> dict:
    features = [
        data.CreditScore,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
        data.Geography_Germany,
        data.Geography_Spain,
        data.Gender_Male,
    ]
    logger.info("Input features: %s", features)
    result = predict_churn(features)
    logger.info("Prediction result: %s", result)
    return {"churn": result}


# App(Register endpoint functions)
app = Litestar(
    route_handlers=[home, health, predict],
)
