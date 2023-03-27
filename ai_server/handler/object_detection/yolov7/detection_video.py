import cv2
import numpy as np

from utils.datasets import letterbox



import time



class DetectionVideo:
    def __init__(self, video_urls=[], img_size=640, stride=32):

        """
            Temporarily, this implementation is just supported for video_urls with 1 url in it
        """


        self.mode = 'video'

        self.video_urls = video_urls

        self.n = len(self.video_urls)

        if self.n > 0:
           self.new_video(self.video_urls[0]) 


        self.img_size = img_size
        self.stride = stride

        


    def __iter__(self):
        self.count = 0 # index of the video in array. Temporarily not has any usages
        return self

    def __next__(self):

        while self.frame % 20 != 0:
            

            if self.n <= 0:
                raise StopIteration
            ret_val, img0 = self.cap.read()

            if not ret_val and self.count == self.n - 1:
                raise StopIteration

            if not ret_val:
                self.count += 1
                self.cap.release()
                self.new_video(self.video_urls[self.count])
                ret_val, img0 = self.cap.read()
            

            source = self.video_urls[self.count]

            self.frame += 1
        

            # Padded resize
            img = letterbox(img0, self.img_size, stride=self.stride)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = np.ascontiguousarray(img)

        self.frame += 1









        # if self.n <= 0:
        #     raise StopIteration
        # ret_val, img0 = self.cap.read()

        # if not ret_val and self.count == self.n - 1:
        #     raise StopIteration

        # if not ret_val:
        #     self.count += 1
        #     self.cap.release()
        #     self.new_video(self.video_urls[self.count])
        #     ret_val, img0 = self.cap.read()
        

        # source = self.video_urls[self.count]

        # self.frame += 1
    

        # # Padded resize
        # img = letterbox(img0, self.img_size, stride=self.stride)[0]

        # # Convert
        # img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        # img = np.ascontiguousarray(img)







        return source, img, img0, self.cap, None


    def new_video(self, url):
        self.frame = 1
        self.cap = cv2.VideoCapture(url)
        self.nframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

