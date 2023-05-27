import torch
import cv2

from ..object_detection.yolov7.utils.plots import plot_one_box
from ..object_detection.yolov7.utils.labels import Labels

PERSON_THRESHOLD = 0.31
IOT_EVENT_ZONE_LABEL = "Iot event zone"
CAMERA_EVENT_ZONE_LABEL = "Camera event zone"
CAMERA_ZONE_COLOR = [0, 0, 255] # in BGR format
IOT_ZONE_COLOR = [0, 170, 255]
PERSON_COLOR = [255, 0, 0]

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)

def draw_boxes(img, bbox, confidences, obj_names, identities=None, offset=(0, 0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0
        conf = confidences[i]
        obj_name = obj_names[i]
        color = compute_color_for_labels(id)
        label = f'{int(id)} - {obj_name} {conf:.2f}'
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
        cv2.rectangle(
            img, (x1, y1), (x1 + t_size[0] + 3, y1 + t_size[1] + 4), color, -1)
        cv2.putText(img, label, (x1, y1 +
                                t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 2, [255, 255, 255], 2)
    return img





class DetectionUtils:




    def satisfy_person_condition(self, label, confident):
        return confident >= PERSON_THRESHOLD and label == Labels.PERSON

    def in_event_zone(self, center_w_h, zone_coords):
        if not zone_coords:
            return True
        center_x = center_w_h[0]
        center_y = center_w_h[1]
        [from_x, from_y, to_x, to_y] = zone_coords
        return center_x >= from_x and center_x <= to_x and center_y >= from_y and center_y <= to_y

    def get_zone_coords(self, iot_event_zone_coords, camera_event_zone_coords, is_ai_event):
        return camera_event_zone_coords if is_ai_event else iot_event_zone_coords

    def get_zone_label(self, is_ai_event):
        return CAMERA_EVENT_ZONE_LABEL if is_ai_event else IOT_EVENT_ZONE_LABEL

    def get_zone_color(self, is_ai_event):
        return CAMERA_ZONE_COLOR if is_ai_event else IOT_ZONE_COLOR

    def filter_results(self, detection_results, iot_event_zone_coords, camera_event_zone_coords, is_ai_event):
        results = list()
        xywhs = list()
        confss = list()
        zone_coords = self.get_zone_coords(iot_event_zone_coords, camera_event_zone_coords, is_ai_event)

        for i in range(len(detection_results.results)):
            result = detection_results.results[i]
            xywh = detection_results.xywhs[i]
            conf = detection_results.confss[i]

            if self.satisfy_person_condition(result.class_id, result.confident) and self.in_event_zone(result.center_w_h, zone_coords):
                results.append(result)
                xywhs.append(xywh)
                confss.append(conf)

        # For tracking with deepsort
        # xywhs = torch.Tensor(xywhs)
        # confss = torch.Tensor(confss)


        detection_results.results = results
        detection_results.xywhs = xywhs
        detection_results.confss = confss

        return detection_results
        

    def preprocess_frame(self, detection_results, iot_event_zone_coords, camera_event_zone_coords, is_ai_event, tracker, line_crossing_coords=None):

        zone_coords = self.get_zone_coords(iot_event_zone_coords, camera_event_zone_coords, is_ai_event)
        zone_label = self.get_zone_label(is_ai_event)
        zone_color = self.get_zone_color(is_ai_event)
        if zone_coords:
            plot_one_box(zone_coords, detection_results.img_frame_with_box, label=zone_label, color=zone_color, line_thickness=1)



        # for idx, result in enumerate(detection_results.results):
        #     label = f'{result.name} {result.confident:.2f}'
        #     plot_one_box(result.xyxy, detection_results.img_frame_with_box, label=label, color=PERSON_COLOR, line_thickness=2)

        tracker = detection_results.frame_info.tracker
        print("Tracker outputs: ", tracker.get_outputs())
        if len(tracker.get_outputs()) > 0:
            identities = tracker.get_identities()
            bbox_xyxy = tracker.get_bbox_xyxy()
            confidences = tracker.get_confidences()
            obj_names = tracker.get_obj_names()
            draw_boxes(detection_results.img_frame_with_box, bbox_xyxy, confidences, obj_names, identities)



        # for idx, result in enumerate(detection_results.results):
        #     _id = int(identities[idx]) if identities else 0
        #     label = f'ID: {_id} - {result.name} {result.confident:.2f}'
        #     plot_one_box(result.xyxy, detection_results.img_frame_with_box, label=label, color=PERSON_COLOR, line_thickness=2)
