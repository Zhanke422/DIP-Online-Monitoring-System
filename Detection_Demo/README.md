"""
This is an example of a body detection function. The human detection function 
of this program includes hand detection, body detection, face verification and 
detection and simple in vivo verification.
~~~~~~~~~~~~~~

Requirments:
  - OpenCV
  - Tencent Cloud SDK
  - face_recognition
  - numpy
  - MediaPipe

Output:
  - Video output with time and warning
  - Automatically generated warning log files
 
Optimisation objectives：
  - Separate video output and record output as two functions and use Threading 
    Module to implement multi-threaded operation for efficiency.
  - Audio Detection
  - Create an online database of face and body information
"""
