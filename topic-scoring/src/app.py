from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
from modules.backend import Backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str

@app.post("/ai")
def analizar_sentimiento(data: InputData):
    resultado = Backend.predict_sentiment(data.text) 
    return {
        "input": data.text,
        "resultado": resultado,
        "timestamp": time.time()
    }
