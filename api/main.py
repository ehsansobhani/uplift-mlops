
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from src.predict import predict_uplift


from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

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



REQUEST_COUNT = Counter("request_count", "Total API Requests")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency")

@app.middleware("http")
async def monitor_requests(request, call_next):
    start = time.time()
    REQUEST_COUNT.inc()

    response = await call_next(request)

    latency = time.time() - start
    REQUEST_LATENCY.observe(latency)

    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")