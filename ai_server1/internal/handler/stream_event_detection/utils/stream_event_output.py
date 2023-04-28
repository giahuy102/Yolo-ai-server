import json

class StreamEventOutput:
    def __init__(self, camera_id, event_key, event_time, image_url, detection_image_url, line_coords):
        self.camera_id = camera_id
        self.event_key = event_key
        self.event_time = event_time
        self.image_url = image_url
        self.detection_image_url = detection_image_url
        self.line_coords = line_coords

    def to_json(self):
        data = {
            "camera_id": self.camera_id,
            "event_key": self.event_key,
            "event_time": self.event_time,
            "image_url": self.image_url,
            "detection_image_url": self.detection_image_url
        }
        if self.line_coords:
            data["line_coords"] = self.line_coords
        return json.dumps(data, indent=4)
