
import boto3
import glob
import time
import cv2
import os
import numpy as np
import json

client = boto3.client('sagemaker-runtime')

endpoint_name = "endpoint-name"                  # Your endpoint name.
content_type = "image/png"                       # The MIME type of the input data in the request body.
accept = "application/json"                       # The desired MIME type of the inference in the response.

image_folder = 'test_imgs'
abs_path = os.path.abspath(image_folder)
regex_path = os.path.join(abs_path, '*.jpeg')
file_paths = sorted(glob.glob(regex_path))
print('Files : ', len(file_paths))


ls_fps = []
fps = 0
for img_path in file_paths:

    img = cv2.imread(img_path)
    _, encoded_image = cv2.imencode('.png', img)
    payload = encoded_image.tobytes()

    t1 = time.time()
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType=content_type,
        Accept=accept,
        Body=payload
        )

    fps = (fps + 1/(time.time()-t1))/2
    output = json.loads(response["Body"].read().decode("utf-8"))

    print("Output {0}".format(output))

    print('FPS : ', fps)
    ls_fps.append(fps)

print("Avg FPS : ", np.mean(ls_fps))
