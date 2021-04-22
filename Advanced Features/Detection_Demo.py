import cv2
import os
import time
import sys
from Detection import Body_Detection_image, Hand_Detection_image, Face_Detection_image, Similarity

def Demo():
    cap = cv2.VideoCapture(0)

    frame_number = 0
    frame_max = 360

    Student = Face_Detection_image.load_student("TestFace")
    BodyInfo = Body_Detection_image.BodyInitialize()

    f = open(sys.path[0] + "/TestFace.txt","w+")

    font = cv2.FONT_HERSHEY_DUPLEX

    Abnormalities = {
        "FaceRec":0,
        "InVivo":0,
        "Hands":0,
        "Nobody":0,
        "MultiplePeople":0
    }

    Abnormalities_record = {
        "FaceRec":0,
        "InVivo":0,
        "Hands":0,
        "Nobody":0,
        "MultiplePeople":0
    }

    warnings = {
        "FaceRec":"Does not match the photograph of the person.",
        "InVivo":"May be a photograph rather than a real person.",
        "Nobody":"There is no one in front of the camera.",
        "MultiplePeople":"There are more than two people in front of the camera.",
        "Hands":"Candidate's hands are not in front of the camera.",
        "Voice":"There is a sound of talking."
    }

    def TriggerWarning(Info,trigger):
        if (trigger == 'InVivo' and Info[trigger] < 0.85) or (trigger in ['FaceRec','Nobody','MultiplePeople','Hands'] and Info[trigger] == 0):
            Abnormalities[trigger] = 0
            Abnormalities_record[trigger] = 0
        else:
            Abnormalities[trigger] += Info[trigger]
            if (trigger == 'InVivo' and Abnormalities[trigger] >= 5) or (trigger in ['FaceRec','Nobody','MultiplePeople','Hands'] and Abnormalities[trigger]>= 10):
                warning_list.append(trigger)


    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        if frame_number < frame_max:
            frame_number += 1
        else:
            frame_number = 0

        warning_list = []

        HandInfo = Hand_Detection_image.HandDetection(frame)
        frame = HandInfo["frame"]
        TriggerWarning(HandInfo,'Hands')


        FaceInfo = Face_Detection_image.FaceDetection(frame,Student)
        TriggerWarning(FaceInfo,'Nobody')
        TriggerWarning(FaceInfo,'MultiplePeople')
        TriggerWarning(FaceInfo,'FaceRec')
        

        if frame_number%60 ==0:

            BodyInfo = Body_Detection_image.BodyDetection(frame)
            TriggerWarning(BodyInfo,'Nobody')
            TriggerWarning(BodyInfo,'MultiplePeople')

            if Abnormalities['InVivo'] == 0:
                simi_img = frame
            else:
                Abnormalities['InVivo'] = Similarity.similarity(simi_img,frame)
                SimilarityInfo = {'InVivo':Abnormalities['InVivo']}
                TriggerWarning(SimilarityInfo,'InVivo')
            

        if  (frame_number%60 >= 1) and (frame_number%60 <=30) :
            if BodyInfo["BodyNum"] == 1:
                frame = Body_Detection_image.Draw_Rectangle(frame, BodyInfo)

        localtime = time.asctime( time.localtime(time.time()) )
        frame = cv2.putText(frame, localtime, (40, 50), font, 1.0, (255,250,250), 2)

        warning_list2 = list(set(warning_list))
        # print(warning_list2)

        FileText = ""
        for i in range(len(warning_list2)):
            trigger_now = warning_list2[i]
            WarningText = warnings[trigger_now]
            frame = cv2.putText(frame, WarningText, (40,90+i*35),font, 1.0, (0, 0, 255), 2)
            # print(trigger_now)
            # print("bnormalities_record[trigger_now] =" + str(Abnormalities_record[trigger_now]))
            if not Abnormalities_record[trigger_now]:
                FileText = FileText + warnings[trigger_now] + '\n'
                Abnormalities_record[trigger_now] = 1
                f.write(localtime + ": " + FileText + "\n")
        

        cv2.imshow('Detection Test', frame)

        if cv2.waitKey(5) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Demo()