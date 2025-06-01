# app.py
from flask import Flask, request, render_template
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open("model/model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    try:
        values = [float(x) for x in request.form.values()]
        final = [np.array(values)]
        prediction = model.predict(final)
        return render_template("index.html", prediction_text=f"🌾 Recommended Crop: {prediction[0]}")
    except Exception as e:
        return render_template("index.html", prediction_text=f"❌ Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
