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
    
@app.post("/predict")
def p(r: Req):
    return {"uplift": predict_uplift(r.client_id)}