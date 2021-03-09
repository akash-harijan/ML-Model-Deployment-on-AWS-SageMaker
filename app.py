# https://forums.developer.nvidia.com/t/how-to-use-tensorrt-by-the-multi-threading-package-of-python/123085/8


# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

import os
import json
import flask
import cv2
import numpy as np
from CataractDetection import CataractDetector
import time

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')
weight_path = os.path.join(model_path, 'final-700imgs.h5')

predictor = CataractDetector(weight_path)
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        predictor
        status = 200
    except:
        status = 400
    return flask.Response(response=json.dumps(' '), status=status, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def transformation():
    t1 = time.time()
    np_data = np.fromstring(flask.request.data, np.uint8)
    print("Input Shape : {0}".format(np_data.shape))
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    print("Original Size : {0}".format(img.shape))
    print("Pre Processing : {0}".format(1 / (time.time() - t1)))

    t1 = time.time()
    output = predictor.predict(img)
    print("TIME : {}".format(1 / (time.time() - t1)))

    print("Output : {0}".format(output))
    output = {"output": output if isinstance(output, str) else str(output)}

    return json.dumps(output)
