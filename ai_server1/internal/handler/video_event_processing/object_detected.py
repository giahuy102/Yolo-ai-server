# from multiprocessing import Event
# import cv2
# from pathlib import Path
# from dateutil.parser import parse


# # import sys
# # pp = Path(__file__).parents[1] / 'object_detection' / 'yolov7'
# # sys.path.insert(0, str(pp))




# from ...pkg.config.config import config

# from ...utils.random_generator import RandomGenerator

# from ..object_detection.yolov7.detection_video import DetectionVideo
# from ..object_detection.yolov7.object_detector import ObjectDetector

# from ...entity.event.event_processing.event_processing_output import EventProcessingOutput



# server_config = config["server"]["http"]
# static_config = config["static"]
# path_config = static_config["path"]
# root_path = str(Path(__file__).parents[2])






# from ...delivery.rabbitmq.producer import Producer
# from ...entity.rabbitmq.exchange import Exchange
# from ...entity.rabbitmq.queue import Queue
# import json





# import os


# class ObjectDetected:
    



#     def callback_stream(self, detection_results, cap=None):
#         for res in detection_results:
#             print(res.name, end=" ")
#             if res.name == "person":
#                 event_output = {
#                     'event_key': 'movement',
#                     'event_time': res.cur_time,
#                     'message': "Movement detected"
#                 }
#                 producer = Producer(Exchange("stream_processing"), Queue("camera_event", ["event.camera.*"]))
#                 producer.produce_message("stream_processing", "event.camera.movement", json.dumps(event_output, indent=4))
#                 break
#         print("")




#     def callback_video(self, detection_results, cap=None): # cap use for stream --> Need to refactor this code

#         video_cap = self.detection_video.cap
#         timestamp_ms = video_cap.get(cv2.CAP_PROP_POS_MSEC)

#         for res in detection_results:
#             if res.name == "person":
#                 self.true_alarm = True
#                 if abs(timestamp_ms - self.target_timestamp_ms) < self.detection_delta_timestamp_ms:
#                     self.img_frame = res.img_frame
#                     self.img_frame_with_box = res.img_frame_with_box
#                     self.detection_delta_timestamp_ms = abs(timestamp_ms - self.target_timestamp_ms)
            
#                 break
            
#         if not self.true_alarm and abs(timestamp_ms - self.target_timestamp_ms) < self.normal_delta_timestamp_ms:
#             self.img_frame = res.img_frame
#             self.img_frame_with_box = res.img_frame_with_box
#             self.normal_delta_timestamp_ms = abs(timestamp_ms - self.target_timestamp_ms)


#         print("Shape ", res.img_frame_with_box.shape)
#         self.video_writer.write(res.img_frame_with_box)


            


#     def execute_video(self, event_input):


#         self.event_input = event_input
#         self.detection_video = DetectionVideo([event_input.video_url])


#         video_extension = Path(self.event_input.video_url).suffix
#         general_image_file = path_config["general_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
#         detection_image_file = path_config["detection_image"] + '/' + RandomGenerator.gen_file_name() + ".jpg"
#         detection_video_file = path_config["detection_video"] + '/' + RandomGenerator.gen_file_name() + video_extension
#         self.general_image_path = root_path + general_image_file
#         self.detection_image_path = root_path + detection_image_file
#         self.detection_video_path = root_path + detection_video_file




#         os.makedirs(root_path + path_config["general_image"], exist_ok=True)
#         os.makedirs(root_path + path_config["detection_image"], exist_ok=True)
#         os.makedirs(root_path + path_config["detection_video"], exist_ok=True)



#         video_cap = self.detection_video.cap
#         fps = video_cap.get(cv2.CAP_PROP_FPS)
#         w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         self.video_writer = cv2.VideoWriter(self.detection_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

#         print("Width ", w)
#         print("Height ", h)


#         self.start_time = parse(event_input.start_time)
#         self.end_time = parse(event_input.end_time)
#         self.target_time = parse(event_input.target_time)
#         self.target_timestamp_ms = (self.target_time - self.start_time).total_seconds() * (10 ** 3)
#         self.threshold = 2000 # threshold in milliseconds



#         self.img_frame = None
#         self.img_frame_with_box = None
#         self.detection_delta_timestamp_ms = float('inf')
#         self.normal_delta_timestamp_ms = float('inf')
#         self.true_alarm = False



#         detector = ObjectDetector()
#         detector.detect(self.detection_video, self.callback_video)


#         cv2.imwrite(self.general_image_path, self.img_frame)
#         # if self.img_frame_with_box:
#         #     cv2.imwrite(self.detection_image_path, self.img_frame_with_box)

#         cv2.imwrite(self.detection_image_path, self.img_frame_with_box)

        

#         host = f"{server_config['protocol']}://{server_config['host']}:{server_config['port']}"
#         image_url = f"{host}{general_image_file}"
#         detection_image_url = f"{host}{detection_image_file}"
#         detection_video_url = f"{host}{detection_video_file}"
#         true_alarm = self.true_alarm

        

#         event_output = EventProcessingOutput(event_input.event_id, image_url, event_input.video_url, detection_image_url, detection_video_url, true_alarm)
        
        

#         producer = Producer(Exchange("event_processing"), Queue("event_verified", ["event.verified.camera.*"]))
#         producer.produce_message("event_processing", "event.verified.camera.movement", event_output.to_json())




import cv2

from ..object_detection.yolov7.utils.labels import Labels

class ObjectDetected:
    
    def execute(self, manager, detection_results):
        video_cap = manager.detection_video.cap
        timestamp_ms = video_cap.get(cv2.CAP_PROP_POS_MSEC)

        for res in detection_results:
            if res.class_id == Labels.PERSON:
                manager.true_alarm = True
                if abs(timestamp_ms - manager.target_timestamp_ms) < manager.detection_delta_timestamp_ms:
                    manager.img_frame = detection_results.img_frame
                    manager.img_frame_with_box = detection_results.img_frame_with_box
                    manager.detection_delta_timestamp_ms = abs(timestamp_ms - manager.target_timestamp_ms)
                break

        if not manager.true_alarm and abs(timestamp_ms - manager.target_timestamp_ms) < manager.normal_delta_timestamp_ms:
            manager.img_frame = detection_results.img_frame
            manager.img_frame_with_box = detection_results.img_frame_with_box
            manager.normal_delta_timestamp_ms = abs(timestamp_ms - manager.target_timestamp_ms)

        manager.video_writer.write(detection_results.img_frame_with_box)
