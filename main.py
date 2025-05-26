from flask import Flask, render_template, request
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
from model_utils import predict, get_label
from sheets_utils import registrar_prediccion

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Carpeta para subir imágenes
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    label = None
    confidence = None
    image_filename = None

    if request.method == "POST":
        # 1. Guardar imagen
        file = request.files["image"]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"{timestamp}_{file.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        file.save(image_path)

        # 2. Ejecutar predicción
        pred_class, confidence = predict(image_path)
        label = get_label(pred_class)
        print("✅ Resultado de la predicción:", label, confidence)

        # 3. Registrar en Google Sheets
        registrar_prediccion(image_filename, label, confidence)

    return render_template(
        "index.html",
        label=label,
        confidence=confidence,
        image_filename=image_filename
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
