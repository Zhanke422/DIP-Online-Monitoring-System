# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of known faces.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_nianqi": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

from api import Student
import eventlet
from flask import Flask, jsonify, request, redirect, render_template
from flask_socketio import SocketIO, emit

# from engineio.payload import Payload
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# eventlet.monkey_patch()
# Payload.max_decode_packets = 500
app = Flask(__name__)
socketio = SocketIO(app)
FRAME = 0


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
    process_result = process_student_face(input_frame)
    # print(process_result)
    if process_result:
        emit('face_detection_result', process_result, broadcast=True)
        status_change = check_status_change(process_result)
        if status_change:
            emit('status_change', status_change, broadcast=True)


@socketio.on('access control', namespace='/client')
def access_control(message):
    # print(message)
    emit('status_change', message, broadcast=True)

@app.route('/monitor_courseID')
def monitor_courseID():
    return render_template("monitor_courseID.html")

    # send message through notification window
@socketio.on('send_message', namespace='/client')
def handle_send_message_event(data):
    # print("Received a message: "+ data)
    # app.logger.info("Received a message: {}"['data'])
    emit('receive_message', data, broadcast = True)



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
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Is this a picture of a known student?</title>
    <h1>Upload a picture and see if it's a picture of which student!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def process_student_face(image_base64_str):
    global FRAME
    if FRAME != 100:
        FRAME += 1
        return
    FRAME = 0
    # the rest of the function will be run every two second, when FRAME flag = 100
    # this is to ease the load of program and reduce video streaming latency
    processed_str = image_base64_str[23:]  # process data to remove 'data:image/jpeg;base64,'
    # print(processed_str)
    student = Student("photo.jpg")  # put a photo of student in the same directory as this file
    authentication_status, people_in_the_frame = student.authentication(processed_str)
    return dict({'authentication_status': authentication_status,
            'people_in_the_frame': people_in_the_frame})


def check_status_change(result):
    if result['authentication_status']:
        return
    elif result['people_in_the_frame'] == 0:
        return "student leave the screen!"
    elif result['people_in_the_frame'] == 1:
        return "people in front of screen is not student!"
    else:
        return "there are " + str(result['people_in_the_frame']) + " people in front of screen!"


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
    return jsonify(result)




if __name__ == "__main__":
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)

    # app.run(host='0.0.0.0', port=5000, debug=True)
