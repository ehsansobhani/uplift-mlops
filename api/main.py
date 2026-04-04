
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict_uplift

app = FastAPI()

# class Req(BaseModel):
#     feature1: float
#     feature2: float
#     feature3: float
class Req(BaseModel):
    client_id: str

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# @app.post("/predict")
# def p(r: Req):
#     return {"uplift": predict_uplift(r.client_id)}

@app.post("/predict")
def p(r: Req):
    logger.info(f"Request received: {r.client_id}")

    uplift = predict_uplift(r.client_id)

    logger.info(f"Prediction: {uplift}")

    return {"uplift": uplift}