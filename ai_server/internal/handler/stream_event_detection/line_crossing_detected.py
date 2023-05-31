import numpy as np
from numpy.linalg import norm

from ....pkg.config.config import config
from ..object_detection.yolov7.utils.labels import Labels
from .event_detected import EventDetected
from ..event_detection.line_crossing_utils import LineCrossingUtils

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
LINE_CROSSING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["line_crossing"]

class LineCrossingDetected(EventDetected):

    def execute(self, manager, detection_results, callback):
        frame_info = detection_results.frame_info
        continue_process = self.preprocess_frame(manager, detection_results)
        line_crossing_utils = LineCrossingUtils()

        line_crossing_utils.draw_event_utils(detection_results.img_frame_with_box, frame_info.line_coords, frame_info.line_crossing_vector)

        if not continue_process:
            return False


        # found = False
        # info = detection_results.frame_info
        # [from_x, from_y, to_x, to_y] = info.line_coords
        # pline_from = np.array([from_x, from_y])
        # pline_to = np.array([to_x, to_y])
        # for res in detection_results.results:
        #     if res.class_id == Labels.PERSON:
        #         [center_x, center_y, w, h] = res.center_w_h
        #         p_center = np.array([center_x, center_y])
        #         distance = norm(np.cross(pline_to - pline_from, pline_from - p_center)) / norm(pline_to - pline_from)
        #         if distance <= LINE_CROSSING_EVENT_CONFIG["crossing_distance_threshold"]:
        #             found = True
        #             break
        # if found:
        #     manager.process_event_output(detection_results, callback)

        line_crossing_utils = LineCrossingUtils()
        tracker = frame_info.tracker

        crossing_condition = False
        if LINE_CROSSING_EVENT_CONFIG["is_optimistic"]:
            crossing_condition = line_crossing_utils.exist_line_crossing_in_trajectories(tracker.get_current_frame_trajectories(), frame_info.line_coords, frame_info.line_crossing_vector)
        else:
            crossing_condition = line_crossing_utils.exist_object_near_line(detection_results, frame_info.line_coords)
        if crossing_condition:
            manager.process_event_output(detection_results, callback)

        # manager.process_event_output(detection_results, callback)
        
