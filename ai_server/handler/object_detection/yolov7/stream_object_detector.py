import argparse
from email.policy import default
import time
from pathlib import Path
from collections import defaultdict

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




from detection_stream import DetectionStream
from detection_argument import DetectionArgument


class StreamObjectDetector:

    
    def __init__(self, stream_loader, save_dir=Path(__file__).parents[3] / 'static' / 'detection', weight_dir=Path(__file__).parents[3] / 'pkg' / 'object_detection' / 'yolov7' / ''):

        self.stream_loader = stream_loader
        

        # Generate saving directory
        self.save_dir = save_dir
        self.save_img_dir = self.save_dir / 'image'
        self.save_video_dir = self.save_dir / 'video'
        self.save_img_dir.mkdir(parents=True, exist_ok=True)
        self.save_video_dir.mkdir(parents=True, exist_ok=True)


        self.weight_dir = weight_dir





    def detect(self, opt=DetectionArgument()):

        # Initialize
        set_logging()
        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(str(self.weight_dir / opt.weights), map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(opt.img_size, s=stride)  # check img_size

        if opt.trace:
            model = TracedModel(model, device, opt.img_size)

        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()








        # # Set Dataloader
        # vid_path, vid_writer = None, None
        # if webcam:
        #     view_img = check_imshow()
        #     cudnn.benchmark = True  # set True to speed up constant image size inference
        #     dataset = LoadStreams(source, img_size=imgsz, stride=stride)
        # else:
        #     dataset = LoadImages(source, img_size=imgsz, stride=stride)


        stream_frames = DetectionStream(self.stream_loader, opt.img_size, opt.stride)




        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap, stream_info in stream_frames:
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


                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), stream_frames.count

                p = Path(p)  # to Path



                save_path = str(self.save_dir / p.name)  # img.jpg
                txt_path = str(self.save_dir / 'labels' / p.stem) + ('' if stream_frames.mode == 'image' else f'_{frame}')  # img.txt
                
                
                
                
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Write results
                    detection_result = defaultdict(list)
                    for *xyxy, conf, cls in reversed(det):
                        new_obj = {
                            'xyxy': list(map(lambda x: float(x), xyxy)),
                            'center_w_h': xyxy2xywh(torch.tensor(xyxy).view(1, 4))[0].tolist(),
                            'confident': conf
                        }   
                        detection_result[names[cls]].append(new_obj)             

                # Print time (inference + NMS)
                print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

        print(f'Done. ({time.time() - t0:.3f}s)')

        


