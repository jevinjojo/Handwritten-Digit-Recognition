import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import numpy as np
import cv2
try:
    from tflite_runtime.interpreter import Interpreter
    USE_TFLITE = True
except ImportError:
    import tensorflow as tf
    USE_TFLITE = False

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the model (prefer TFLite for deployment)
if USE_TFLITE:
    interpreter = Interpreter(model_path='handwritten.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
else:
    model = tf.keras.models.load_model('handwritten.keras')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28))
    img = 255 - img  # invert colors as in your script
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)
    return img


def predict_digit(img):
    if USE_TFLITE:
        interpreter.set_tensor(input_details[0]['index'], img.astype(np.float32))
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        return int(np.argmax(output_data))
    else:
        prediction = model.predict(img)
        return int(np.argmax(prediction))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Preprocess and predict
            try:
                img = preprocess_image(filepath)
                digit = predict_digit(img)
                return render_template('index.html', filename=filename, prediction=digit)
            except Exception as e:
                flash(f'Error processing image: {e}')
                return redirect(request.url)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)