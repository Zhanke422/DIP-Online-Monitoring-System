import face_recognition
import cv2
import numpy as np
import time
import os

face_locations = []
face_encodings = []
face_names = []
FaceInfo = {}

def load_student(student_name):
    imgfile = "/Users/b0165333c/Desktop/"+ student_name +".png"
    if os.path.isfile(imgfile):
        student_image = face_recognition.load_image_file("/Users/b0165333c/Desktop/"+ student_name +".png")
        student_face_encoding = face_recognition.face_encodings(student_image)[0]

        known_face_encodings = [
            student_face_encoding
        ]
        known_face_names = [
            student_name
        ]
        info = {
            "known_face_encodings":known_face_encodings,
            "known_face_names":known_face_names   
        }

        return info
    else:
        print("Student image file doesn't exist.")
        return False


def FaceDetection(ImgFile,Student):

    known_face_encodings = Student["known_face_encodings"]
    known_face_names = Student["known_face_names"]

    frame = ImgFile
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    #cv2.imshow('Video', frame)
    FaceInfo = {
        'frame':frame,
        'Nobody':0,
        'MultiplePeople':0,
        'FaceRec':0
    }

    if len(face_encodings) == 0:
        FaceInfo["Nobody"] = 1
    elif len(face_encodings) > 1:
        FaceInfo['MultiplePeople'] = 1
    elif known_face_names[0] not in face_names:
        FaceInfo['FaceRec'] = 1

    return FaceInfo


if __name__ == "__main__":
    student = load_student("TestFace")

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        FaceInfo = FaceDetection(frame,student)
        frame = FaceInfo['frame']
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


