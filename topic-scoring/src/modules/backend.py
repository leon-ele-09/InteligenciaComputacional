import tensorflow as tf
import numpy as np
import pickle
from tensorflow import keras

model = keras.models.load_model('model_no_vector.keras')
with open("vocab.pkl", "rb") as f:
    vocab = pickle.load(f)

vectorize_layer = tf.keras.layers.TextVectorization(
    output_mode='int',
    output_sequence_length=100,
    vocabulary=vocab
)
print("Modelo cargado")


class Backend:
    @staticmethod
    def predict_sentiment(text: str):
        """Analiza el sentimiento del texto"""
        texto_tensor = tf.convert_to_tensor([text])
        entrada = vectorize_layer(texto_tensor)
        # Obtener predicción
        pred = model.predict(entrada, verbose=0)[0]
        
        return pred.tolist()
    
    
