import threading
import torch
import cv2
import math

from ..object_detection.yolov7.utils.plots import plot_one_box
from ..object_detection.yolov7.utils.labels import Labels

PERSON_THRESHOLD = 0.31
IOT_EVENT_ZONE_LABEL = "Iot event zone"
CAMERA_EVENT_ZONE_LABEL = "Camera event zone"
CAMERA_ZONE_COLOR = [0, 0, 255] # in BGR format
IOT_ZONE_COLOR = [0, 170, 255]
PERSON_COLOR = [255, 0, 0]



palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
"""Function to Get color from tracking ID"""
def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)

#............................... Bounding Boxes Drawing ............................
"""Function to Draw Bounding boxes"""
def draw_boxes(img, bbox, identities=None, categories=None, names=None, offset=(0, 0)):
    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        cat = int(categories[i]) if categories is not None else 0
        id = int(identities[i]) if identities is not None else 0
        data = (int((box[0]+box[2])/2),(int((box[1]+box[3])/2)))
        color = compute_color_for_labels(id)

        if id == 0:
            id = "Unconfirmed ID"

        label = str(id) + ": "+ names[cat]
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, [255, 255, 255], 1)
        # cv2.circle(img, data, 6, color,-1)   #centroid of box
    return img



def draw_trails(img, trajectories):
    for key in trajectories:
        trajectory = trajectories[key]
        for i in range(1, len(trajectory)):
            color = compute_color_for_labels(key)
            cur = trajectory[i]
            prev = trajectory[i - 1]
            cv2.line(img, (int(prev[0]), int(prev[1])), (int(cur[0]), int(cur[1])), color, thickness=2)


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
        zone_coords = self.get_zone_coords(iot_event_zone_coords, camera_event_zone_coords, is_ai_event)

        for i in range(len(detection_results.results)):
            result = detection_results.results[i]

            if self.satisfy_person_condition(result.class_id, result.confident) and self.in_event_zone(result.center_w_h, zone_coords):
                results.append(result)
        detection_results.results = results
        return detection_results
        
    def equal_xyxy(self, result_xyxy, track_xyxy):
        [x, y, z, t] = result_xyxy
        [a, b, c, d] = track_xyxy

        cx = x + abs(z - x) / 2
        cy = y + abs(t - y) / 2
        ca = a + abs(c - a) / 2
        cb = b + abs(d - b) / 2
        threshold = max(abs(z - x), abs(t - y)) / 2
        dis = math.sqrt((cx - ca) ** 2 + (cb - cy) ** 2)
        if dis > threshold:
            return False

        # if abs(x - a) > threshold or abs(y - b) > threshold or abs(z - c) > threshold or abs(t - d) > threshold:
        #     return False
        return True

    def concatenate_unconfirmed_tracking_object(self, detection_results, xyxy_boxes, identities, categories):
        indices = list()
        xyxy_boxes = list(xyxy_boxes)
        identities = list(identities)
        categories = list(categories)
        results = detection_results.results
        for idx, result in enumerate(results):
            found = False
            for box in xyxy_boxes:
                if self.equal_xyxy(result.xyxy, box):
                    found = True
            if not found:
                indices.append(idx)
        for idx in indices:
            xyxy_boxes = xyxy_boxes + [results[idx].xyxy]
            identities = identities + [0]
            categories = categories + [results[idx].class_id]
        return xyxy_boxes, identities, categories


    def preprocess_frame(self, detection_results, iot_event_zone_coords, camera_event_zone_coords, is_ai_event, tracker):
        tracker.update(detection_results)
        zone_coords = self.get_zone_coords(iot_event_zone_coords, camera_event_zone_coords, is_ai_event)
        zone_label = self.get_zone_label(is_ai_event)
        zone_color = self.get_zone_color(is_ai_event)
        if zone_coords:
            plot_one_box(zone_coords, detection_results.img_frame_with_box, label=zone_label, color=zone_color, line_thickness=1)

        print("Length of detection results: ", len(detection_results.results))
        print("Length of tracking objects: ", len(tracker.get_identities()))
        xyxy_boxes = tracker.get_xyxy_boxes()
        identities = tracker.get_identities()
        categories = tracker.get_categories()
        xyxy_boxes, identities, categories = self.concatenate_unconfirmed_tracking_object(detection_results, xyxy_boxes, identities, categories)
        draw_boxes(detection_results.img_frame_with_box, xyxy_boxes, identities, categories, detection_results.names)

        cur_trajectories = tracker.get_current_frame_trajectories()
        print("Trajectories: ", cur_trajectories)
        draw_trails(detection_results.img_frame_with_box, cur_trajectories)
