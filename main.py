# XXGurjot07 !! 01/05/2021
'''NOTE : recusion is involved heavily is this program, as video frames are coming as they are bring manipulated and being drawn on,
so i have restricted myself from making a lot of derived classes and what not, repeating code and all that, this may not be most efficient way to 
to do this in one go,    ~~~Cherrio '''
import cv2
from mediapipe import python
import time
import math
import mediapipe as mp
import numpy as np

# control of audio systems - library (PYCAW - github)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# main function


class run_detection:
    display_lst = input(
        "Press 'y' for Parameter Selection, 'd' for Default (Parameters), 'n' to Quit - ")

    if display_lst == "d":
        max_num_hands = 1
        min_detection_confidence = 0.6
        min_tracking_confidence = 0.7
    elif display_lst == "n":
        quit()
    else:
        max_num_hands = int(
            input("Maximum No. of Hands for Detection - "))
        min_detection_confidence = float(
            input("Minimum Detection Confidence (default = 0.5) - "))
        min_tracking_confidence = float(
            input("Minimum Tracking Confidence (default = 0.7) - "))

    def __init__(self):
        # command arugment
        to_toggle_vol = False
        # camera index (sort of), used DroidCAM to model phone camera as webcam
        self.my_capture = cv2.VideoCapture(1)
        self.mphands = mp.solutions.hands
        self.my_hands = mp.solutions.hands.Hands(False, self.max_num_hands, 1, self.min_detection_confidence,
                                                 self.min_tracking_confidence)  # initialize Hands solution file
        # intitialze drawing calcutions + styles
        self.mp_Draw = mp.solutions.drawing_utils
        self.mp_DrawStyles = mp.solutions.drawing_styles

        self.pTime = 0
        self.cTime = 0
        Alive = bool(True)
        frameNo = 0
        # max no. of hands is set from input condtion
        # while frames are coming, perform processes and draws landmarks and connection
        while Alive == True:
            # returns 2 values (bool_value, image)
            was_success, self.my_frames = self.my_capture.read()
            lmList = []
            # MediaPipe uses RGB, Open CV uses BGR
            self.my_framesRGB = cv2.cvtColor(self.my_frames, cv2.COLOR_BGR2RGB)
            self.result = self.my_hands.process(self.my_framesRGB)
            if self.result.multi_hand_landmarks:  # if result = true i.e it found any hands, executes the for loop for each hand and draws point and line
                for self.hand_landmarks in self.result.multi_hand_landmarks:

                    for id, landmarks_co in enumerate(self.hand_landmarks.landmark):
                        height, widht, channels = self.my_frames.shape
                        self.x_co = int(landmarks_co.x * widht)
                        self.y_co = int(landmarks_co.y * height)

                        # stores values in list
                        lmList.append([id, self.x_co, self.y_co])

                    self.mp_Draw.draw_landmarks(self.my_frames, self.hand_landmarks, self.mphands.HAND_CONNECTIONS,
                                                self.mp_DrawStyles.get_default_hand_landmarks_style(),
                                                self.mp_DrawStyles.get_default_hand_connections_style())

            # FPS Calculation
            self.cTime = time.time()
            self.FPS = 1 / (self.cTime - self.pTime)
            self.pTime = self.cTime
            # FPS display
            cv2.putText(self.my_frames, str(int(self.FPS)), (0, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (256, 155, 256), 2)

            # print("FPS = ", str(int(self.FPS)))

            # getting data in list only when data is there
            if self.display_lst == "y" or self.display_lst == "Y" or self.display_lst == "d":
                if len(lmList) != 0:
                    pass  # print(lmList[4],lmList[8])
            else:
                pass
            # comment underlying if else, to disable volume control
            if len(lmList) != 0:
                # plotting specific points
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                # toggle switch, middle finger tip co-ordinates
                x3, y3 = lmList[20][1], lmList[20][2]
                cx, cy = (x1+x2) // 2, (y1+y2) // 2

                cv2.circle(self.my_frames, (x1, y1), 7,
                           (163, 111, 103), cv2.FILLED)
                cv2.circle(self.my_frames, (x2, y2), 7,
                           (163, 111, 103), cv2.FILLED)
                cv2.line(self.my_frames, (x1, y1), (x2, y2), (89, 89, 255), 5)
                cv2.circle(self.my_frames, (cx, cy), 6,
                           (255, 222, 205), cv2.FILLED)

                # mapping length, as volume scale, personal tweaking can be done here
                length = math.hypot(y2-y1, x2-x1)
                minVol = -45.0
                maxVol = 0.0
                vol = np.interp(length, [20, 140], [minVol, maxVol])
                print(length)
                # the distance between tip of pinky finger and thumb will determine this and toggle - set volume command
                length_toggle = math.hypot(y3-y1, x3-x1)
                # print(length_toggle)
                # print(to_toggle_vol)

                # an preliminary solution to control jittering
                if frameNo % 15 == 0:
                    if length_toggle <= 50:
                        to_toggle_vol = not to_toggle_vol
                frameNo += 1 
                if frameNo == 300:
                    frameNo = 0
                #solution end
                
                if to_toggle_vol == True:
                    # set volume function
                    print(int(vol))
                    cv2.putText(self.my_frames, str("Control : Enabled"), (300, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (75, 255, 146), 2)
                    volume.SetMasterVolumeLevel(vol, None)
                else:
                    cv2.putText(self.my_frames, str("Control : Disabled"), (300, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (53, 41, 223), 2)

            cv2.imshow("Open CV Capture", self.my_frames)

            # pressing space will Exit Main Loop
            keypress = cv2.waitKey(1)
            if keypress == ord(" "):
                Alive = False
