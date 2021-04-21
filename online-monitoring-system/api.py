import face_recognition
import cv2
import base64
import numpy as np


class Student:
    def __init__(self, image_file):
        # Load picture of the student and learn how to recognize it.
        student_image = face_recognition.load_image_file(image_file)
        self.face_encoding = [face_recognition.face_encodings(student_image)[0]]
        self.missing_frame = 0

        def authentication(self, webcam_capture):
        '''
        This function check whether the face captured by webcam is the same as the picture of student in the database.
        :param webcam_capture: A data string of picture captured by web camera, encoded in base64 format
        :return: True or False value indicating the authentication status, also the number of people in the picture
        '''
        # webcam_capture is one frame of picture captured by web camera
        # captured_image = face_recognition.load_image_file(webcam_capture)
        img_data = base64.b64decode(webcam_capture)
        np_arr = np.frombuffer(img_data, np.uint8)
        img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imwrite('buffer.jpeg', img_np)
        captured_image = face_recognition.load_image_file('buffer.jpeg')
        capture_encodings = face_recognition.face_encodings(captured_image)
        if len(capture_encodings):
            if len(capture_encodings) == 1:
                capture_encoding = capture_encodings[0]
                match = face_recognition.compare_faces(self.face_encoding, capture_encoding, tolerance=0.3)
                # note for tolerance value: tried 0.5, but does not give a very good result
                if match[0]:
                    return [True, 1]
                else:
                    return [False, 1]
            else:
                return [False, len(capture_encodings)]
        else:
            return [False, 0]
