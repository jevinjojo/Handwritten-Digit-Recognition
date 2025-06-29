from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load your model (adjust path if needed)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model.pkl')
model = joblib.load(MODEL_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Example: get data from form
        data = request.form.get('data')
        # Convert data as needed for your model
        prediction = model.predict(np.array([data]).reshape(1, -1))
        return render_template('index.html', prediction=prediction)
    return render_template('index.html')

# Vercel looks for 'app' variable; do NOT use app.run()
