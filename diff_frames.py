import cv2
import numpy as np


def different_frames(previous_frame, image):
    if previous_frame is None:
        return True

    _diff = cv2.absdiff(previous_frame, image)
    diff = np.sum(_diff) / \
        previous_frame.shape[0] / previous_frame.shape[1] / 3.

    return diff > 0.1
