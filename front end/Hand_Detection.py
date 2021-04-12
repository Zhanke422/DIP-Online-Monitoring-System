#!/usr/bin/env python

"""
Hand detection (realized with MediaPipe)
~~~~~~~~~~~~~~

This module returns number and position of hands in image.

Normally, there should be 2 hands.

Requirements:
    cv2
    numpy
    mediapipe
    eventlet
    flask
    flask_socketio

Parameters:
    file_stream - Original image file received

Returns:
    A dic named 'HandDetect' contains state.
    For example:, if number of hands is 2 (Normal)
    HandDetect = {
        "Normal":1
    }
    If number of hands is 0 or 1, return:
    HandDetect = {
        "Normal":0
    }

Raises:
    Error - raises an exception

"""
import cv2
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

import eventlet
from flask_socketio import SocketIO, emit
from flask import Flask, jsonify, request, redirect, render_template

#Default Value
HandDetect = {
        "Normal":1
}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
eventlet.monkey_patch()
app = Flask(__name__)
socketio = SocketIO(app)

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

@socketio.on('connect', namespace='/client')
def connect():
    print("client connected!")


@socketio.on('webcam capture', namespace='/client')
def webcam_capture(input_frame):
    # print("receive frame in server")
    # print(input_frame)
    emit('video_feed', {'data': input_frame}, broadcast=True)
    # print("send out frame to examiner side")

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
            return Hand_Detect(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Error: Image uploading for hand detection is not successful.</title>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''

def Hand_Detect(file_stream):
    """Detect hands in image 

    Args:
        file_stream - Original image file received

    Return:
        A dic named 'HandDetect' contains detection result.
    """
    with mp_hands.Hands(
        static_image_mode=True, #hand detection runs on every input image, ideal for processing a batch of static images. 
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        bytes_stream = np.asarray(bytearray(file_stream.read()), dtype="uint8")
        img = cv2.imdecode(bytes_stream, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        if not results.multi_hand_landmarks:
            HandDetect['Normal'] = 0
        elif len(results.multi_handedness) != 2:
            HandDetect['Normal'] = 0
        
        return jsonify(HandDetect)

if __name__ == "__main__":
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)
        