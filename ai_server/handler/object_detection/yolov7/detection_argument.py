
class DetectionArgument:
    def __init__(self, img_size=640, stride=32, trace=False, device='', weights='yolov7.pt', augment=False, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic_nms=False):
        self.img_size = img_size
        self.stride = stride
        self.trace = trace
        self.device = device
        self.weights = weights
        self.augment = augment
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.classes = classes
        self.agnostic_nms = agnostic_nms
