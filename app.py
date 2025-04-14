from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from utils.model_utils import load_trained_model, predict_disease, preprocess_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model, class_names = load_trained_model('models/plant_disease_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        img_array = preprocess_image(filepath)
        predicted_class, confidence, solution = predict_disease(model, img_array, class_names)

        plant, disease = predicted_class.split("__") if "__" in predicted_class else (predicted_class, "Unknown")

        return jsonify({
            'plant': plant,
            'disease': disease,
            'solution': solution,
            'confidence': float(confidence),
            'processed': f"/uploads/{file.filename}"
        })
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)


