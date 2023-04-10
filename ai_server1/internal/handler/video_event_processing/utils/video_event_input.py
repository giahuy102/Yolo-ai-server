
class VideoEventInput:
    def __init__(self, event_id, event_key, video_url, start_time, end_time, target_time, detection_image_url=None, line_coords=None):
        self.event_id = event_id
        self.event_key = event_key
        self.video_url = video_url
        self.start_time = start_time
        self.end_time = end_time
        self.target_time = target_time
        self.detection_image_url = detection_image_url
        # self.detection_video_url = detection_video_url
        self.line_coords = line_coords
