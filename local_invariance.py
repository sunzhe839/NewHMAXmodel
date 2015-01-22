__author__ = 'yuki'
#coding UTF-8

import numpy as np
from filter import Filter


class LocalInvariance(Filter):
    def __init__(self, filter_size, orientations):
        self.filter_size = filter_size
        self.orientations = orientations

    def compute_unit(self, input_layer, scale, feature, x1, y1, orientation):
        # "feature" is not used
        space = 1.0 * input_layer.get_space(scale) / input_layer.get_space(scale + 1)
        x2 = x1 + self.filter_size
        y2 = y1 + self.filter_size
        u_x1 = int(x1 * space)
        u_x2 = int(x2 * space)
        u_y1 = int(y1 * space)
        u_y2 = int(y2 * space)
        patch1 = input_layer.get_array(scale)[0, x1:x2, y1:y2, orientation]
        patch2 = input_layer.get_array(scale + 1)[0, u_x1:u_x2, u_y1:u_y2, orientation]

        return max(np.max(patch1), np.max(patch2))
