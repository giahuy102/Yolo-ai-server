import os
import cv2
from threading import Thread, Lock
import time
import re




class StreamLoader:  # multiple IP or RTSP cameras
    def __init__(self, stream_infos):
        


        n = len(stream_infos)
        self.stream_infos = dict()
        for info in stream_infos:
            self.stream_infos[info.stream_id] = info
        self.frames = [None] * n

        for info in self.stream_infos:
            info.rtsp_url = self.clean_url_stream(info.rtsp_url)

        for key, info in self.stream_infos.items():
            # Start the thread to read frames from the video stream
            url = eval(info.rtsp_stream) if info.rtsp_stream.isnumeric() else info.rtsp_stream
            cap = cv2.VideoCapture(url)
            assert cap.isOpened(), f'Failed to open {s}'
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = cap.get(cv2.CAP_PROP_FPS) % 100

            _, self.frames[key] = cap.read()  # guarantee first frame
            thread = Thread(target=self.update, args=([key, cap]), daemon=True)
            print(f' success ({w}x{h} at {self.fps:.2f} FPS).')
            thread.start()
        print('')  # newline

        # check for common shapes
        s = np.stack([letterbox(x, self.img_size, stride=self.stride)[0].shape for x in self.imgs], 0)  # shapes
        self.rect = np.unique(s, axis=0).shape[0] == 1  # rect inference if all shapes equal
        if not self.rect:
            print('WARNING: Different stream shapes detected. For optimal performance supply similarly-shaped streams.')

    def clean_url_stream(self, s):
        return re.sub(pattern="[|@#!¡·$€%&()=?¿^*;:,¨´><+]", repl="_", string=s)


    def add_stream(self, info, stream_id):
        if stream_id not in self.stream_infos:
            self.stream_infos[stream_id] = info
            self.frames[stream_id] = None

    

    def remove_stream(self, stream_id):

        del self.stream_infos[stream_id]
        del self.frames[stream_id]


    def get_frames(self):
        return self.frames
    
    def get_stream_infos(self):
        return self.stream_infos


    def update(self, key, cap):
        # Read next stream frame in a daemon thread
        n = 0
        while cap.isOpened():
            n += 1
            # _, self.imgs[index] = cap.read()
            cap.grab()
            if n == 4:  # read every 4th frame
                success, im = cap.retrieve()
                self.frames[key] = im if success else self.frames[key] * 0
                n = 0
            time.sleep(1 / self.fps)  # wait time

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        img0 = self.imgs.copy()
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

        return self.sources, img, img0, None

    def __len__(self):
        return 0  # 1E12 frames = 32 streams at 30 FPS for 30 years
