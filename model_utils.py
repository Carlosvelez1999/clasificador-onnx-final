import os
import json
import requests
import numpy as np
import onnxruntime as ort
from PIL import Image

# URL pública del modelo ONNX
MODEL_URL = "https://github.com/onnx/models/raw/main/Computer_Vision/mobilenetv2_050_Opset18_timm/mobilenetv2_050_Opset18.onnx"
MODEL_PATH = "mobilenetv2.onnx"

# URL del archivo de etiquetas
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
LABELS_PATH = "imagenet_labels.json"

# Softmax para normalizar la salida del modelo
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# Preprocesamiento
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224)).convert("RGB")
    img = np.array(img).astype(np.float32)
    img = img.transpose(2, 0, 1) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Descargar modelo y etiquetas si no existen
def download_model():
    if not os.path.exists(MODEL_PATH):
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

def download_labels():
    if not os.path.exists(LABELS_PATH):
        r = requests.get(LABELS_URL)
        with open(LABELS_PATH, "wb") as f:
            f.write(r.content)

# Cargar todo al inicio
download_model()
download_labels()

session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
with open(LABELS_PATH, "r") as f:
    LABELS = json.load(f)

# Predicción
def predict(image_path):
    img = preprocess_image(image_path)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img})[0]
    probabilities = softmax(outputs[0])
    pred_class = int(np.argmax(probabilities))
    confidence = float(np.max(probabilities))
    return pred_class, confidence

def get_label(index):
    return LABELS[index]
