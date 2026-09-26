import os
import boto3
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Initialize the Blueprint
upload_bp = Blueprint('upload_api', __name__)

# AWS S3 Configuration (Uses your attached EC2 IAM Role automatically)
s3 = boto3.client('s3', region_name='eu-north-1')
BUCKET_NAME = 'your-actual-bucket-name-here'

@upload_bp.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Sanitize the filename to prevent directory traversal attacks
    filename = secure_filename(file.filename)
    
    try:
        # 1. Ship to Amazon S3 for permanent, scalable storage
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        
        # 2. Reset the file pointer so your TensorFlow model can read it
        file.seek(0)
        
        # 3. (Insert your TensorFlow Protein model prediction logic here)
        # sequence_data = file.read()
        # prediction = model.predict(sequence_data)
        
        # 4. Return the data to your asynchronous frontend
        return "File successfully archived in S3 and processed by model.", 200
        
    except Exception as e:
        return jsonify({'error': f"Cloud ingestion failed: {str(e)}"}), 500
