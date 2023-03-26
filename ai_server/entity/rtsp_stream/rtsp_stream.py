
class RTSPStream:
    def __init__(self, camera_id, rtsp_url, stream_id=None):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.stream_id = stream_id if stream_id else self.camera_id




