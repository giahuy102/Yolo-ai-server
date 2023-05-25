from pathlib import Path

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

    def update(self, xywhs, confss, img_frame):
        outputs = self.deepsort.update(xywhs, confss, img_frame)
        self.identities = outputs[:, -1]
    
    def get_identities(self):
        return self.identities

