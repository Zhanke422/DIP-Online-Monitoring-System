import face_recognition
import cv2


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
        captured_image = face_recognition.load_image_file(webcam_capture)
        capture_encoding = face_recognition.face_encodings(captured_image)[0]
        match = face_recognition.compare_faces(self.face_encoding, capture_encoding, tolerance=0.5)
        if match[0]:
            return True
        else:
            return False

    def check_presence(self, image_file):
        '''
        This function check the presence of the student by checking the current frame takes in from web cam.
        If the student has not been recognized for more than 5 frames, the function will return false.
        :param image_file: one frame of picture captured by web camera
        :return: True or False value indicating the presence status
        '''
        # set a flag with original value to be True
        presence_flag = True
        trigger_value = 5
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

