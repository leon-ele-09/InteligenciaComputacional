from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import time

class backend:
    @staticmethod
    def GenerateNumbers():
        # CONVERTIR A LISTA PARA MANEJAR EN JSON
        return np.random.randint(0,100,5).tolist()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str

@app.post("/ai")
def home(data: InputData):
    return {
        "input": data.text,
        "scores": backend.GenerateNumbers(),  # ✅ CHANGED HERE
        "timestamp": time.time()
    }
