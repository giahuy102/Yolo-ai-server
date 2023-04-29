import time
from datetime import datetime
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np


from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel


from utils.detection_argument import DetectionArgument


class ModelLoader:

    _instance = None

    def __init__(self, opt=DetectionArgument()):
        if ModelLoader._instance != None:
            raise Exception("This class is a singleton! Please access from get_instance method")
        ModelLoader._instance = self
        self.init_model(opt)

    def init_model(self, opt):
        set_logging()
        self.device = select_device(opt.device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(str(opt.weight_dir / opt.weights), map_location=self.device)  # load FP32 model
        
        
        
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(opt.img_size, s=self.stride)  # check img_size

        if opt.trace:
            self.model = TracedModel(self.model, self.device, opt.img_size)

        if self.half:
            self.model.half()  # to FP16

        # Second-stage classifier
        self.classify = False
        self.modelc = None
        if self.classify:
            self.modelc = load_classifier(name='resnet101', n=2)  # initialize
            self.modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()



        # Get names and colors
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once


    def get_model(self):
        return self.model

    def get_device(self):
        return self.device

    def get_imgsz(self):
        return self.imgsz

    def get_names(self):
        return self.names
    
    def get_colors(self):
        return self.colors

    def get_half(self):
        return self.half

    def get_classify(self):
        return self.classify

    def get_modelc(self):
        return self.modelc

    @staticmethod
    def get_instance():
        if ModelLoader._instance == None:
            ModelLoader()
        return ModelLoader._instance
