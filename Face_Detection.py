#!/usr/bin/env python

"""
Face detection from side view (realized with api provided by Tencent)
~~~~~~~~~~~~~~

This module returns number, position and score of 'Completeness' of faces in the uploaded image, which is the side view
of student caught by camera.

Normally, there should be only one face during exam. If the face number is 0, it means student 
is not in the monitoring image, else if face number is more than 1, there is someone else here.

Parameters:
    file_stream - Original image file received

Returns:
    A dic named 'FaceDetect' contains position and score of 'Completeness' of faces in image.
    For example:
    FaceDetect = {
        "FaceNum":1,
        "X": 156,
        "Y": 129,
        "Width": 196,
        "Height": 196,
        "Completeness":99
    }
    If number of faces is 0 or larger than 1 (abnormal), return:
    FaceDetect = {
        "FaceNum":0
    }
    or
    FaceDetect = {
        "FaceNum":3
    }

Raises:
    Error - raises an exception

"""
FaceDetect = {
    "FaceNum":1
}

import json
import base64 # Image is encoded in base64 form
from numpy import mean # Calculate score of "Completeness"

from flask import Flask, jsonify, request, redirect, render_template

# Prepare to call interface (API document: https://cloud.tencent.com/document/product/867/44989)
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models

# Flask part
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
            return FaceDetect_SideView(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Error: Image uploading for face detection is unsuccessful.</title>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

def FaceDetect_SideView(file_stream):
    """Detect Faces in image (side view of student)

    Args:
        file_stream - Original image file received

    Return:
        A dic named 'FaceDetect' contains number, position and score of 'Completeness' of faces in image.

    Raises:
        Error - raises an exception
    """
    # Encode image file in bas64 form.

    base64_data = base64.b64encode(file_stream.read())
    image_encoded = str(base64_data, 'utf-8') # Important!! The 'utf-8' delete  b'' at the beginning of string.

    # Call Api
    try: 
        cred = credential.Credential("AKIDFI5dttmsqWw5xXgavzm45rMGxNYusnKd", "BqHSTQAdrpWx95mAJHxNXR6Xv43qc8ON") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile) 

        req = models.DetectFaceRequest()
        params = {
            "MaxFaceNum": 3, # Detect 3 faces at most
            "MinFaceSize": 10, # Fcae size must be larger than 10
            "Image": image_encoded, # Image encoded
            "NeedQualityDetection": 1 # Default value is 0, set it to compute score of 'Completeness'
        }
        req.from_json_string(json.dumps(params))

        resp = client.DetectFace(req) 
        data = resp.to_json_string()
        dic = json.loads(data)

        # dic['FaceInfos'] is a list containing data detected, each item contains information of a face.
        if len(dic['FaceInfos']) != 1:
            FaceDetect['FaceNum'] = len(dic['FaceInfos']) 
        else:
            v = dic['FaceInfos'][0]
            FaceDetect['X'] = v['X']
            FaceDetect['Y'] = v['Y']
            FaceDetect['Width'] = v['Width']
            FaceDetect['Height'] = v['Height']
            QualityInfo = v['FaceQualityInfo']
            CompletenessScore = list(QualityInfo['Completeness'].values())
            FaceDetect['Completeness'] = mean(CompletenessScore)
        
        return jsonify(FaceDetect)

    except TencentCloudSDKException as err: 
        print(err) 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)