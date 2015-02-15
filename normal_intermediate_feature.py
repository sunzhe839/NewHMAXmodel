__author__ = 'yuki'
#coding UTF-8

import numpy as np
import os.path as path
from filter import Filter
from layer import Layer


class NormalIntermediateFeature(Filter):
    def __init__(self, filter_size, input_size, scales, features, orientations, folder_name, mode):
        self.filter_size = filter_size  # size of patch
        self.input_size = input_size
        self.orientations = orientations  # number of orientation
        self.scales = scales
        self.features = features
        self.folder_name = folder_name
        self.mode = mode

    def compute_s2(self, input_layer, output_layer):
        class_number = 1
        data_number = 1
        exi1 = path.isdir(self.folder_name + "/" + str(class_number) + "_" + str(data_number)
                          + "_" + str(self.input_size))
        print "\n", "normal_s2"
        while exi1:
            exi2 = path.isdir(self.folder_name + "/" + str(class_number) + "_" + str(data_number)
                              + "_" + str(self.input_size))
            while exi2:
                self.prototype = Layer(self.filter_size, self.scales, self.orientations, "learning_s2",
                                       self.features, self.filter_size, input_layer)
                self.prototype.set_layer(self.folder_name, str(class_number) + "_" + str(data_number)
                                         + "_" + str(self.input_size))
                print "feature set " + str(class_number) + "_" + str(data_number)
                self.compute_layer(input_layer, output_layer)

                data_number += 1
                exi2 = path.isdir(self.folder_name + "/" + str(class_number) + "_" + str(data_number)
                                  + "_" + str(self.input_size))
            data_number = 1
            class_number += 1
            exi1 = path.isdir(self.folder_name + "/" + str(class_number) + "_" + str(data_number)
                              + "_" + str(self.input_size))

    def compute_unit(self, input_layer, scale, feature, x, y, orientation):
        patch = input_layer.get_array(scale)[0, x:x + self.filter_size, y:y + self.filter_size, orientation]
        p_patch = self.prototype.get_array(scale)[feature, 0:self.filter_size, 0:self.filter_size, orientation]
        alpha = (self.filter_size / 4) ** 2.0
        res = np.exp(-np.linalg.norm(p_patch - patch) * 1.0 / (2 * alpha))
        return res
