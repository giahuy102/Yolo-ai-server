import json

class StreamEventOutput:
    def __init__(self, event_key, event_time, image_url, detection_image_url):
        self.event_key = event_key
        self.event_time = event_time
        self.image_url = image_url
        self.detection_image_url = detection_image_url

    def to_json(self):
        data = {
            "event_key": self.event_key,
            "event_time": self.event_time,
            "image_url": self.image_url,
            "detection_image_url": self.detection_image_url
        }
        return json.dumps(data, indent=4)
