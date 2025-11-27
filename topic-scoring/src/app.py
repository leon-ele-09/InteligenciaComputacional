from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_path = os.path.join(current_dir, 'modules')
sys.path.append(utils_path)

import backend

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
    resultado = backend.Backend.predict_sentiment(data.text)
    print(f"Sentiment scores: {resultado['sentiment_scores']}")
    print(f"Topic scores: {resultado['topic_scores']}")
    
    return {
        "input": data.text,
        "sentiment_scores": resultado['sentiment_scores'],
        "topic_scores": resultado['topic_scores'],
        "timestamp": time.time()
    }