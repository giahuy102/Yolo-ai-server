import os
import cv2
from threading import Thread, Lock
import time
import re
import copy
import logging

from ..object_detection.yolov7.utils.threading_condition import stream_condition

class StreamLoader:  # multiple IP or RTSP cameras

    _instance = None
    _singleton_lock = Lock()

    @staticmethod
    def get_instance(stream_infos=list()):
        with StreamLoader._singleton_lock:
            if not StreamLoader._instance:
                StreamLoader(stream_infos)
            return StreamLoader._instance

    def __init__(self, stream_infos=list()): # let stream_infos a defautl argument for easy to use singleton pattern for multiple time
        
        if StreamLoader._instance != None:
            raise Exception("This class is a singleton! Please access from get_instance method")
        StreamLoader._instance = self
        


        self.infos_lock = Lock()

        n = len(stream_infos)
        self.stream_infos = dict()
        self.frames = dict()
        for info in stream_infos:
            self.stream_infos[info.stream_id] = info
            self.frames[info.stream_id] = None

        # for info in self.stream_infos.values():
        #     info.rtsp_url = self.clean_url_stream(info.rtsp_url)

        self.just_updated_infos = True

        for key, info in self.stream_infos.items():
            self.consume_new_stream(key, info)
        print('')  # newline

            # check for common shapes
            # s = np.stack([letterbox(x, self.img_size, stride=self.stride)[0].shape for x in self.imgs], 0)  # shapes
            # self.rect = np.unique(s, axis=0).shape[0] == 1  # rect inference if all shapes equal
            # if not self.rect:
            #     print('WARNING: Different stream shapes detected. For optimal performance supply similarly-shaped streams.')

    def consume_new_stream(self, key, info):
        # Start the thread to read frames from the video stream
        # url = eval(info.rtsp_stream) if info.rtsp_stream.isnumeric() else info.rtsp_stream
        url = info.rtsp_url
        cap = cv2.VideoCapture(url)

        if not cap.isOpened():
            raise Exception(f"Failed to open {url} for detection")

        # assert cap.isOpened(), f'Failed to open {url}'
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS) % 100 # suppose all streams have same fps

        _, self.frames[key] = cap.read()  # guarantee first frame
        thread = Thread(target=self.update, args=([key, cap]), daemon=True)
        logging.info(f' success ({w}x{h} at {self.fps:.2f} FPS).')
        thread.start()



    # def clean_url_stream(self, s):
    #     return re.sub(pattern="[|@#!¡·$€%&()=?¿^*;:,¨´><+]", repl="_", string=s)


    def add_stream(self, stream_id, info):
        try:
            need_notify = False

            self.infos_lock.acquire()
            if stream_id not in self.stream_infos:
                self.stream_infos[stream_id] = info
                self.frames[stream_id] = None

                self.consume_new_stream(stream_id, info)

                self.just_updated_infos = True

                if len(self.stream_infos) == 1:
                    need_notify = True

            if need_notify:
                logging.info("Notify to all threads which is waiting for incoming streams") 
                with stream_condition:
                    stream_condition.notify_all()

        except Exception as e:
            raise e
        else:
            logging.info(f"Add new stream {stream_id} successfully for detection")
        finally:
            self.infos_lock.release()

    
    def remove_stream(self, stream_id):
        try:
            self.infos_lock.acquire()

            if stream_id in self.stream_infos:
                del self.stream_infos[stream_id]
                del self.frames[stream_id]

            self.just_updated_infos = True
        except Exception as e:
            raise e
        else:
            logging.info(f"Remove stream {stream_id} successfully from detection")
        finally:
            self.infos_lock.release()

    def update_stream(self, old_stream_id, info):
        try:
            self.infos_lock.acquire()

            if old_stream_id in self.stream_infos:
                old_info = self.stream_infos[old_stream_id]

                del self.stream_infos[old_stream_id]
                del self.frames[old_stream_id]
                self.stream_infos[info.stream_id] = info
                self.frames[info.stream_id] = None
                if old_info.rtsp_url != info.rtsp_url:
                    self.consume_new_stream(info.stream_id, info)
                    self.just_updated_infos = True
        except Exception as e:
            raise e
        else:
            logging.info(f"Update stream {old_stream_id} successfully for detection")
        finally:
            self.infos_lock.release()


    def get_streams(self):
        """
            Return array of results
        """
        self.infos_lock.acquire()

        stream_infos = copy.deepcopy(list(self.stream_infos.values()))
        frames = copy.deepcopy(list(self.frames.values()))

        just_update_infos = self.just_updated_infos
        self.just_updated_infos = False
        
        self.infos_lock.release()
        return stream_infos, frames, just_update_infos

        


    def get_frames(self):
        return self.frames
    
    def get_stream_infos(self):
        return self.stream_infos


    def update(self, key, cap):
        # Read next stream frame in a daemon thread
        n = 0
        original_url = self.stream_infos[key].rtsp_url
        while cap.isOpened():
            n += 1
            # _, self.imgs[index] = cap.read()
            cap.grab()
            if n == 4:  # read every 4th frame
                self.infos_lock.acquire()
                if key not in self.stream_infos or self.stream_infos[key].rtsp_url != original_url: 
                    self.infos_lock.release()
                    break
                success, im = cap.retrieve()
                self.frames[key] = im if success else self.frames[key] * 0
                self.infos_lock.release()
                n = 0
            time.sleep(1 / self.fps)  # wait time
        else:
            self.remove_stream(key)
        cap.release()
        logging.info(f"Remove stream {key} from detection because of closed stream")

    # def __iter__(self):
    #     self.count = -1
    #     return self

    # def __next__(self):
    #     self.count += 1
    #     img0 = self.imgs.copy()
    #     if cv2.waitKey(1) == ord('q'):  # q to quit
    #         cv2.destroyAllWindows()
    #         raise StopIteration

    #     # Letterbox
    #     img = [letterbox(x, self.img_size, auto=self.rect, stride=self.stride)[0] for x in img0]

    #     # Stack
    #     img = np.stack(img, 0)

    #     # Convert
    #     img = img[:, :, :, ::-1].transpose(0, 3, 1, 2)  # BGR to RGB, to bsx3x416x416
    #     img = np.ascontiguousarray(img)

    #     return self.sources, img, img0, None

    # def __len__(self):
    #     return 0  # 1E12 frames = 32 streams at 30 FPS for 30 years
