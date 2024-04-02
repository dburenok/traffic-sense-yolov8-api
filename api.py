from flask import Flask, jsonify, request
from time import time
from uuid import uuid4
from PIL import Image
import glob
import os
from deepsparse import Pipeline
from utils.vehicles_in_result import vehicles_in_result
from utils.dir import init_dir, delete_dir

TEMP_DIR = './temp'
MODEL_PATH = "best.onnx"
print("Creating deepsparse pipeline...")
yolo_pipeline = Pipeline.create(task="yolov8", model_path=MODEL_PATH)

# Initialize Flask app
init_dir(TEMP_DIR)
print("Initializing API...")
app = Flask(__name__)


@app.route('/api/health/', methods=['GET'])
def health():
    return { 'message': 'API is up' }


@app.route('/api/inference/', methods=['POST'])
def inference():
    t0 = time()
    ERR_RESPONSE = jsonify({'vehicle_count' : -1})
    if 'images' not in request.files or not len(request.files.getlist('images')):
        print('Images not provided')
        return ERR_RESPONSE
    image_temp_dir = f'{TEMP_DIR}/{str(uuid4())[0:8]}'
    init_dir(image_temp_dir)
    received_files = request.files.getlist('images')
    for f in received_files:
        file_name = f.headers['Content-Disposition'].split('filename=')[1][1:-1]
        if file_name == '':
            print('File name not provided')
            return ERR_RESPONSE
        file_path = f'{image_temp_dir}/{file_name}'
        f.save(file_path)
    try:
        files = sorted(glob.glob(os.path.join(image_temp_dir, '*')))
        pipeline_outputs = yolo_pipeline(images=files, conf_thres=0.25)
        boxes = [x[0] for x in pipeline_outputs]
        vehicle_count = sum([len(x) for x in boxes])
        delete_dir(image_temp_dir)
        time_taken = f'{time() - t0:.3f}s'
        print(f'vehicle_count={vehicle_count}, {time_taken} for {len(files)} images')
        return jsonify({'vehicle_count' : vehicle_count})
    except Exception as e:
        print(e)
        delete_dir(image_temp_dir)
        return ERR_RESPONSE