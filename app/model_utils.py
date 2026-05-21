"""
Model loading and prediction logic
The model must be loaded ONCE at module level NOT inside the predict function
"""

import joblib
import numpy as np

# Load your serialized churn model from data/model.joblib
model = joblib.load("data/model.joblib")


def predict_churn(features: list[float]) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1
    """
    # Use model.predict() to get a prediction and return it as an int
    # Hint: model.predict() expects a 2D array
    prediction = model.predict(np.array([features]))
    return int(prediction[0])


if __name__ == "__main__":
    # Replace with sample features that match your model
    sample = [600.0, 35.0, 5.0, 50000.0, 2.0, 1.0, 1.0, 80000.0, 0.0, 0.0, 1.0]
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
