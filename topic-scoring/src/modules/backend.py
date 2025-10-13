import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("src/modules/sentiment_model.keras")
print("Modelo cargado")


class Backend:
    @staticmethod
    def predict_sentiment(text: str):
        """Analiza el sentimiento del texto"""
        texto_tensor = tf.constant([text])
        pred = model.predict(texto_tensor, verbose=0)
        score = tf.sigmoid(pred[0][0]).numpy()
        sentimiento = "positivo" if score > 0.5 else "negativo"
        confianza = round(float(score if score > 0.5 else 1 - score), 3)

        return {
            "sentimiento": sentimiento,
            "confianza": confianza
        }
