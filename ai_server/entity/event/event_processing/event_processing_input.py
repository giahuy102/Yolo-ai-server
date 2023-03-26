
class EventProcessingInput:
    def __init__(self, event_id, video_url, start_time, end_time, target_time, specific_detail=None):
        
        self.event_id = event_id
        self.video_url = video_url
        self.start_time = start_time
        self.end_time = end_time
        self.target_time = target_time

        self.specific_detail = specific_detail # dictionary for specific event detail (Ex: Line crossing need additional points)