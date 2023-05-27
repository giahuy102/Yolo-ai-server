from pathlib import Path
import torch

from .deep_sort_pytorch.utils.parser import get_config
from .deep_sort_pytorch.deep_sort import DeepSort

USE_CUDA = False


class Tracker:
    def __init__(self):
        # initialize deepsort
        cfg_deep = get_config()


        


        config_file = Path(__file__).parents[0] / 'deep_sort_pytorch' / 'configs' / 'deep_sort.yaml'

        cfg_deep.merge_from_file(config_file)

        MODEL_CHECK_POINT = str(Path(__file__).parents[0]) + '/' + cfg_deep.DEEPSORT.REID_CKPT

        # attempt_download("deep_sort_pytorch/deep_sort/deep/checkpoint/ckpt.t7", repo='mikel-brostrom/Yolov5_DeepSort_Pytorch')
        self.deepsort = DeepSort(MODEL_CHECK_POINT,
                            max_dist=cfg_deep.DEEPSORT.MAX_DIST, min_confidence=cfg_deep.DEEPSORT.MIN_CONFIDENCE,
                            nms_max_overlap=cfg_deep.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg_deep.DEEPSORT.MAX_IOU_DISTANCE,
                            max_age=cfg_deep.DEEPSORT.MAX_AGE, n_init=cfg_deep.DEEPSORT.N_INIT, nn_budget=cfg_deep.DEEPSORT.NN_BUDGET,
                            use_cuda=USE_CUDA)

    def update(self, xywhs, confss, obj_names, img_frame):
        if len(xywhs) > 0:
            print("Tracker xywhs: ", xywhs)
            xywhs = torch.Tensor(xywhs)
            confss = torch.Tensor(confss)
            outputs = self.deepsort.update(xywhs, confss, obj_names, img_frame)
        else:
            outputs = []
        self.bbox_xyxy = []
        self.identities = []
        self.confidences = []
        self.obj_names = []
        for output in outputs:
            self.bbox_xyxy.append(output[0][:4])
            self.identities.append(output[0][-1])
            self.confidences.append(output[1])
            self.obj_names.append(output[2])
        # self.bbox_xyxy = outputs[:, :4] if len(outputs) > 0 else []
        # self.identities = outputs[:, -1] if len(outputs) > 0 else []
        # self.confidences = outputs[:, -2] if len(outputs) > 0 else []
        self.outputs = outputs

    def get_outputs(self):
        return self.outputs

    def get_bbox_xyxy(self):
        return self.bbox_xyxy

    def get_identities(self):
        return self.identities

    def get_confidences(self):
        return self.confidences

    def get_obj_names(self):
        return self.obj_names
