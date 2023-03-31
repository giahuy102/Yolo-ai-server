import json

class StreamEventOutput:
    def __init__(self, event_key, event_time, detection_image_url, detection_video_url):
        self.event_key = event_key
        self.event_time = event_time
        self.detection_image_url = detection_image_url
        self.detection_video_url = detection_video_url

    def to_json(self):
        data = {
            "event_key": self.event_key,
            "event_time": self.event_time,
            "detection_image_url": self.detection_image_url,
            "detection_video_url": self.detection_video_url
        }
        return json.dumps(data, indent=4)
