# This is the flask server we build for the exam monitoring system.
# Run this file and open localhost:5000/homepage on your browser to start explore our system!

from api import Student
import eventlet
from flask import Flask, jsonify, request, redirect, render_template
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# eventlet.monkey_patch()
Payload.max_decode_packets = 50 # if any payload warning occurs, can try to increase this number
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



if __name__ == "__main__":
    socketio.run(app=app, host='0.0.0.0', port=5000, debug=True)

    # app.run(host='0.0.0.0', port=5000, debug=True)
