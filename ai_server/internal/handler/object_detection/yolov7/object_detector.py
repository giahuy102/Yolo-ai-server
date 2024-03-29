import time
from datetime import datetime
import pytz
from pathlib import Path
import logging

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



from utils.detection_stream import DetectionStream
from utils.detection_argument import DetectionArgument

from utils.detection_result import DetectionResult
from utils.detection_results import DetectionResults

from utils.labels import Labels

from .model_loader import ModelLoader

PERSON_THRESHOLD = 0.38
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')

class ObjectDetector:

    def satisfy_person_condition(self, label, confident):
        return confident >= PERSON_THRESHOLD and label == Labels.PERSON


    def xyxy_to_xywh(self, *xyxy):
        """" Calculates the relative bounding box from absolute pixel values. """
        bbox_left = min([xyxy[0].item(), xyxy[2].item()])
        bbox_top = min([xyxy[1].item(), xyxy[3].item()])
        bbox_w = abs(xyxy[0].item() - xyxy[2].item())
        bbox_h = abs(xyxy[1].item() - xyxy[3].item())
        x_c = (bbox_left + bbox_w / 2)
        y_c = (bbox_top + bbox_h / 2)
        w = bbox_w
        h = bbox_h
        return x_c, y_c, w, h





    def detect(self, detection_object, callback, opt=DetectionArgument()):  

        # print(str(opt.weight_dir / opt.weights))
        # print((opt.weight_dir / opt.weights).exists())




        # # Initialize
        # set_logging()
        # device = select_device(opt.device)
        # half = device.type != 'cpu'  # half precision only supported on CUDA

        # # Load model
        # model = attempt_load(str(opt.weight_dir / opt.weights), map_location=device)  # load FP32 model
        
        
        
        # stride = int(model.stride.max())  # model stride
        # imgsz = check_img_size(opt.img_size, s=stride)  # check img_size

        # if opt.trace:
        #     model = TracedModel(model, device, opt.img_size)

        # if half:
        #     model.half()  # to FP16

        # # Second-stage classifier
        # classify = False
        # if classify:
        #     modelc = load_classifier(name='resnet101', n=2)  # initialize
        #     modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()



        # # Get names and colors
        # names = model.module.names if hasattr(model, 'module') else model.names
        # colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # # Run inference
        # if device.type != 'cpu':
        #     model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        
        
        
        model_loader = ModelLoader.get_instance()
        model = model_loader.get_model()
        device = model_loader.get_device()
        imgsz = model_loader.get_imgsz()
        names = model_loader.get_names()
        colors = model_loader.get_colors()
        half = model_loader.get_half()
        classify = model_loader.get_classify()
        modelc = model_loader.get_modelc()


        
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap, info, success in detection_object:
            if success:
                img = torch.from_numpy(img).to(device)
                img = img.half() if half else img.float()  # uint8 to fp16/32
                img /= 255.0  # 0 - 255 to 0.0 - 1.0
                if img.ndimension() == 3:
                    img = img.unsqueeze(0)

                # Warmup
                if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                    old_img_b = img.shape[0]
                    old_img_h = img.shape[2]
                    old_img_w = img.shape[3]
                    for i in range(3):
                        model(img, augment=opt.augment)[0]

                # Inference
                t1 = time_synchronized()
                with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
                    pred = model(img, augment=opt.augment)[0]
                t2 = time_synchronized()

                # Apply NMS
                pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
                t3 = time_synchronized()

                # Apply Classifier
                if classify:
                    pred = apply_classifier(pred, modelc, img, im0s)

                # Process detections
                for i, det in enumerate(pred):  # detections per image
                    # if detection_object.mode == 'stream':
                    #     p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), detection_object.count
                    # else:
                    #     p, s, im0, frame = path, '', im0s, getattr(detection_object, 'frame', 0)

                    if detection_object.mode == 'stream':
                        p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                        
                        finfo = info[i]

                    else:
                        p, s, im0 = path, '', im0s
                        finfo = info
                    

                    p = Path(p)  # to Path
                    
                    # Write results
                    detection_results = list()
                    img_frame = np.copy(im0)
                    cur_time = datetime.now(TIMEZONE).isoformat()


                    # xywhs = []
                    # confss = []

                    if len(det):
                        # Rescale boxes from img_size to im0 size
                        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()





                        for *xyxy, conf, cls in reversed(det):

                            # For tracking with deepsort
                            x_c, y_c, bbox_w, bbox_h = self.xyxy_to_xywh(*xyxy)
                            xywh_obj = [x_c, y_c, bbox_w, bbox_h]
                            # xywhs.append(xywh_obj)
                            # confss.append([conf.item()])


                            
                            class_name = names[int(cls)]
                            xyxy = list(map(lambda x: float(x), xyxy))
                            center_w_h = xyxy2xywh(torch.tensor(xyxy).view(1, 4))[0].tolist()
                            confident = conf.item()

                            # if self.satisfy_person_condition(int(cls), confident):

                            #     label = f'{names[int(cls)]} {conf:.2f}'
                            #     plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

                                
                            #     detection_results.append(DetectionResult(int(cls), class_name, xyxy, center_w_h, confident))

                            
                            detection_results.append(DetectionResult(int(cls), class_name, xyxy, center_w_h, confident, xywh_obj))

                        # # For tracking with deepsort
                        # xywhs = torch.Tensor(xywhs)
                        # confss = torch.Tensor(confss)
                    img_frame_with_box = im0
                    callback(DetectionResults(detection_results, img_frame, img_frame_with_box, cur_time, finfo, vid_cap, names))

                    # Print time (inference + NMS)
                    logging.info(f'{"Stream#" + s + " " if s else s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')


                # is stream detection
                if not vid_cap:
                    access_frame_lock = detection_object.get_access_detection_frame_condition()
                    try:
                        with access_frame_lock:
                            access_frame_lock.notify_all()
                    except Exception as e:
                        logging.warn(str(e))



        logging.info(f'Done. ({time.time() - t0:.3f}s)')
