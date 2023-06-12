class DetectionResults:
    def __init__(self, results, frame, frame_with_box, cur_time, frame_info, capture, names):
        self.results = results # list of DetectionResult object
        self.img_frame = frame
        self.img_frame_with_box = frame_with_box
        self.cur_time = cur_time
        self.frame_info = frame_info # have RTSPStream class type
        self.capture = capture

        self.names = names

        # # For tracking with deepsort
        # self.xywhs = xywhs
        # self.confss = confss
        