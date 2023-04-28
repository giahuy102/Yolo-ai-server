import cv2
import os
from pathlib import Path
from ...rtsp_stream.stream_loader import StreamLoader
from .....pkg.config.config import config
from ...object_detection.yolov7.utils.detection_stream import DetectionStream
from ....utils.random_generator import RandomGenerator
from .stream_event_output import StreamEventOutput

ROOT_INDEX = 4
SERVER_CONFIG = config["server"]["http"]
STATIC_CONFIG = config["static"]
PATH_CONFIG = STATIC_CONFIG["path"]
ROOT_PATH = str(Path(__file__).parents[ROOT_INDEX])

class StreamEventManager:
    
    def process_stream_loader(self, event_input):
        self.stream_loader = StreamLoader.get_instance(event_input.stream_infos)
        return self

    def process_detection_stream(self):
        self.detection_stream = DetectionStream(self.stream_loader)
        return self

    def process_directory(self):
        os.makedirs(ROOT_PATH + PATH_CONFIG["general_image"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["detection_image"], exist_ok=True)
        return self

    def set_callback_output(self, callback_output):
        self.callback_output = callback_output
        return self

    def gen_image_names(self):
        general_image_name = RandomGenerator.gen_file_name() + ".jpg"
        detection_image_name = RandomGenerator.gen_file_name() + ".jpg"
        return general_image_name, detection_image_name

    def gen_image_files(self):
        general_image_name, detection_image_name = self.gen_image_names()
        general_image_file = PATH_CONFIG["general_image"] + '/' + general_image_name
        detection_image_file = PATH_CONFIG["detection_image"] + '/' + detection_image_name
        return general_image_file, detection_image_file


    def gen_image_paths(self, general_image_file, detection_image_file):
        general_image_path = ROOT_PATH + general_image_file
        detection_image_path = ROOT_PATH + detection_image_file
        return general_image_path, detection_image_path



    def gen_image_urls(self, general_image_file, detection_image_file):
        host = f"{SERVER_CONFIG['scheme']}://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}"
        general_image_url = f"{host}{general_image_file}"
        detection_image_url = f"{host}{detection_image_file}"
        return general_image_url, detection_image_url

    def save_images(self, general_image_path, detection_image_path, img_frame, img_frame_with_box):
        cv2.imwrite(general_image_path, img_frame)
        cv2.imwrite(detection_image_path, img_frame_with_box)


    def process_event_output(self, detection_results, callback):
        frame_info = detection_results.frame_info
        general_image_file, detection_image_file = self.gen_image_files()
        general_image_path, detection_image_path = self.gen_image_paths(general_image_file, detection_image_file)
        general_image_url, detection_image_url = self.gen_image_urls(general_image_file, detection_image_file)
        self.save_images(general_image_path, detection_image_path, detection_results.img_frame, detection_results.img_frame_with_box)
        event_output = StreamEventOutput(frame_info.camera_id, frame_info.event_key, detection_results.cur_time, general_image_url, detection_image_url, frame_info.line_coords)

        # print("#################")
        # print(frame_info.camera_id)
        # print(frame_info.event_key)
        # print(detection_results.cur_time)
        # print(general_image_url)
        # print(detection_image_url)
        callback(event_output)
