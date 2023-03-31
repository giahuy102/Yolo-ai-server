from pathlib import Path
import os
import cv2
from dateutil.parser import parse

from ...object_detection.yolov7.utils.detection_video import DetectionVideo
from .....pkg.config.config import config
from ....utils.random_generator import RandomGenerator
from .video_event_output import VideoEventOutput


ROOT_INDEX = 3
SERVER_CONFIG = config["server"]["http"]
STATIC_CONFIG = config["static"]
PATH_CONFIG = STATIC_CONFIG["path"]
ROOT_PATH = str(Path(__file__).parents[ROOT_INDEX])


class VideoEventManager:

    def process_video(self, event_input):
        self.event_input = event_input
        video_url = event_input.video_url
        self.detection_video = DetectionVideo(video_url)

    def process_path(self):
        video_extension = Path(self.event_input.video_url).suffix
        self.general_image_file = PATH_CONFIG["general_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
        self.detection_image_file = PATH_CONFIG["detection_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
        self.detection_video_file = PATH_CONFIG["detection_video"] + '/' + RandomGenerator.gen_file_name() + video_extension
        self.general_image_path = ROOT_PATH + self.general_image_file
        self.detection_image_path = ROOT_PATH + self.detection_image_file
        self.detection_video_path = ROOT_PATH + self.detection_video_file

    def process_directory(self):
        os.makedirs(ROOT_PATH + PATH_CONFIG["general_image"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["detection_image"], exist_ok=True)
        os.makedirs(ROOT_PATH + PATH_CONFIG["detection_video"], exist_ok=True)

    def process_video_writer(self):
        video_cap = self.detection_video.cap
        fps = video_cap.get(cv2.CAP_PROP_FPS)
        w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_writer = cv2.VideoWriter(self.detection_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))


    def process_initial_event_data(self, event_input):
        self.is_ai_event = False
        if event_input.is_ai_event:
            self.is_ai_event = True
        self.start_time = parse(event_input.start_time)
        self.end_time = parse(event_input.end_time)
        self.target_time = parse(event_input.target_time)
        self.target_timestamp_ms = (self.target_time - self.start_time).total_seconds() * (10 ** 3)

        self.video_url = event_input.video_url
        self.detection_image_url = event_input.detection_image_url
        self.detection_video_url = event_input.detection_video_url

    def process_initial_detection_data(self):
        self.img_frame = None
        self.img_frame_with_box = None
        self.detection_delta_timestamp_ms = float('inf')
        self.normal_delta_timestamp_ms = float('inf')
        self.true_alarm = False

    def process_save_images(self):
        cv2.imwrite(self.general_image_path, self.img_frame)
        cv2.imwrite(self.detection_image_path, self.img_frame_with_box)

    def process_event_output(self):
        self.host = f"{SERVER_CONFIG['scheme']}://{SERVER_CONFIG['host']}:{SERVER_CONFIG['port']}"
        self.image_url = f"{self.host}{self.general_image_file}"

        if self.is_ai_event: 
            # pertimistic trategy
            # detection_image_url and detection_video_url have been assigned in the initial method
            if self.true_alarm:
                self.detection_image_url = f"{self.host}{self.detection_image_file}"
                self.detection_video_url = f"{self.host}{self.detection_video_file}"                
            self.true_alarm = True
        else:
            self.detection_image_url = f"{self.host}{self.detection_image_file}"
            self.detection_video_url = f"{self.host}{self.detection_video_file}"


    def get_event_output(self):
        return VideoEventOutput(self.event_input.event_id, self.image_url, self.video_url, self.detection_image_url, self.detection_video_url, self.true_alarm)
