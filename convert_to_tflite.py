import tensorflow as tf

model = tf.keras.models.load_model("handwritten.keras")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("handwritten.tflite", "wb") as f:
    f.write(tflite_model)

print("handwritten.tflite written.")