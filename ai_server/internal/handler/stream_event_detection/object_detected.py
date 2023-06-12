from multiprocessing import Event
from ..object_detection.yolov7.utils.labels import Labels
from .event_detected import EventDetected

class ObjectDetected(EventDetected):

    def execute(self, manager, detection_results, callback):
        if not self.preprocess_frame(manager, detection_results):
            return False
        found = False
        for res in detection_results.results:
            if res.class_id == Labels.PERSON:
                found = True
        if found:
            manager.process_event_output(detection_results, callback)
