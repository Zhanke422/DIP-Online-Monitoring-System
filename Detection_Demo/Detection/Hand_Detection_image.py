#!/usr/bin/env python

"""
Hand detection (realized with MediaPipe)
~~~~~~~~~~~~~~

This module returns number and position of hands in image.
MediaPipe document:https://google.github.io/mediapipe/solutions/hands#python-solution-api

Normally, there should be 2 hands.

Parameters:
    file_stream - Original image file received

Returns:
    A dic named 'HandDetect' contains number and position of hands.
    For example:
    HandDetect = {
        "HandNum":2,
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

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#Default Value
HandInfo = {
        "Hands":0
}

font = cv2.FONT_HERSHEY_DUPLEX

warning = "Candidate's hands are not in front of the camera."

def HandDetection(ImgFile):

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:

        image = cv2.flip(ImgFile, 1)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            HandInfo['Hands'] = 1
        else:
            image_height, image_width, _ = image.shape
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            if len(results.multi_handedness) !=2:
                HandInfo['Hands'] = 1
            else:
                HandInfo['Hands'] = 0
            
        HandInfo['frame'] = image

    return HandInfo

if __name__ == '__main__':
    HandDetection("/Users/b0165333c/PythonTest/IM3080-DIP/Body_Face_Test/FaceBodyTest6.jpg")
    print(HandDetect)
