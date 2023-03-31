
class DetectionResult:
    def __init__(self, class_id, name, xyxy, center_w_h, confident, frame, frame_with_box, cur_time, img_frame_info=None):
        self.class_id = class_id
        self.name = name #object name
        self.xyxy = xyxy # list with 4 elements: from_x, from_y, to_x, to_y
        self.center_w_h = center_w_h # list with 4 elements: center_x, center_y, width, height
        self.confident = confident # confident score
        self.img_frame = frame
        self.img_frame_with_box = frame_with_box

        self.cur_time = cur_time

        self.img_frame_info = img_frame_info # stream info when detection object is stream
