from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load trained model
model = pickle.load(open('model/model.pkl', 'rb'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', prediction_text='', user=session['user'])

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        features = [
            float(request.form['Nitrogen']),
            float(request.form['Phosphorus']),
            float(request.form['Potassium']),
            float(request.form['temperature']),
            float(request.form['humidity']),
            float(request.form['pH']),
            float(request.form['rainfall']),
        ]
        prediction = model.predict([features])
        prediction_text = f"✅ Recommended Crop: {prediction[0]}"
    except:
        prediction_text = "❌ Error: Please enter valid numeric inputs."
    return render_template('index.html', prediction_text=prediction_text, user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
