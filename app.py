from flask import Flask, request, jsonify
import cv2
import numpy as np
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['pt', 'en'])

@app.route('/')
def home():
    return 'API OCR funcionando. Use POST em /processar com imagem.'

@app.route('/processar', methods=['POST'])
def processar():
    if 'imagem' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem enviada'}), 400

    file = request.files['imagem']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    resultados = reader.readtext(img)
    textos = [text for (_, text, _) in resultados]

    return jsonify({'textos': textos})

# Para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
