import numpy as np
from numpy.linalg import norm
import math
from numpy import linalg as LA
import cv2

from ....pkg.config.config import config

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
LINE_CROSSING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["line_crossing"]

class LineCrossingUtils:

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])
        return A, B, -C

    # Calcuate the coordination of intersect point of line segments - 線分同士が交差する座標を計算
    def calcIntersectPoint(self, line1p1, line1p2, line2p1, line2p2):
        L1 = self.line(line1p1, line1p2)
        L2 = self.line(line2p1, line2p2)
        D  = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        x = Dx / D
        y = Dy / D
        return x, y

    # Check if line segments intersect - 線分同士が交差するかどうかチェック
    def checkIntersect(self, p1, p2, p3, p4):
        tc1 = (p1[0] - p2[0]) * (p3[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p3[0])
        tc2 = (p1[0] - p2[0]) * (p4[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p4[0])
        td1 = (p3[0] - p4[0]) * (p1[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p1[0])
        td2 = (p3[0] - p4[0]) * (p2[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p2[0])
        return tc1 * tc2 < 0 and td1 * td2 < 0

    # convert a line to a vector
    # line(point1)-(point2)
    def line_vectorize(self, point1, point2):
        a = point2[0] - point1[0]
        b = point2[1] - point1[1]
        return [a, b]

    def calcAngle(self, ptrace1, ptrace2, pline_crossing1, pline_crossing2):
        vector_1 = self.line_vectorize(ptrace1, ptrace2)
        vector_2 = self.line_vectorize(pline_crossing1, pline_crossing2)
        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)

        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)

        dot_product = np.dot(unit_vector_1, unit_vector_2)

        angle = np.arccos(dot_product)

        degree = angle * (180 / math.pi)
        return degree


    def checkLineCross(self, trajectory, line, line_crossing_vector):
        pline1 = (line[0], line[1])
        pline2 = (line[2], line[3])
        ptrace1 = (trajectory[0], trajectory[1])
        ptrace2 = (trajectory[2], trajectory[3])
        is_intersect = self.checkIntersect(ptrace1, ptrace2, pline1, pline2)
        in_track_direction = True
        if line_crossing_vector != None and len(line_crossing_vector) > 0:
            pline_crossing1 = (line_crossing_vector[0], line_crossing_vector[1])
            pline_crossing2 = (line_crossing_vector[2], line_crossing_vector[3])
            degree = self.calcAngle(ptrace1, ptrace2, pline_crossing1, pline_crossing2)
            if degree <= 90:
                in_track_direction = True
            else:
                in_track_direction = False
        return is_intersect and in_track_direction

    def exist_line_crossing_in_trajectories(self, trajectories, line, line_crossing_vector):
        line_cross = False
        for track_id in trajectories:
            trajectory = trajectories[track_id]
            if len(trajectory) > 1:
                for i in range(1, len(trajectory)):
                    start = trajectory[i - 1]
                    end = trajectory[i]
                    line_cross = line_cross or self.checkLineCross((start[0], start[1], end[0], end[1]), line, line_crossing_vector)
        return line_cross

    def exist_object_near_line(self, detection_results, line):
        [from_x, from_y, to_x, to_y] = line
        pline_from = np.array([from_x, from_y])
        pline_to = np.array([to_x, to_y])
        for res in detection_results.results:
            p_center = np.array([res.xywh[0], res.xywh[1]])
            distance = norm(np.cross(pline_to - pline_from, pline_from - p_center)) / norm(pline_to - pline_from)
            if distance <= LINE_CROSSING_EVENT_CONFIG["crossing_distance_threshold"]:
                return True
        return False

    def draw_event_utils(self, img, line, line_crossing_vector):
        cv2.line(img, (int(line[0]), int(line[1])), (int(line[2]), int(line[3])), (61, 31, 209), thickness=2)
        if line_crossing_vector and len(line_crossing_vector) > 0:
            cv2.arrowedLine(img, (int(line_crossing_vector[0]), int(line_crossing_vector[1])), (int(line_crossing_vector[2]), int(line_crossing_vector[3])), (61, 31, 209), thickness=2)
