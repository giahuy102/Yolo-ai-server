import json

class StreamEventOutput:
    def __init__(self, camera_id, event_key, event_time, image_url, detection_image_url):
        self.camera_id = camera_id
        self.event_key = event_key
        self.event_time = event_time
        self.image_url = image_url
        self.detection_image_url = detection_image_url

    def to_json(self):
        data = {
            "camera_id": self.camera_id,
            "event_key": self.event_key,
            "event_time": self.event_time,
            "image_url": self.image_url,
            "detection_image_url": self.detection_image_url
        }
        return json.dumps(data, indent=4)
