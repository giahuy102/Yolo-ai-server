import cv2
import urllib
import numpy as np

from .utils.datasets import letterbox

class DetectionImage:
    def __init__(self, img_urls=[], img_size=640, stride=32):

        self.img_urls = img_urls

        self.imgs = list()

        for url in self.img_urls:
            req = urllib.urlopen(url)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            self.imgs.append(cv2.imdecode(arr, -1))

        self.n = len(self.imgs)



        self.img_size = img_size
        self.stride = stride

        self.mode = 'image'


    
    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count >= self.n:
            raise StopIteration
        img0 = self.imgs[self.count]
        source = self.img_urls[self.count]

        self.count += 1


        # Padded resize
        img = letterbox(img0, self.img_size, stride=self.stride)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        return source, img, img0, None, None

