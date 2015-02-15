__author__ = 'yuki'
#coding UTF-8

import os
import sys
import numpy as np
from PIL import ImageOps


class Layer(object):
    def __init__(self, largest_size, scales, orientations, layer_type, features, filter_size, previous_layer):
        self.largest_size = largest_size  # largest image size (or prototype patch size)
        self.scales = scales  # number of scales
        self.orientations = orientations  # number of orientations
        self.layer_type = layer_type  # "Input" or "s1" or "c1" or "normal_s2" or "learning_s2" or "c2"
        self.features = features  # number of features
        self.filter_size = filter_size

        self.array = []  # array = [scales][features, size, size, orientations]

        #print "size of layer:"
        for i in range(self.scales):
            features2 = self.features
            if features2 == 0:
                features2 = 1
            if self.layer_type == "Input":
                size = int(self.largest_size * (2 ** (-1.0 * i / 4)))
            elif self.layer_type == "learning_s2":
                size = self.largest_size
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            elif self.layer_type == "normal_s2":
                size = self.resize(previous_layer.get_size(i))
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            elif self.layer_type == "c2":
                size = 1
                features2 = int(self.features * (2 ** (-1.0 * i / 4)))
            else:
                size = self.resize(previous_layer.get_size(i))
            self.array.append(np.zeros((features2, size, size, self.orientations), dtype=float))
            #print size, "*", size, ", ", features2, "features"

    def set_image(self, image):
        for s in range(self.scales):
            size = self.get_size(s)
            gray_img = np.asarray(ImageOps.grayscale(image).resize((size, size))).T * 1.0 / 255
            for x in range(size):
                for y in range(size):
                    self.array[s][0, x, y, 0] = gray_img[x, y]

    def set_layer(self, folder_name, filename):
        for s in range(self.scales):
            exi = os.path.isfile(folder_name + "/" + filename + "/" + filename + self.get_layer_type() +
                                 "_" + str(s) + ".npz")
            if exi:
                load_data = np.load(folder_name + "/" + filename + "/" + filename + self.get_layer_type() +
                                    "_" + str(s) + ".npz")
                self.array[s][:, :, :, :] = load_data["arr_0"][:, :, :, :]
            else:
                print "\"" + filename + self.get_layer_type() + "_" + str(s) + ".npz" + "\"" + "is not exist"
                sys.exit()

    def get_space(self, scale):
        return self.largest_size * 1.0 / self.get_size(scale)

    def get_array(self, scale):
        return self.array[scale]

    def get_size(self, scale):
        return self.array[scale][0, :, 0, 0].size

    def get_orientations(self):
        return self.orientations

    def get_scales(self):
        return self.scales

    def get_layer_type(self):
        return self.layer_type

    def get_step(self):
        if self.layer_type == "c1":
            return 5
        else:
            return 1

    def get_features(self, scale):
        return self.array[scale][:, 0, 0, 0].size

    def resize(self, size):
        return (size - self.filter_size) / self.get_step() + 1

    def save_layer(self, folder_name, filename):
        exi = os.path.isdir(folder_name + "/" + filename)
        if not exi:
            os.mkdir(folder_name + "/" + filename)
        for s in range(self.scales):
            np.savez(folder_name + "/" + filename + "/" + filename + self.get_layer_type() +
                     "_" + str(s), self.array[s])
