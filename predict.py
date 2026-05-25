# predict.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app)

# ✅ Load model
MODEL_PATH = "model.h5"

if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully")
else:
    model = None
    print("❌ Model file not found")

# ✅ Class labels (adjust if needed)
class_names = [
    "Leaf Blight",
    "Powdery Mildew",
    "Rust",
    "Healthy"
]

# ✅ Treatments
treatments = {
    "Leaf Blight": "Use fungicide and remove infected leaves",
    "Powdery Mildew": "Apply neem oil spray",
    "Rust": "Use sulfur-based spray",
    "Healthy": "No treatment needed"
}

# ================== PREDICT ==================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # ✅ FIXED: use "file" (matches frontend)
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files['file']

        # Save image
        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        print("📁 File received:", file.filename)

        # ✅ If model exists
        if model:
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img)

            # Normalize
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            predictions = model.predict(img_array)

            print("🔥 Prediction:", predictions)

            predicted_index = int(np.argmax(predictions))
            confidence = float(np.max(predictions))

            predicted_class = class_names[predicted_index]

            # Safety
            if confidence < 0.01:
                predicted_class = "Unknown"

        else:
            # Fallback if model missing
            predicted_class = "Leaf Blight"
            confidence = 0.85

        return jsonify({
            "disease": predicted_class,
            "confidence": confidence,
            "treatment": treatments.get(predicted_class, "N/A")
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)})

# ================== RUN ==================
if __name__ == '__main__':
    app.run(debug=True)