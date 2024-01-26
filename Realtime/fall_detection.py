import torch
import numpy as np
import pandas as pd
import cv2
from time import time
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from cvzone.PoseModule import PoseDetector
import winsound
from winsound import PlaySound
import time
#from player import notification
#import notification
#from notification import notify
from twilio.rest import Client
from datetime import datetime
#import keys

class falldetection:

    def  __init__(self,out_file="current_time.avi"):
        self.model = self.load_model()
        self.classes = self.model.names
        self.out_file = out_file
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.camera = self.open_camera()
    def open_camera(self):
        return cv2.VideoCapture(0)
    def load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
        return model
    def out_file(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord
    def class_to_label(self, x):
        return self.classes[int(x)]
    def plot_boxes(self,results,frame):
        labels ,cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame
    def send_message(self):
        client = Client(keys.account_sid, keys.auth_token)
        message = client.messages.create(
            body="Baga g Has fallen, Alert by Intellegent system Developed By Hadi",
            from_=keys.twilio_number,
            to=keys.target_number
        )
        print("Message has sended")
    def sound_alert(self):
        PlaySound('mixkit-spell-waves-874.wav',winsound.SND_ASYNC)
        print("Alarm")
    def __call__(self, *args, **kwargs):
        segmentor = SelfiSegmentation()
        detector = PoseDetector()
        player = self.open_camera()
        assert player.isOpened()
        x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(self.out_file, four_cc, 0, (x_shape, y_shape))
        while True:
            #start_time = time()
            ret, frame = player.read()
            assert ret
            color = (10, 10, 10)
            imgnobg = segmentor.removeBG(frame, color, threshold=0.20)
            imgnobg = blur_img = cv2.medianBlur(imgnobg, 5)
            imgnobg = detector.findPose(imgnobg)
            lmList, bboxInfo = detector.findPosition(imgnobg, bboxWithHands=False)
            if bboxInfo:
                center = bboxInfo["center"]
                cv2.circle(imgnobg, center, 5, (255, 0, 255), cv2.FILLED)
            results = self.score_frame(imgnobg)

            last = self.plot_boxes(results, imgnobg)
            #color = (0,0,0)
            #frame = segmentor.removeBG(frame, color, threshold=0.50)
            #end_time = time()
            #fps = 1/np.round(end_time - start_time, 3)
            #print(f"Frame per Second : {fps}" )
            result = list(results)
            #print(results[1])
            for i in results[1]:
                print(i[3])
                if i[3] == 1.0:
                    # self.send_message()
                    #self.sound_alert()
                    self.send_message()
                    time.sleep(5)
                    print("Fall Detected, Message sended")

            #a = np.array(result[1])
           # a
            #for i in a:
               # if i[2] >= 0.7:
                 #   print("Buda has Fall")
                    #self.send_message()
                 #   self.sound_alert()

            #print(f"Reults: {results}")
            cv2.imshow('frame',last)
            out.write(last)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        player.release()
        cv2.destroyAllWindows()
a = falldetection()
a()
