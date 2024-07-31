from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from highlight_generator import generate_highlights

main = Blueprint('main', __name__)

# Configure allowed extensions and maximum file size (1.5 GB)
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'avi'}
MAX_CONTENT_LENGTH = 1.5 * 1024 * 1024 * 1024  # 1.5 GB

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.before_app_request
def before_request():
    """Set the maximum content length for file uploads."""
    current_app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@main.route('/upload-video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        success = generate_highlights(file_path)
        if success:
            return jsonify({'message': 'File uploaded and highlights generated successfully', 'filename': filename}), 200
        else:
            return jsonify({'error': 'Failed to generate highlights.'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to upload the file.'}), 500

@main.route('/upload-link', methods=['POST'])
def upload_link():
    data = request.get_json()
    video_link = data.get('videoLink')
    
    if not video_link:
        return jsonify({'error': 'No video link provided'}), 400

    # Process the video link
    success = generate_highlights(video_link)
    if success:
        return jsonify({'message': 'Link processed and highlights generated successfully', 'link': video_link}), 200
    else:
        return jsonify({'error': 'Failed to generate highlights from link.'}), 500
