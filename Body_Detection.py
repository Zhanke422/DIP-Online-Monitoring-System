#!/usr/bin/env python

"""
Body detection from side view (realized with api provided by Tencent)
~~~~~~~~~~~~~~

This module returns number and position of bodies in the uploaded image, which is the side view
of student caught by camera.

Normally, there should be only one body during exam. If the body number is 0, it means student 
is not in the monitoring image, else if body number is more than 1, there is someone else here.

Parameters:
    file_stream - Original image file received

Returns:
    A dic named 'BodyDetect' contains number and position of bodies in image.
    For example:
    BodyDetect = {
        "BodyNum":1,
        "X": 156,
        "Y": 129,
        "Width": 196,
        "Height": 196
    }
    If number of bodies is 0 or larger than 1 (abnormal), return:
    BodyDetect = {
        "BodyNum":0
    }
    or
    BodyDetect = {
        "BodyNum":3
    }

Raises:
    Error - raises an exception

"""

import json
import base64 # Image is encoded in base64 form

from flask import Flask, jsonify, request, redirect, render_template

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.bda.v20200324 import bda_client, models

#Default Value
BodyDetect = {
    "BodyNum":1
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/homepage')
def home():
    return render_template("homepage.html")

@app.route('/student_list')
def student_list():
    return render_template("student_list.html")

@app.route('/examiner_list')
def examiner_list():
    return render_template("examiner_list.html")

@app.route('/exam_courseID')
def exam_courseID():
    return render_template("exam_courseID.html")

@app.route('/monitor_courseID')
def monitor_courseID():
    return render_template("monitor_courseID.html")

@app.route('/administrator_list')
def administrator_list():
    return render_template("administrator_list.html")


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return BodyDetect_SideView(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Error: Image uploading for body detection is unsuccessful.</title>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''
def BodyDetect_SideView(file_stream):
    """Detect Bodies in image (side view of student)

    Args:
        file_stream - Original image file received

    Return:
        A dic named 'BodyDetect' contains number and position of bodies in image.

    Raises:
        Error - raises an exception
    """

    # Encode image file in bas64 form.
    base64_data = base64.b64encode(file_stream.read())
    image_encoded = str(base64_data, 'utf-8') 

    # Call Api
    try: 
        cred = credential.Credential("AKIDFI5dttmsqWw5xXgavzm45rMGxNYusnKd", "BqHSTQAdrpWx95mAJHxNXR6Xv43qc8ON") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "bda.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = bda_client.BdaClient(cred, "ap-shanghai", clientProfile) 

        req = models.DetectBodyRequest()
        params = {
            "Image": image_encoded, # Image encoded
            "MaxBodyNum": 3 # Detect 3 bodies at most
        }
        req.from_json_string(json.dumps(params))

        resp = client.DetectBody(req) 
        data = resp.to_json_string()
        dic = json.loads(data)

        # dic['BodyDetectResults'] is a list containing result data, each item contains information of a body.
        if len(dic['BodyDetectResults']) != 1:
            BodyDetect['BodyNum'] = len(dic['BodyDetectResults'])
        else:
            v = dic['BodyDetectResults'][0]
            BodyDetect.update(v['BodyRect'])

        return jsonify(BodyDetect)
        
    except TencentCloudSDKException as err: 
        print(err)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)