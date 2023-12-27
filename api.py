from flask import Flask, jsonify, request
from ultralytics import YOLO
from utils.vehicles_in_result import vehicles_in_result
from time import time
from pathlib import Path
from shutil import rmtree
import os
import uuid
from PIL import Image
import glob

# Initialize Flask app
app = Flask(__name__)
if os.path.exists('./temp') and os.path.isdir('./temp'):
    rmtree('./temp')
Path('./temp').mkdir(exist_ok=True)

# Initialize YOLOv8
model = YOLO("yolov8n.pt")


@app.route('/api/health/', methods=['GET'])
def health():
    return { 'message': 'API is up' }


@app.route('/api/inference/', methods=['POST'])
def inference():
    if 'images' not in request.files or not len(request.files.getlist('images')):
        return { 'error': 'Image files not provided' }, 400

    t0 = time()

    # Initialize temp directory for image files
    temp_dir = f'./temp/{uuid.uuid4().hex}'
    Path(temp_dir).mkdir(exist_ok=True)
    
    received_files = request.files.getlist('images')
    for f in received_files:
        file_name = f.headers['Content-Disposition'].split('filename=')[1][1:-1]
        if file_name == '':
            return { 'error': 'Image files not provided' }, 400
        file_path = f'{temp_dir}/{file_name}'
        f.save(file_path)

    try:
        files = sorted(glob.glob(os.path.join(temp_dir, '*.*')))
        for file in files:
            im = Image.open(file)
            im.verify()
            im.close()
            im = Image.open(file) 
            im.transpose(Image.FLIP_LEFT_RIGHT)
            im.close()
        results = model.predict(source=temp_dir, stream=True, verbose=False)
        vehicle_counts = [vehicles_in_result(result.boxes.cls) for result in results]
        vehicle_count = sum(vehicle_counts)
        time_taken = f'{time() - t0:.3f}s'
        rmtree(temp_dir)
        return jsonify({'vehicle_count' : vehicle_count, 'time_taken': time_taken})
    except Exception as e:
        print(f'{prefix()} Error:', e)
        return { 'error': 'One or more images are corrupt' }, 400
    

def prefix():
    return '[API]'