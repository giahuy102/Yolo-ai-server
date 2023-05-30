from pathlib import Path
import os
import cv2
from dateutil.parser import parse
import logging
import requests

from ...object_detection.yolov7.utils.detection_video import DetectionVideo
from .....pkg.config.config import config
from ....utils.random_generator import RandomGenerator
from .video_event_output import VideoEventOutput


ROOT_INDEX = 4
SERVER_CONFIG = config["server"]["http"]
STATIC_CONFIG = config["static"]
PATH_CONFIG = STATIC_CONFIG["path"]
ROOT_PATH = str(Path(__file__).parents[ROOT_INDEX])

EVENT_CONFIG = config["event"]
IOT_EVENT = EVENT_CONFIG["iot"]
CAMERA_EVENT = EVENT_CONFIG["camera"]

TEMP_FILE_STRING = "temporary-"


class VideoEventManager:

    def process_video(self, event_input):
        self.event_input = event_input
        video_url = event_input.video_url
        self.detection_video = DetectionVideo(video_url)
        return self

    def process_path(self, event_input):
        video_extension = '.mp4'
        self.general_image_file = PATH_CONFIG["general_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
        self.detection_image_file = PATH_CONFIG["detection_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
        
        self.general_image_path = ROOT_PATH + self.general_image_file
        self.detection_image_path = ROOT_PATH + self.detection_image_file

        self.detection_video_filename = RandomGenerator.gen_file_name()
        self.detection_video_file = PATH_CONFIG["detection_video"] + '/' + self.detection_video_filename + video_extension
        self.temp_detection_video_file = PATH_CONFIG["detection_video"] + '/' + TEMP_FILE_STRING + self.detection_video_filename + video_extension
        self.detection_video_path = ROOT_PATH + self.temp_detection_video_file

        self.general_video_filename = RandomGenerator.gen_file_name()
        self.general_video_file = PATH_CONFIG["general_video"] + '/' + self.general_video_filename + video_extension
        self.general_video_path = ROOT_PATH + self.general_video_file
        return self

    def process_directory(self):
        os.makedirs(ROOT_PATH + PATH_CONFIG["general_image"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["detection_image"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["detection_video"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["general_video"], exist_ok=True)
        return self

    def process_video_writer(self):
        video_cap = self.detection_video.cap
        fps = video_cap.get(cv2.CAP_PROP_FPS)
        w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_writer = cv2.VideoWriter(self.detection_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
        return self

    def process_download_general_video_file(self):
        print("Downloading video from google drive")
        r = requests.get(self.event_input.video_url, timeout=2000)
        with open(self.general_video_path, 'wb') as f:
            f.write(r.content)
        print("Finish downloading video from google drive")
        return self


    def check_is_ai_event(self, event_key):
        event_with_equal_key = list(filter(lambda e: type(e) is dict and e["key"] == event_key, CAMERA_EVENT.values()))
        return True if event_with_equal_key else False

    def process_initial_event_data(self, event_input):
        self.is_ai_event = self.check_is_ai_event(event_input.event_key)
        self.start_time = parse(event_input.start_time)
        self.end_time = parse(event_input.end_time)
        self.target_time = parse(event_input.target_time)
        self.target_timestamp_ms = (self.target_time - self.start_time).total_seconds() * (10 ** 3)

        self.video_url = event_input.video_url
        self.image_url = event_input.image_url
        self.detection_image_url = event_input.detection_image_url
        self.detection_video_url = self.video_url
        return self

    def process_initial_detection_data(self):
        self.img_frame = None
        self.img_frame_with_box = None
        self.detection_delta_timestamp_ms = float('inf')
        self.normal_delta_timestamp_ms = float('inf')
        self.true_alarm = False
        return self

    def process_save_images(self):
        cv2.imwrite(self.general_image_path, self.img_frame)
        cv2.imwrite(self.detection_image_path, self.img_frame_with_box)
        return self

    def process_event_output(self):
        self.host = f"{SERVER_CONFIG['scheme']}://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}"
    
        self.video_writer.release()

        if self.is_ai_event: 
            # pessimistic trategy
            # detection_image_url and detection_video_url have been assigned in the initial method
            if self.true_alarm:
                self.image_url = f"{self.host}{self.general_image_file}"
                self.detection_image_url = f"{self.host}{self.detection_image_file}"
            self.detection_video_url = f"{self.host}{self.detection_video_file}"                
            self.true_alarm = True
        else:
            self.image_url = f"{self.host}{self.general_image_file}"
            self.detection_image_url = f"{self.host}{self.detection_image_file}"
            self.detection_video_url = f"{self.host}{self.detection_video_file}"

        self.convert_output_video_codec()

        return self

    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            logging.warning(f"File having path {file_path} does not exist but trying to remove")

    def convert_output_video_codec(self):
        temp_path = self.detection_video_path
        # if self.detection_video_url != self.video_url:
        self.detection_video_path = ROOT_PATH + self.detection_video_file
        os.system(f"ffmpeg -loglevel warning -i {temp_path} -vcodec libx264 -f mp4 {self.detection_video_path}")
        self.remove_file(temp_path)

    def process_clear_file(self):
        print("Clear file: ", self.general_video_path)
        self.remove_file(self.general_video_path)
        print("After clear file: ", self.general_video_path)
        return self

    def get_event_output(self):
        print(VideoEventOutput(self.event_input.event_id, self.image_url, self.video_url, self.detection_image_url, self.detection_video_url, self.true_alarm, self.is_ai_event).to_json())
        return VideoEventOutput(self.event_input.event_id, self.image_url, self.video_url, self.detection_image_url, self.detection_video_url, self.true_alarm, self.is_ai_event)


    def set_callback_detection_result(self, callback_detection_result):
        self.callback_detection_result = callback_detection_result


    def update_image_with_nearest_timestamp(self, detection_results):
        video_cap = self.detection_video.cap
        timestamp_ms = video_cap.get(cv2.CAP_PROP_POS_MSEC)
        if self.true_alarm:
            if abs(timestamp_ms - self.target_timestamp_ms) < self.detection_delta_timestamp_ms:
                self.img_frame = detection_results.img_frame
                self.img_frame_with_box = detection_results.img_frame_with_box
                self.detection_delta_timestamp_ms = abs(timestamp_ms - self.target_timestamp_ms)
        else:
            if not self.true_alarm and abs(timestamp_ms - self.target_timestamp_ms) < self.normal_delta_timestamp_ms:
                self.img_frame = detection_results.img_frame
                self.img_frame_with_box = detection_results.img_frame_with_box
                self.normal_delta_timestamp_ms = abs(timestamp_ms - self.target_timestamp_ms)

        self.video_writer.write(detection_results.img_frame_with_box)

