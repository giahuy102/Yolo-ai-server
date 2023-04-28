import numpy as np
import cv2
import copy

from utils.datasets import letterbox

from .threading_condition import stream_condition


class DetectionStream:
    def __init__(self, stream_loader, img_size=640, stride=32):
        self.mode = 'stream'
        self.stream_loader = stream_loader
        self.img_size = img_size
        self.stride = stride

    def check_common_shape(self, frames):
        # check for common shapes
        s = np.stack([letterbox(x, self.img_size, stride=self.stride)[0].shape for x in frames], 0)  # shapes
        self.rect = np.unique(s, axis=0).shape[0] == 1  # rect inference if all shapes equal
        if not self.rect:
            print('WARNING: Different stream shapes detected. For optimal performance supply similarly-shaped streams.')



    def __iter__(self):
        self.count = -1 # Temporarily not have any usage here
        return self


    def __next__(self):
        


        stream_infos, img0, just_updated_infos = self.stream_loader.get_streams()
        if not stream_infos:
            with stream_condition:
                stream_condition.wait()

        if stream_infos:

            self.count += 1
            if just_updated_infos:
                self.check_common_shape(img0)

            sources = [info.rtsp_url for info in stream_infos]

            # img0 = self.stream_loader.get_frames().copy()
            # stream_infos = copy.deepcopy(list(self.stream_loader.get_stream_infos().values()))
            # sources = [info.rtsp_url for info in stream_infos.values()]



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

            return sources, img, img0, None, stream_infos, True

        else:
            return None, None, None, None, None, False

