import json

class VideoEventOutput:
    def __init__(self, event_id, image_url, video_url, detection_image_url, detection_video_url, true_alarm, is_ai_event):
        self.event_id = event_id
        self.image_url = image_url
        self.video_url = video_url
        self.detection_image_url = detection_image_url
        self.detection_video_url = detection_video_url
        self.true_alarm = true_alarm
        self.is_ai_event = is_ai_event

    def to_json(self):
        data = {
            "event_id": self.event_id,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "detection_image_url": self.detection_image_url,
            "detection_video_url": self.detection_video_url,
            "true_alarm": self.true_alarm
        }
        return json.dumps(data, indent=4)
