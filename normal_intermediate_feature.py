__author__ = 'yuki'
#coding UTF-8

import numpy as np
import os.path as path
from filter import Filter


class NormalIntermediateFeature(Filter):
    def __init__(self, filter_size, orientations, filename):
        self.filter_size = filter_size  # size of patch
        self.orientations = orientations  # number of orientation
        self.filename = filename

    def compute_s2(self, input_layer, output_layer):
        data_number = 1
        exi = path.isfile(self.filename + "/" + str(data_number) + ".npz")
        print "\n", "normal_s2"
        while exi:
            self.prototype = np.load(self.filename + "/" + str(data_number) + ".npz")
            print "feature set", data_number
            self.compute_layer(input_layer, output_layer)
            data_number += 1
            exi = path.isfile(self.filename + "/" + str(data_number) + ".npz")

    def compute_unit(self, input_layer, scale, feature, x, y, orientation):
        patch = input_layer.get_array(scale)[0, x:x + self.filter_size, y:y + self.filter_size, orientation]
        p_patch = self.prototype["arr_0"][scale][feature, 0:self.filter_size, 0:self.filter_size, orientation]
        alpha = (self.filter_size / 4) ** 2.0
        res = np.exp(-np.linalg.norm(p_patch - patch) * 1.0 / (2 * alpha))
        return res
