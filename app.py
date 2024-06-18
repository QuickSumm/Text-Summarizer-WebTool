import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from QuickSumm import summarize_text
import chardet

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath, file_extension):
    if file_extension == 'txt':
        with open(filepath, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            text = raw_data.decode(encoding)
    else:
        text = ""
    return text

@app.route('/')
def home():
    return render_template('QuickSumm.html')

@app.route('/summarize', methods=['POST'])
def summarization():
    if request.is_json:
        data = request.get_json()
        text = data.get('input_text', '')
        summary = summarize_text(text)
        return jsonify({'summary': summary})
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        file_extension = filename.rsplit('.', 1)[1].lower()
        text = extract_text_from_file(filepath, file_extension)

        return jsonify({'text': text})
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
