import sys
sys.path.extend('..src/')

import json
import glob
from typing import Dict
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, Request

from src.model.predict import KeyStrokeInference
from src.model.classifier import get_model_results

# Our app instance
app = FastAPI()

# Some BaseModels to appear as fields to fill-in

# Class for aggregates
class Agg(BaseModel):
    Mean: float
    STD: float

# Class for feature and model types
class Item(BaseModel):
    Model: str 
    HT: Agg
    PPT: Agg
    RRT: Agg
    RPT: Agg


# GET and POST methods

@app.get("/")
async def api_info():
    return {"This is an API which recognizes keyboard users based "
            "on their keystrokes. Please check '/docs' tab for more information about the endpoints."}


@app.get("/api/models/{model}_{version}")
async def model_info(model: str, version: int) -> dict:
    res = get_model_results(model, version)
    return res

@app.post("/api/predict_file")
async def predict_file(file: UploadFile = File(...)):
    config = json.load(file.file)
    infer = KeyStrokeInference()
    pred_lbl = infer.get_inference_from_dict(config)
    return pred_lbl


@app.post("/api/predict_direct")
async def predict_direct(item: Item) -> dict:
    # Config JSON
    config = item.dict()
    print(config)
    print(type(config))
    # Inference
    infer = KeyStrokeInference()
    pred_lbl = infer.get_inference_from_dict(config)
    print(pred_lbl)

    return pred_lbl


if __name__ == '__main__':
    uvicorn.run(app=app, port=8051, host='127.1.0.0', workers=-1, reload=True)

