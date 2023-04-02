
class DetectionResult:
    def __init__(self, class_id, name, xyxy, center_w_h, confident):
        self.class_id = class_id
        self.name = name #object name
        self.xyxy = xyxy # list with 4 elements: from_x, from_y, to_x, to_y
        self.center_w_h = center_w_h # list with 4 elements: center_x, center_y, width, height
        self.confident = confident # confident score
