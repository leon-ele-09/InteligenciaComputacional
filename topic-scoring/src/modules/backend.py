import tensorflow as tf
import numpy as np
import pickle
from tensorflow import keras

@tf.keras.utils.register_keras_serializable()
class SimpleSelfAttention(tf.keras.layers.Layer):
    def __init__(self, hidden_dim, **kwargs):
        super().__init__(**kwargs)
        self.hidden_dim = hidden_dim
        # We define the layers here, but they are NOT built yet
        self.query_dense = tf.keras.layers.Dense(hidden_dim)
        self.key_dense = tf.keras.layers.Dense(hidden_dim)
        self.value_dense = tf.keras.layers.Dense(hidden_dim)
        self.scale = tf.sqrt(tf.cast(hidden_dim, tf.float32))

    # --- ADD THIS METHOD ---
    def build(self, input_shape):
        # We must manually tell the sub-layers to build using the input shape
        self.query_dense.build(input_shape)
        self.key_dense.build(input_shape)
        self.value_dense.build(input_shape)
        super().build(input_shape)

    def call(self, inputs):
        Q = self.query_dense(inputs)
        K = self.key_dense(inputs)
        V = self.value_dense(inputs)

        scores = tf.matmul(Q, K, transpose_b=True) / self.scale
        weights = tf.nn.softmax(scores, axis=-1)

        return tf.matmul(weights, V)

    def get_config(self):
        config = super().get_config()
        config.update({
            "hidden_dim": self.hidden_dim,
        })
        return config

# Load models
model_sentiment = keras.models.load_model(
    'modules/model1.keras',
    custom_objects={'SimpleSelfAttention': SimpleSelfAttention}
)
model_topic = keras.models.load_model('modules/model_topic.keras')

# ... rest of your code ...

with open("vocab_topic.pkl", "rb") as f:
    vocab = pickle.load(f)

with open("vocab_bilstm_att.pkl", "rb") as f:
    vocab_sent = pickle.load(f)

vectorize_layer = tf.keras.layers.TextVectorization(
    output_mode='int',
    output_sequence_length=100,
    vocabulary=vocab
)

vectorize_layer_sent = tf.keras.layers.TextVectorization(
    output_mode='int',
    output_sequence_length=100,
    vocabulary=vocab_sent
)


print("Modelos cargados")


class Backend:
    @staticmethod
    def predict_sentiment(text: str):
        """Analiza el sentimiento y el topic del texto"""
        texto_tensor = tf.convert_to_tensor([text])
        entrada = vectorize_layer(texto_tensor)
        
        # Obtener predicción de topic (19 labels)
        pred_topic = model_topic.predict(entrada, verbose=0)[0]
        
        
        entrada = vectorize_layer_sent(texto_tensor)
        # Obtener predicción de sentimiento (6 labels)
        pred_sentiment = model_sentiment.predict(entrada, verbose=0)[0]
        
        
        
        return {
            'sentiment_scores': pred_sentiment.tolist(),
            'topic_scores': pred_topic.tolist()
        }