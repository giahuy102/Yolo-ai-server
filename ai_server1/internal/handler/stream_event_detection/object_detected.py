from ..object_detection.yolov7.utils.labels import Labels


class ObjectDetected:

    def execute(manager, detection_results, callback):
        found = False
        for res in detection_results.results:
            if res.class_id == Labels.PERSON:
                found = True
        if found:
            manager.process_event_output(detection_results, callback)
