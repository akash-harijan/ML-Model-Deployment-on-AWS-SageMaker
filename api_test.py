from __future__ import print_function
import requests
import cv2
import glob
import time
import json
import os
import numpy as np


image_folder = 'test_imgs'
abs_path = os.path.abspath(image_folder)
regex_path = os.path.join(abs_path, '*.jpeg')
file_paths = sorted(glob.glob(regex_path))
print('Files : ', len(file_paths))

assert(len(file_paths) != 0)

addr = "http://0.0.0.0:8080"
url = addr + '/invocations'

content_type = 'application/json'
headers = {'content-type': content_type}

ls_fps = []
ls_images = []
index = 1
for img_path in file_paths:

    img = cv2.imread(img_path)
    _, payload = cv2.imencode('.png', img)

    t2 = time.time()
    response = requests.post(url, data=payload.tobytes(), headers=headers)
    fps2 = 1/(time.time()-t2)
    print("FPS model : {}".format(fps2))
    # decode response

    output = json.loads(response.text)
    print("Output : {0}".format(output))

    ls_fps.append(fps2)

print("Avg FPS : ", np.mean(ls_fps))
