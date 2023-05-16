from ..object_detection.yolov7.utils.plots import plot_one_box
from ..object_detection.yolov7.utils.labels import Labels

PERSON_THRESHOLD = 0.38
IOT_EVENT_ZONE_LABEL = "Iot event zone"
CAMERA_EVENT_ZONE_LABEL = "Camera event zone"
ZONE_COLOR = [0, 0, 255] # in BGR format
PERSON_COLOR = [255, 0, 0]

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

    def preprocess_frame(self, detection_results, iot_event_zone_coords, camera_event_zone_coords, is_ai_event, line_crossing_coords=None):
        if is_ai_event:
            zone_coords = camera_event_zone_coords
            zone_label = IOT_EVENT_ZONE_LABEL
        else:
            zone_coords = iot_event_zone_coords
            zone_label = CAMERA_EVENT_ZONE_LABEL

        if zone_coords:
            plot_one_box(zone_coords, detection_results.img_frame_with_box, label=zone_label, color=ZONE_COLOR, line_thickness=1)

        results = list()
        for result in detection_results.results:
            if self.satisfy_person_condition(result.class_id, result.confident) and self.in_event_zone(result.center_w_h, zone_coords):
                label = f'{result.name} {result.confident:.2f}'
                plot_one_box(result.xyxy, detection_results.img_frame_with_box, label=label, color=PERSON_COLOR, line_thickness=1.5)
                results.append(result)

        detection_results.results = results       
