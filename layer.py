__author__ = 'yuki'
#coding UTF-8

import numpy as np
from PIL import ImageOps


class Layer(object):
    def __init__(self, largest_size, scales, orientations, layer_type, features):
        self.largest_size = largest_size  # largest image size (or prototype patch size)
        self.scales = scales  # number of scales
        self.orientations = orientations  # number of orientations
        self.layer_type = layer_type  # "Input" or "s1" or "c1" or "normal_s2" or "learning_s2" or "c2"
        self.features = features  # number of features

        self.array = []  # array = [scales][features, size, size, orientations]

        print "size of layer:"
        for i in range(self.scales):
            size = int(self.largest_size * (2 ** (-1.0 * i / 4)))
            features2 = 1
            if self.layer_type == "s1":
                size = self.resize_to_s1(size)
            elif self.layer_type == "c1":
                size = self.resize_to_c1(size)
            elif self.layer_type == "learning_s2":
                size = self.largest_size
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            elif self.layer_type == "normal_s2":
                size = self.resize_to_s2(size)
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            elif self.layer_type == "c2":
                size = 1
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            self.array.append(np.zeros((features2, size, size, self.orientations), dtype=float))
            print size, "*", size, ", ", features2, "features"

    def set_layer(self, image):
        for s in range(self.scales):
            size = self.get_size(s)
            gray_img = np.asarray(ImageOps.grayscale(image).resize((size, size))).T * 1.0 / 255
            for x in range(size):
                for y in range(size):
                    self.array[s][0, x, y, 0] = gray_img[x, y]

    def get_space(self, scale):
        return self.largest_size * 1.0 / self.get_size(scale)

    def get_array(self, scale):
        return self.array[scale]

    def get_size(self, scale):
        return self.array[scale][0, :, 0, 0].size

    def get_scales(self):
        return self.scales

    def get_layer_type(self):
        return self.layer_type

    def get_step(self):
        if self.layer_type == "s1":
            return 1
        elif self.layer_type == "c1":
            return 5
        elif self.layer_type == "normal_s2":
            return 1
        elif self.layer_type == "c1":
            return 1

    def get_features(self, scale):
        return self.array[scale][:, 0, 0, 0].size

    # !!! hard cording !!!
    def resize_to_s1(self, size):
        return size - 10

    def resize_to_c1(self, size):
        size = self.resize_to_s1(size)
        return size / 5 - 1

    def resize_to_s2(self, size):
        size = self.resize_to_c1(size)
        return size - 3
