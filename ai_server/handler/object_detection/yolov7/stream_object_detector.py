import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel




from yolo_stream_loader import YOLOStreamLoader


class StreamObjectDetector:
    
    def __init__(self, stream_loader, save_dir=Path(__file__).parents[3] / 'static' / 'detection', weight_dir=Path(__file__).parents[3] / 'pkg' / 'object_detection' / 'yolov7' / ''):

        self.yolo_stream_loader = YOLOStreamLoader(stream_loader)

        # Generate saving directory
        self.save_dir = save_dir
        self.save_img_dir = self.save_dir / 'image'
        self.save_video_dir = self.save_dir / 'video'
        self.save_img_dir.mkdir(parents=True, exist_ok=True)
        self.save_video_dir.mkdir(parents=True, exist_ok=True)


        self.weight_dir = weight_dir





    def detect(self, trace=False, device='', model='yolov7.pt', imgsz=640):
        


        # Initialize
        set_logging()
        device = select_device(device)
        half = device.type != 'cpu'  # half precision only supported on CUDA


        # Load model
        model = attempt_load(str(self.weight_dir / model), map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check img_size


        if trace:
            model = TracedModel(model, device, imgsz)

        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()





        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        

    

        


