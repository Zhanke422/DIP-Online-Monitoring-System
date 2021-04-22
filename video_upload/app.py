import face_recognition
from flask import Flask, jsonify, request, redirect, render_template
from flask import Flask, render_template, request,Response,jsonify
from flask_cors import CORS
import json
import cv2
import base64
import numpy
from PIL import Image
import io
import warnings

warnings.simplefilter("ignore", DeprecationWarning)
app = Flask(__name__)
CORS(app, supports_credentials=True)
 
 
@app.route('/')
def hello_world():
 
    return Response('hello_world')
 
 
@app.route('/video_sample/')
def video_sample():
 
    return render_template('camera.html')
 
 
@app.route('/receiveImage/', methods=["GET","POST"])
def receive_image():
 
    if request.method == "POST":
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        str_image = json_data.get("imgData")
        #print(str_image)
        img = base64.b64decode(str_image)
        print(img)
        img_np = numpy.fromstring(img, dtype='uint8')
        new_img_np = cv2.imdecode(img_np, 1)
        # im=Image.fromarray(img_np)
        print(type(new_img_np))
        cv2.imwrite('./images/rev_image.jpg',new_img_np)
        
        path = './images/rev_image.jpg'
        #file = base64.decodestring(json.dumps(data)['imgData'])
        #file = base64.decodebytes(json.dumps(data)['imgData'])
        print('data:{}'.format('success'))
 
    return detect_faces_in_image(path)

def detect_faces_in_image(file_stream):
    # Load some sample pictures and learn how to recognize them.
    naq_image = face_recognition.load_image_file("naqphoto.jpg")
    naq_face_encoding = face_recognition.face_encodings(naq_image)[0]
    hby_image = face_recognition.load_image_file("hbyphoto.jpg")
    hby_face_encoding = face_recognition.face_encodings(hby_image)[0]
    known_face_encoding = [
        naq_face_encoding,
        hby_face_encoding
    ]

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    # is_nianqi = False
    is_who = ""

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of students
        match_results = face_recognition.compare_faces(known_face_encoding, unknown_face_encodings[0])
        if match_results[0]:
            is_who = "Ni Anqi"
        elif match_results[1]:
            is_who = "Hou Boyu"

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_who": is_who,
    }

    print(result)
    return jsonify(result)
 
 
if __name__ == '__main__':
 
    app.run(debug=True,host='0.0.0.0',port=5000)