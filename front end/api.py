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
        :param webcam_capture: one frame of picture captured by web camera
        :return: True or False value indicating the authentication status
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
                match = face_recognition.compare_faces(self.face_encoding, capture_encoding, tolerance=0.3) # note for tolerance value: tried 0.5, but does not give a very good result
                if match[0]:
                    return [True, 1]
                else:
                    return [False, 1]
            else:
                return [False, len(capture_encodings)]
        else:
            return [False, 0]


    def check_presence(self, image_file):
        '''
        This function check the presence of the student by checking the current frame takes in from web cam.
        If the student has not been recognized for more than 5 frames, the function will return false.
        :param image_file: one frame of picture captured by web camera
        :return: True or False value indicating the presence status
        '''
        # set a flag with original value to be True
        presence_flag = True
        trigger_value = 60
        while presence_flag:
            if not self.authentication(image_file):
                self.missing_frame += 1
            else:
                # reset to 0
                self.missing_frame = 0
            if self.missing_frame >= trigger_value:
                return False
            else:
                return True

    def authentication_return_picture_with_rectangle(self, image_file):
        '''
        This function takes in the image of student, do the authentication then return picture with a rectangle around detected face.
        :param image_file: one frame of picture captured by web camera
        :return: a image_file with a rectangle around detected face or nothing indicating nothing is found
        '''
        if not self.authentication(image_file):
            return None

        # Initialize face_location as a list
        face_location = []

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = image_file[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_location.append(face_recognition.face_locations(rgb_frame))

        for (top, right, bottom, left) in zip(face_location):
            # Draw a box around the face
            cv2.rectangle(image_file, (left, top), (right, bottom), (0, 0, 255), 2)
        # not sure if I should destroy all windows here, if something wrong happens,
        # then try commenting the next line of code and rerun
        cv2.destroyAllWindows()
        return image_file

    def authentication_return_video(self, video_file):
        '''
        A temporary function for reading in a video file and output a file with rectangles around face detected.
        :param video_file:
        :return: output video file for demo
        '''
        # Open the input movie file
        input_movie = cv2.VideoCapture(video_file)
        length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create an output movie file (make sure resolution/frame rate matches input video!)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter('student_output.avi', fourcc, 29.97, (1280, 720))

        frame_number = 0

        while True:
            # Grab a single frame of video
            ret, frame = input_movie.read()
            frame_number += 1

            # Quit when the input video file ends
            if not ret:
                break

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                match = face_recognition.compare_faces(self.face_encoding, face_encoding, tolerance=0.50)

                name = None
                if match[0]:
                    name = "Ni Anqi"

                face_names.append(name)

            # Label the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not name:
                    continue

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            # Write the resulting image to the output video file

            output_movie.write(frame)
            print("Writing frame {} / {}".format(frame_number, length))

        # All done!
        input_movie.release()
        cv2.destroyAllWindows()
        return output_movie
