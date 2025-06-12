import os

from flask import Flask, request, jsonify
from voice_classification import load_model, predict_emotion
from werkzeug.utils import secure_filename
from flask_cors import CORS
from audio_analysis import analyze_wav_audio

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/voice_classification', methods=['POST'])
def voice_classification():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    speaker_text = request.form.get('speaker_text')
    print(speaker_text)
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    if not file.filename.lower().endswith('.wav'):
        return jsonify({'error': 'Only .wav files are supported'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    processor, model = load_model()

    try:
        result = predict_emotion(file_path, processor, model)
        result2 = analyze_wav_audio(file_path, speaker_text)
        return jsonify({
            'emotion': result['label'],
            'confidence': result['confidence'],
            'audio': result2
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
