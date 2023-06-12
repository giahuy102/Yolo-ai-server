from .sort import *

class SortTracker:
    def __init__(self):
        #.... Initialize SORT .... 
        #......................... 
        sort_max_age = 5 
        sort_min_hits = 2
        sort_iou_thresh = 0.2
        self.sort_tracker = Sort(max_age=sort_max_age,
                        min_hits=sort_min_hits,
                        iou_threshold=sort_iou_thresh)

        self.trajectories = dict()

    def update(self, detection_results):
        dets_to_sort = np.empty((0,6))
        
        for result in detection_results.results:
            [x1, y1, x2, y2] = result.xyxy
            dets_to_sort = np.vstack((dets_to_sort, 
                        np.array([x1, y1, x2, y2, result.confident, result.class_id])))
        self.tracked_dets = self.sort_tracker.update(dets_to_sort)

        self.filter_trajectories()

    def filter_trajectories(self):
        self.trajectories = dict()
        for tracker in self.sort_tracker.getTrackers():
            self.trajectories[tracker.id + 1] = tracker.centroidarr

    def get_current_frame_trajectories(self):
        active_ids = self.get_identities()
        res = dict()
        for k in self.trajectories:
            if k in active_ids:
                res[k] = self.trajectories[k]
        return res            



    def get_xyxy_boxes(self):
        return self.tracked_dets[:,:4] if len(self.tracked_dets) > 0 else []

    def get_identities(self):
        return self.tracked_dets[:, 8] if len(self.tracked_dets) > 0 else []
    
    def get_categories(self):
        return self.tracked_dets[:, 4] if len(self.tracked_dets) > 0 else []

