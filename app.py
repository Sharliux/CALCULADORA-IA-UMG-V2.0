
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import math
from PIL import Image
from scipy.special import comb, perm
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)
CORS(app)

# Ruta del modelo cargado
MODEL_PATH = "modelo_mnist.keras"
modelo = load_model(MODEL_PATH)

def es_guion(w, h):
    return h < 12 and w > 15 and (w / h) > 3

def analizar_con_separador(imagen):
    img = cv2.imdecode(np.frombuffer(imagen.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img)
    _, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[0])

    grupo1, grupo2 = [], []
    separador_encontrado = False

    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        if es_guion(w, h) and not separador_encontrado:
            separador_encontrado = True
            continue
        if not separador_encontrado:
            grupo1.append(c)
        else:
            grupo2.append(c)

    def reconocer(grupo):
        digitos = []
        for c in sorted(grupo, key=lambda c: cv2.boundingRect(c)[0]):
            x, y, w, h = cv2.boundingRect(c)
            roi = thresh[y:y+h, x:x+w]
            roi = cv2.resize(roi, (18, 18))
            roi = cv2.copyMakeBorder(roi, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=0)
            roi = roi.astype("float32") / 255.0
            roi = np.expand_dims(roi, axis=-1)
            roi = np.expand_dims(roi, axis=0)
            pred = modelo.predict(roi, verbose=0)
            digito = np.argmax(pred)
            digitos.append(str(digito))
        return int("".join(digitos)) if digitos else None

    cantidad1 = reconocer(grupo1)
    cantidad2 = reconocer(grupo2)
    return cantidad1, cantidad2

def operar(a, b, op):
    try:
        if op == "suma":
            return f"{a} + {b} = {a + b}"
        elif op == "resta":
            return f"{a} - {b} = {a - b}"
        elif op == "mult":
            return f"{a} × {b} = {a * b}"
        elif op == "div":
            return "❌ División por cero." if b == 0 else f"{a} ÷ {b} = {a / b:.2f}"
        elif op == "comparacion":
            return f"{a} es mayor que {b}" if a > b else (f"{a} es menor que {b}" if a < b else f"{a} es igual a {b}")
        elif op == "max_min":
            return f"Máximo: {max(a,b)}, Mínimo: {min(a,b)}"
        elif op == "abs_diff":
            return f"Diferencia Absoluta: {abs(a-b)}"
        elif op == "promedio":
            return f"Promedio: {(a + b) / 2:.2f}"
        elif op == "rango":
            return f"Rango: {max(a,b) - min(a,b)}"
        elif op == "factorial":
            return f"{a}! = {math.factorial(a)}\n{b}! = {math.factorial(b)}"
        elif op == "combinaciones":
            return f"Combinaciones ({a},{b}): {comb(a,b,exact=True)}"
        elif op == "permutaciones":
            return f"Permutaciones ({a},{b}): {perm(a,b,exact=True)}"
        elif op == "mcd_mcm":
            mcd_ab = math.gcd(a, b)
            mcm_ab = abs(a * b) // mcd_ab if mcd_ab else 0
            return f"MCD({a}, {b}): {mcd_ab}\nMCM({a}, {b}): {mcm_ab}"
        elif op == "interpolacion":
            interpolado = a + (b - a) / 2
            return f"Interpolación lineal (mitad): {interpolado:.2f}"
        elif op == "media_armonica":
            if a == 0 or b == 0:
                return "❌ Media armónica no definida si algún número es cero."
            media = 2 * (a * b) / (a + b)
            return f"Media Armónica: {media:.2f}"
        elif op == "ratios":
            if a == 0 or b == 0:
                return "❌ División por cero."
            return f"Ratio A/B: {a / b:.2f}\nRatio B/A: {b / a:.2f}"
        else:
            return "Operación inválida."
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/procesar", methods=["POST"])
def procesar():
    if "imagen" not in request.files:
        return jsonify({"error": "No se proporcionó ninguna imagen."}), 400
    imagen = request.files["imagen"]
    a, b = analizar_con_separador(imagen)
    return jsonify({
    "numero1": int(a) if a is not None else None,
    "numero2": int(b) if b is not None else None
})



@app.route("/operar", methods=["POST"])
def operacion():
    data = request.json
    a = int(data["a"])
    b = int(data["b"])
    op = data["op"]
    resultado = operar(a, b, op)
    return jsonify({"resultado": resultado})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


