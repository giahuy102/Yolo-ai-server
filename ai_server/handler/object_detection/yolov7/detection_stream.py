import numpy as np
import cv2
import copy

from .utils.datasets import letterbox



class DetectionStream:
    def __init__(self, stream_loader, img_size=640, stride=32):
        self.mode = 'stream'


        self.stream_loader = stream_loader
        self.img_size = img_size
        self.stride = stride


        # check for common shapes
        s = np.stack([letterbox(x, self.img_size, stride=self.stride)[0].shape for x in self.stream_loader.get_frames()], 0)  # shapes
        self.rect = np.unique(s, axis=0).shape[0] == 1  # rect inference if all shapes equal
        if not self.rect:
            print('WARNING: Different stream shapes detected. For optimal performance supply similarly-shaped streams.')


    def __iter__(self):
        self.count = -1
        return self


    def __next__(self):
        self.count += 1
        img0 = self.stream_loader.get_frames().copy()
        stream_infos = copy.deepcopy(list(self.stream_loader.get_stream_infos().values()))
        sources = [info.rtsp_url for info in stream_infos.values()]



        if cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration

        # Letterbox
        img = [letterbox(x, self.img_size, auto=self.rect, stride=self.stride)[0] for x in img0]

        # Stack
        img = np.stack(img, 0)

        # Convert
        img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
        img = np.ascontiguousarray(img)

        return sources, img, img0, None, stream_infos






        
        
