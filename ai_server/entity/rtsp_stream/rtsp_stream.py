
class RTSPStream:
    def __init__(self, camera_id, rtsp_url, event_key, stream_id=None): 
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.event_key = event_key # necessary when we don't communication through broker
        self.stream_id = stream_id if stream_id else self.camera_id
