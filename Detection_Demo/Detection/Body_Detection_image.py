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
    A dic named 'bodyDetect' contains position and score of 'Completeness' of bodies in image.
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


import time
import json
import base64 # Image is encoded in base64 form
import cv2
import numpy as np

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.bda.v20200324 import bda_client, models

BodyDetect = {}

info = {
        "BodyNum":0,
        "Nobody":0,
        "MultiplePeople":0,
        "left":0,
        "top":0,
        "right":0,
        "bottom":0
    }

def BodyInitialize():
    BodyInfo = info
    return BodyInfo

def Draw_Rectangle(ImgFile,BodyInfo):
    ImgFile = cv2.rectangle(ImgFile, (BodyInfo["left"], BodyInfo["top"]), (BodyInfo["right"], BodyInfo["bottom"]), (0, 0, 255), 2)
    ImgFile = cv2.rectangle(ImgFile, (BodyInfo["left"], BodyInfo["bottom"] + 35), (BodyInfo["right"], BodyInfo["bottom"]), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    ImgFile = cv2.putText(ImgFile, 'Body', (BodyInfo["left"] + 6, BodyInfo["bottom"] - 6), font, 1.0, (255, 255, 255), 1)
    return ImgFile


def BodyDetection(ImgFile):
    image = ImgFile
    img_str = cv2.imencode('.jpg', ImgFile)[1].tostring()
    base64_data = base64.b64encode(img_str)
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

        if len(dic['BodyDetectResults']) > 1:
            BodyDetect['BodyNum'] = len(dic['BodyDetectResults'])
            info["BodyNum"] = BodyDetect['BodyNum']
            info["MultiplePeople"] = 1
        else:
            BodyDetect['BodyNum'] = 1
            v = dic['BodyDetectResults'][0]
            BodyDetect.update(v['BodyRect'])
            left = BodyDetect['X']
            top = BodyDetect['Y']
            right = left + BodyDetect['Width']
            bottom = right + BodyDetect['Height']
            info = {
                "BodyNum":1,
                "Nobody":0,
                "MultiplePeople":0,
                "left":left,
                "top":top,
                "right":right,
                "bottom":bottom
            }
            

        print(info)
        return info
     
    except TencentCloudSDKException as err:
        #print(err) Print API Error
        print("No body detected.")
        info = {
            "BodyNum":0,
            "Nobody":1,
            "MultiplePeople":0,
            "left":0,
            "top":0,
            "right":0,
            "bottom":0
        }
        return info

if __name__ == '__main__':
    BodyDetection("/Users/b0165333c/PythonTest/IM3080-DIP/Body_Face_Test/FaceBodyTest7.jpg")