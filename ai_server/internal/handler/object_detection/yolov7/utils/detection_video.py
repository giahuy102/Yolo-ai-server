import cv2
import numpy as np
import time

from utils.datasets import letterbox

MAX_FRAME = 30

class DetectionVideo:
    def __init__(self, video_url, img_size=640, stride=32):
        self.mode = 'video'
        self.video_url = video_url
        self.new_video(self.video_url) 
        self.img_size = img_size
        self.stride = stride

        
    def __iter__(self):
        self.count = 0 # Temporarily not has any usages
        return self

    def __next__(self):
        ret_val, img0 = self.cap.read()

        if self.frame >= MAX_FRAME:
            self.cap.release()
            raise StopIteration

        if not ret_val:
            self.cap.release()
            raise StopIteration
        source = self.video_url

        self.frame += 1
    

        # Padded resize
        img = letterbox(img0, self.img_size, stride=self.stride)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        return source, img, img0, self.cap, None, True


    def new_video(self, url):
        self.frame = 0
        self.cap = cv2.VideoCapture(url)
        self.nframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
